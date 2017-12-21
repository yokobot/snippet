"""
AWS Management Console Login Check
"""
# coding: utf-8

from datetime import datetime
from datetime import timedelta
import boto3

class ConsoleLoginCheck:
    """
    AWS cloudtrail log をパースして console login があったら slack に通知する
    """
    def __init__(self):
        self.cloudtrail = boto3.client('cloudtrail', region_name='ap-northeast-1')
        self.response_array = []

    def parse_cloud_trail(self):
        """
        cloud trail 解析用関数
        """
        response = self.cloudtrail.lookup_events(
            LookupAttributes=[
                {
                    'AttributeKey': 'EventName',
                    'AttributeValue': 'ConsoleLogin'
                },
            ],
            StartTime=datetime.now() - timedelta(hours=1, minutes=10),
            EndTime=datetime.now()
        )
        self.response_array = response['Events']

    def make_string(self, arr):
        """
        メッセージ作成関数
        """
        pass

    def send_to_slack(self, content):
        """
        slack 通知用の関数
        """
        pass

def lambda_handler(event, context):
    """
    メイン関数
    """
    cloud_trail = ConsoleLoginCheck()
    cloud_trail.parse_cloud_trail()
