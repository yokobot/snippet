"""
AWS Management Console Login Check
"""
# coding: utf-8

import json
from datetime import datetime
from datetime import timedelta
import urllib.request
import boto3

class ConsoleLoginCheck:
    """
    AWS cloudtrail log をパースして console login があったら slack に通知する
    """
    def __init__(self):
        self.cloudtrail = boto3.client('cloudtrail', region_name='ap-northeast-1')
        self.response_list = []
        self.content_list = []

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
        self.response_list = response['Events']

    def make_string(self):
        """
        メッセージ作成関数
        """
        for response in self.response_list:
            cloud_trail_event = json.loads(response['CloudTrailEvent'])
            user_name = cloud_trail_event['userIdentity']['userName']
            user_type = cloud_trail_event['userIdentity']['type']
            mfa_used = cloud_trail_event['additionalEventData']['MFAUsed']
            event_name = cloud_trail_event['eventName']
            source_ip_address = cloud_trail_event['sourceIPAddress']
            event_time = cloud_trail_event['eventTime']
            result = cloud_trail_event['responseElements']['ConsoleLogin']
            content = (
                'ログインユーザ\n'
                'user_name: %s\n'
                'user_type: %s\n'
                'mfa_used: %s\n'
                'event_name: %s\n'
                'source_ip_address: %s\n'
                'event_time: %s\n'
                'result: %s'
                % (
                    user_name,
                    user_type,
                    mfa_used,
                    event_name,
                    source_ip_address,
                    event_time,
                    result
                )
            )
            self.content_list.append(content)
        self.content_list.reverse()

    def send_to_slack(self, content):
        """
        slack 通知用の関数
        """
        url = 'https://hooks.slack.com/services/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'
        payload_dic = {
            "channel":'#alert',
            "username":'AWS',
            "attachments": [
                {
                    "fallback": "過去1時間のコンソールログイン記録です",
                    "color": "#36a64f",
                    "author_name": "AWS",
                    "title": content,
                }
            ],
            "icon_emoji":'grin:',
        }
        headers ={
            "pragma":"no-cache",
        }
        method = "POST"
        json_data = json.dumps(payload_dic).encode('utf-8')
        request = urllib.request.Request(url, data=json_data, method=method, headers=headers)
        with urllib.request.urlopen(request) as response:
            response_body = response.read().decode("utf-8")

def lambda_handler(event, context):
    """
    メイン関数
    """
    cloud_trail = ConsoleLoginCheck()
    cloud_trail.parse_cloud_trail()
    cloud_trail.make_string()
    for content in cloud_trail.content_list:
        cloud_trail.send_to_slack(content)

lambda_handler(1, 2)
