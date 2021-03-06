"""
console_login_check のテストコード
"""
# coding: utf-8

import unittest
from datetime import datetime
from datetime import timedelta
from mock import Mock
from console_login_check import ConsoleLoginCheck

class TestConsoleLoginCheck(unittest.TestCase):
    """
    テスト用クラス
    """

    def test_init(self):
        """
        init test
        """
        expected = True
        obj = ConsoleLoginCheck()
        actual = isinstance(obj, ConsoleLoginCheck)
        self.assertTrue(obj.cloudtrail is not None)
        self.assertEqual(expected, actual)

    def test_parse_cloud_trail(self):
        """
        parse_cloud_trail test
        """
        test_time = datetime.now() - timedelta(hours=1)
        expected = [
            {
                "CloudTrailEvent": '{"userIdentity": {"type": "IAMUser","userName": "t-yokoyama"},'
                                   '"eventTime": %s,"awsRegion": "ap-northeast-1",'
                                   '"sourceIPAddress": "133.13.13.133",'
                                   '"additionalEventData": {"MFAUsed": "Yes"},'
                                   '"responseElements": {"ConsoleLogin": "Success"},'
                                   '"eventName": "ConsoleLogin"}' % test_time
            }
        ]
        obj = ConsoleLoginCheck()
        obj.cloudtrail.lookup_events = Mock(
            return_value={
                'Events': [
                    {
                        "CloudTrailEvent": \
                            '{"userIdentity": {"type": "IAMUser","userName": "t-yokoyama"},'
                            '"eventTime": %s,"awsRegion": "ap-northeast-1",'
                            '"sourceIPAddress": "133.13.13.133",'
                            '"additionalEventData": {"MFAUsed": "Yes"},'
                            '"responseElements": {"ConsoleLogin": "Success"},'
                            '"eventName": "ConsoleLogin"}' % test_time
                    }
                ]
            }
        )
        obj.parse_cloud_trail()
        actual = obj.response_list
        self.assertEqual(expected, actual)

    def test_make_string(self):
        """
        make_string test
        """
        test_time = 'yyyymmddHHMMSS'
        expected = [(
            'ログインユーザ\n'
            'user_name: t-yokoyama\n'
            'user_type: IAMUser\n'
            'mfa_used: Yes\n'
            'event_name: ConsoleLogin\n'
            'source_ip_address: 133.13.13.133\n'
            'event_time: %s\n'
            'result: Success'
            % test_time
        )]
        obj = ConsoleLoginCheck()
        obj.cloudtrail.lookup_events = Mock(
            return_value={
                'Events': [
                    {
                        'CloudTrailEvent': \
                            '{"userIdentity":{"type":"IAMUser","userName":"t-yokoyama"},'
                            '"eventTime":"yyyymmddHHMMSS","eventName":"ConsoleLogin",'
                            '"sourceIPAddress":"133.13.13.133",'
                            '"responseElements":{"ConsoleLogin":"Success"},'
                            '"additionalEventData":{"MFAUsed":"Yes"}}'
                    }
                ]
            }
        )
        obj.parse_cloud_trail()
        obj.make_string()
        actual = obj.content_list
        self.assertEqual(expected, actual)

    def test_send_to_slack(self):
        """
        send_to_slack test
        """
        pass # 何を持って OK とするか考える

if __name__ == '__main__':
    unittest.main()
