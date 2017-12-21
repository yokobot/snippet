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
                "userIdentity": {
                    "type": "IAMUser",
                    "userName": "t-yokoyama"
                },
                "eventTime": test_time,
                "awsRegion": "ap-northeast-1",
                "sourceIPAddress": "133.13.13.133",
                "additionalEventData": {
                    "MFAUsed": "Yes"
                },
                "responseElements": {
                    "ConsoleLogin": "Success"
                },
                "eventName": "ConsoleLogin"
            }
        ]
        obj = ConsoleLoginCheck()
        obj.cloudtrail.lookup_events = Mock(
            return_value=[
                {
                    "userIdentity": {
                        "type": "IAMUser",
                        "userName": "t-yokoyama"
                    },
                    "eventTime": test_time,
                    "awsRegion": "ap-northeast-1",
                    "sourceIPAddress": "133.13.13.133",
                    "additionalEventData": {
                        "MFAUsed": "Yes"
                    },
                    "responseElements": {
                        "ConsoleLogin": "Success"
                    },
                    "eventName": "ConsoleLogin"
                }
            ]
        )
        actual = obj.parse_cloud_trail()
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
