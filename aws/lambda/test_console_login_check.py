"""
console_login_check のテストコード
"""
# coding: utf-8

import unittest
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

if __name__ == '__main__':
    unittest.main()
