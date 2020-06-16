# coding: utf-8

import boto3
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger()
logger.setLevel(logging.INFO)


ec2 = boto3.client('ec2')
rds = boto3.client('rds')


def get_ec2_target_list():
    logger.info("get_ec2_target_list is start.")
    response = ec2.describe_instances()
    ec2_target_list= []
    for group in response['Reservations']:
        for instance in group['Instances']:
            for tag in instance['Tags']:
                ec2_target_info = []
                if tag['Key'] == 'AutoStartStop' and tag['Value'] == 'true':
                    ec2_target_list.append(instance['InstanceId'])
    if ec2_target_list == []:
        logger.info("EC2 target is not exsit.")
    else:
        logger.info("EC2 tagets list %s" % ec2_target_list)
    logger.info("get_ec2_target_list is end.")
    return ec2_target_list


def start_stop_ec2_instance(ec2_target):
    logger.info("start_stop_ec2_instance is start.")
    jst = timezone(timedelta(hours=9), 'JST')
    now = datetime.now(jst)
    logger.info("Exec time is %s oclock." % now.hour)
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
    if not 2 == len(response['Tags']):
        logger.info("StartTime or StopTime is not set.")
        return
    if str(now.hour) == str(response['Tags'][0]['Value']):
        logger.info("%s is starting." % ec2_target)
        ec2.start_instances(
            InstanceIds=[
                ec2_target
            ]
        )
    if str(now.hour) == str(response['Tags'][1]['Value']):
        logger.info("%s is stopping." % ec2_target)
        print("%s is stopping." % ec2_target)
        ec2.stop_instances(
            InstanceIds=[
                ec2_target
            ],
            Force=True
        )
    logger.info("start_stop_ec2_instance is end.")


def get_rds_aurora_target_list():
    None #TODO


def start_stop_rds_aurora_instance(rds_aurora_target):
    None #TODO


def start_aurora_cluster(db_name):
    try:
        response = rds.start_db_cluster(DBClusterIdentifier=db_name)
        logger.info('response: ' + str(response))
        logger.info(db_name + ' is start.')
    except:
        logging.info(traceback.format_exc())


def stop_aurora_cluster(db_name):
    try:
        response = rds.stop_db_cluster(DBClusterIdentifier=db_name)
        logger.info('response: ' + str(response))
        logger.info(db_name + ' is stop.')
    except:
        logging.info(traceback.format_exc())


def start_rds_instance(db_name):
    try:
        response = rds.start_db_instance(DBInstanceIdentifier=db_name)
        logger.info('response: ' + str(response))
        logger.info(db_name + ' is start.')
    except:
        logging.info(traceback.format_exc())


def stop_rds_instance(db_name):
    try:
        response = rds.stop_db_instance(DBInstanceIdentifier=db_name)
        logger.info('response: ' + str(response))
        logger.info(db_name + ' is stop.')
    except:
        logging.info(traceback.format_exc())


def start_db(db_name):
    logging.info('looking for ' + db_name)
    response = rds.describe_db_instances(
        Filters=[
            {
                'Name': 'db-instance-id',
                'Values': [
                        db_name,
                ]
            }
        ]
    )
    if response['DBInstances']:
        start_rds_instance(db_name)
        return
    response = rds.describe_db_clusters(
        Filters=[
            {
                'Name': 'db-cluster-id',
                        'Values': [
                            db_name,
                        ]
            }
        ]
    )
    if response['DBClusters']:
        start_aurora_cluster(db_name)
        return
    logging.info(db_name + ' is not exist.')


def stop_db(db_name):
    logging.info('looking for ' + db_name)
    response = rds.describe_db_instances(
        Filters=[
            {
                'Name': 'db-instance-id',
                'Values': [
                        db_name,
                ]
            }
        ]
    )
    if response['DBInstances']:
        stop_rds_instance(db_name)
        return
    response = rds.describe_db_clusters(
        Filters=[
            {
                'Name': 'db-cluster-id',
                        'Values': [
                            db_name,
                        ]
            }
        ]
    )
    if response['DBClusters']:
        stop_aurora_cluster(db_name)
        return
    logging.info(db_name + ' is not exist.')


def lambda_handler(event, context):
    logger.info("lambda function is start.")
    for ec2_target in get_ec2_target_list():
        start_stop_ec2_instance(ec2_target)
    for rds_aurora_target in get_rds_aurora_target_list():
        start_stop_rds_aurora_instance(rds_aurora_target)
    logger.info("lambda function is end.")