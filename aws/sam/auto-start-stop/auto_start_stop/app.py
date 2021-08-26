"""AWS lambda function"""
# coding: utf-8

import logging
import traceback
from datetime import datetime, timedelta, timezone
import boto3
from botocore.exceptions import ClientError


logger = logging.getLogger()
logger.setLevel(logging.INFO)


ec2 = boto3.client('ec2')
ecs = boto3.client('ecs')
rds = boto3.client('rds')
sts = boto3.client('sts')
AWS_ACCOUNT = sts.get_caller_identity()['Account']


def get_ec2_target_list():
    """
    任意のタグを持つ EC2 の instance-id を配列で返す
    """
    logger.info("get_ec2_target_list is start.")
    response = ec2.describe_instances()
    ec2_target_list = []
    for group in response['Reservations']:
        for instance in group['Instances']:
            for tag in instance['Tags']:
                if tag['Key'] == 'AutoStartStop' and tag['Value'] == 'true':
                    ec2_target_list.append(instance['InstanceId'])
    if ec2_target_list == []:
        logger.info("EC2 target is not exist.")
    else:
        logger.info("EC2 targets list %s", ec2_target_list)
    logger.info("get_ec2_target_list is end.")
    return ec2_target_list


def start_stop_ec2_instance(ec2_target):
    """
    タグ StartTime, StopTime で指定された時間に EC2 を起動停止する
    """
    logger.info("start_stop_ec2_instance is start.")
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    logger.info("Exec time is %s .", now.hour)
    response = ec2.describe_tags(
        Filters=[
            {
                "Name": "key",
                'Values': [
                    'StartTime',
                    'StopTime'
                ]
            },
            {
                "Name": "resource-id",
                'Values': [
                    ec2_target
                ]
            }
        ]
    )
    if not len(response['Tags']) == 2:
        logger.info("StartTime or StopTime is not set.")
        return
    if str(now.hour) == str(response['Tags'][0]['Value']):
        if 0 <= int(now.weekday()) <= 4:
            logger.info("%s is starting.", ec2_target)
            ec2.start_instances(
                InstanceIds=[
                    ec2_target
                ]
            )
    if str(now.hour) == str(response['Tags'][1]['Value']):
        logger.info("%s is stopping.", ec2_target)
        print("%s is stopping." % ec2_target)
        ec2.stop_instances(
            InstanceIds=[
                ec2_target
            ],
            Force=True
        )
    logger.info("start_stop_ec2_instance is end.")


def get_ecs_target_list():
    """
    任意のタグを持つ ECS サービスの cluster_arn と service_arn を配列で返す
    """
    logger.info("get_ec2_target_list is start.")
    response = ecs.list_clusters()
    ecs_target_list = []
    for cluster_arn in response['clusterArns']:
        response = ecs.list_services(
            cluster=cluster_arn
        )
        for service_arn in response['serviceArns']:
            response = ecs.describe_services(
                cluster=cluster_arn,
                services=[
                    service_arn,
                ],
                include=[
                    'TAGS',
                ]
            )
            if response['services'][0].get('tags'):
                for tag in response['services'][0]['tags']:
                    if tag['key'] == 'AutoStartStop' and tag['value'] == 'true':
                        ecs_target_list.append({'cluster': cluster_arn, 'service': response['services'][0]['serviceArn']})
    logger.info("get_ec2_target_list is end.")
    return ecs_target_list


def start_stop_ecs_service(ecs_target):
    """
    タグ StartTime, StopTime で指定された時間にタスク数を変更する
    """
    logger.info("start_stop_ecs_service is start.")
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    logger.info("Exec time is %s .", now.hour)
    response = ecs.list_tags_for_resource(
        resourceArn=ecs_target['service']
    )
    for tag in response['tags']:
        if tag['key'] == 'AutoStartStop' and tag['value'] == 'true':
            logger.info("%s is target service.", ecs_target['service'])
            for start_tag in response['tags']:
                if start_tag['key'] == 'StartTime':
                    if str(now.hour) == start_tag['value']:
                        if 0 <= int(now.weekday()) <= 4:
                            response = ecs.update_service(
                                cluster=ecs_target['cluster'],
                                service=ecs_target['service'],
                                desiredCount=1
                            )
                            logger.info(response)
                elif start_tag['key'] == 'StopTime':
                    if str(now.hour) == start_tag['value']:
                        response = ecs.update_service(
                            cluster=ecs_target['cluster'],
                            service=ecs_target['service'],
                            desiredCount=0
                        )
                        logger.info(response)
            break
    else:
        logger.info("%s is not target instance.", ecs_target['service'])
    logger.info("start_stop_ecs_service is end.")


def get_rds_target_list():
    """
    RDS インスタンスの DBInstanceIdentifier を配列で返す
    """
    logger.info('get_rds_target_list is start.')
    response = rds.describe_db_instances()
    rds_target_list = []
    for db_instance in response['DBInstances']:
        rds_target_list.append(db_instance['DBInstanceIdentifier'])
    if rds_target_list == []:
        logger.info("RDS target is not exist.")
    else:
        logger.info("RDS targets list %s", rds_target_list)
    logger.info("get_rds_target_list is end.")
    return rds_target_list


def get_aurora_target_list():
    """
    Aurora クラスターの DBClusterIdentifier を配列で返す
    """
    logger.info('get_aurora_target_list is start.')
    response = rds.describe_db_clusters()
    aurora_target_list = []
    for db_cluster in response['DBClusters']:
        aurora_target_list.append(db_cluster['DBClusterIdentifier'])
    if aurora_target_list == []:
        logger.info('AURORA target is not exist.')
    else:
        logger.info("RDS targets list %s", aurora_target_list)
    logger.info('get_aurora_target_list is end.')
    return aurora_target_list


def start_stop_rds_instance(target, db_type):
    """
    タグ AutoStartStop, StartTime, StopTime で指定された時間に RDS インスタンス, Aurora クラスターを起動停止する
    """
    logger.info('start_stop_rds_instance is start.')
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    logger.info("Exec time is %s .", now.hour)
    response = rds.list_tags_for_resource(
        ResourceName=("arn:aws:rds:ap-northeast-1:%s:db:%s" % (AWS_ACCOUNT, target))
    )
    for tag in response['TagList']:
        if tag['Key'] == 'AutoStartStop' and tag['Value'] == 'true':
            logger.info('%s is target instance.', target)
            for start_tag in response['TagList']:
                if start_tag['Key'] == 'StartTime':
                    if str(now.hour) == start_tag['Value']:
                        if 0 <= int(now.weekday()) <= 4:
                            if db_type == 'RDS':
                                start_rds_instance(target)
                            elif db_type == 'AURORA':
                                start_aurora_cluster(target)
                elif start_tag['Key'] == 'StopTime':
                    if str(now.hour) == start_tag['Value']:
                        if db_type == 'RDS':
                            stop_rds_instance(target)
                        elif db_type == 'AURORA':
                            stop_aurora_cluster(target)
            break
    else:
        logger.info('%s is not target instance.', target)
    logger.info('start_stop_rds_instance is end.')


def start_aurora_cluster(db_name):
    """
    Aurora クラスターを起動する
    """
    try:
        response = rds.start_db_cluster(DBClusterIdentifier=db_name)
        logger.info('response: %s', str(response))
        logger.info('%s is start.', db_name)
    except ClientError:
        logging.info(traceback.format_exc())


def stop_aurora_cluster(db_name):
    """
    Aurora クラスターを停止する
    """
    try:
        response = rds.stop_db_cluster(DBClusterIdentifier=db_name)
        logger.info('response: %s', str(response))
        logger.info('%s is stop.', db_name)
    except ClientError:
        logging.info(traceback.format_exc())


def start_rds_instance(rds_target):
    """
    RDS インスタンスを起動する
    """
    try:
        response = rds.start_db_instance(DBInstanceIdentifier=rds_target)
        logger.info('response: %s', str(response))
        logger.info('%s is start.', rds_target)
    except ClientError:
        logging.info(traceback.format_exc())


def stop_rds_instance(rds_target):
    """
    RDS インスタンスを停止する
    """
    try:
        response = rds.stop_db_instance(DBInstanceIdentifier=rds_target)
        logger.info('response: %s', str(response))
        logger.info('%s is stop.', rds_target)
    except ClientError:
        logging.info(traceback.format_exc())


def lambda_handler(event, context):
    #pylint: disable=unused-argument
    """
    メイン関数
    """
    logger.info("lambda function is start.")
    for ec2_target in get_ec2_target_list():
        start_stop_ec2_instance(ec2_target)
    for ecs_target in get_ecs_target_list():
        start_stop_ecs_service(ecs_target)
    for rds_target in get_rds_target_list():
        start_stop_rds_instance(rds_target, 'RDS')
    for aurora_target in get_aurora_target_list():
        start_stop_rds_instance(aurora_target, 'AURORA')
    logger.info("lambda function is end.")