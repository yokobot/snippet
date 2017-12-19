"""
AWS Management Console Login Check
"""
# coding: utf-8

import boto3

class ConsoleLoginCheck:
    """
    AWS cloudtrail log をパースして console login があったら slack に通知する
    """
    def __init__(self):
        self.cloudtrail = boto3.client('cloudtrail', region_name='ap-northeast-1')

    def parse_cloud_trail(self):
        """
        cloud trail 解析用関数
        """
        pass

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
    pass
