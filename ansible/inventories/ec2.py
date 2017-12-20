"""
Dynamic Inventry
"""
# coding: utf-8

from boto3.session import Session

AWS_REGION = 'ap-northeast-1'
AWS_ENV = 'dev'

class Ec2Instances:
    """
    Dynamic Inventry 作成クラス
    """
    def __init__(self):
        """
        init
        """
        session = Session(profile_name='my_profile_name')
        self.client = session.client(
            'ec2',
            region_name=AWS_REGION
        )
        self.target_hosts = []

    def make_target_list(self):
        """
        Public IP を持つ、かつ Running の EC2 の list を返す関数
        """
        res = self.client.describe_instances()
        for reservation in res['Reservations']:
            for instance in reservation['Instances']:
                if instance.get('PublicIpAddress') and instance['State']['Name'] == 'running':
                    self.target_hosts.append(instance['PublicIpAddress'])

    def output_json(self):
        """
        ansible に渡す json を作成する関数
        """
        res = {
            'ec2-instance': {
                'hosts': self.target_hosts,
                'vars': {
                    'env_name': AWS_ENV
                }
            }
        }
        print(res)

if __name__ == '__main__':
    EC2 = Ec2Instances()
    EC2.make_target_list()
    EC2.output_json()
