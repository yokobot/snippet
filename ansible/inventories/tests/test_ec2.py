"""
Test for ansible/inventories/ec2.py
"""
# coding: utf-8

import unittest
from mock import Mock
from ec2 import Ec2Instances

class TestEc2Instances(unittest.TestCase):
    """
    Ec2Instances のテストクラス
    """
    def test_init(self):
        """
        init test
        """
        expected = True

        obj = Ec2Instances()
        actual = isinstance(obj, Ec2Instances)
        self.assertTrue(obj.client is not None)
        self.assertEqual(expected, actual)

    def test_make_target_list(self):
        """
        make_target_list test
        """
        expected = ['13.13.13.1', '13.13.13.2']
        obj = Ec2Instances()
        obj.client.describe_instances = Mock(
            return_value={
                'Reservations': [
                    {
                        'Instances': [
                            {
                                'PublicIpAddress': '13.13.13.1',
                                'State': {'Name': 'running'}
                            },
                            {
                                'PublicIpAddress': '13.13.13.2',
                                'State': {'Name': 'running'}
                            }
                        ]
                    }
                ]
            }
        )
        obj.make_target_list()
        self.assertEqual(expected, obj.target_hosts)

        expected_with_stopped = ['13.13.13.1']
        obj_with_stopped = Ec2Instances()
        obj_with_stopped.client.describe_instances = Mock(
            return_value={
                'Reservations': [
                    {
                        'Instances': [
                            {
                                'PublicIpAddress': '13.13.13.1',
                                'State': {'Name': 'running'}
                            },
                            {
                                'PublicIpAddress': '13.13.13.2',
                                'State': {'Name': 'stopped'}
                            }
                        ]
                    }
                ]
            }
        )
        obj_with_stopped.make_target_list()
        self.assertEqual(expected_with_stopped, obj_with_stopped.target_hosts)

    def test_output_json(self):
        """
        output_json test
        """
        obj = Ec2Instances()
        obj.target_hosts = ['13.13.13.1']
        actual = obj.output_json()
        # エラーなく完了することのみ確認
        self.assertEqual(actual, None)

if __name__ == '__main__':
    unittest.main()
