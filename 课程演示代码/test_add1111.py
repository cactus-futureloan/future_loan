import random
import unittest
import ddt
import json

from common import requests_handler
from common import mysql_handler
from middleware import handler

# 获取excel数据
cases = handler.MiddleHandler.excel.read_data("recharge")
# 初始化logger
logger = handler.MiddleHandler.logger

env_data = handler.MiddleHandler()


@ddt.ddt
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 登录
        cls.token = handler.MiddleHandler().token
        cls.member_id = handler.MiddleHandler.member_id

    def setUp(self):
        self.db = env_data.db_class()

    def tearDown(self):
        self.db.close()

    @ddt.data(*cases)
    def test_recharge(self, case_info):

        data = case_info["data"]
        if "#member_id#" in data:
            data = data.replace("#member_id#", str(self.member_id))

        headers = case_info["headers"]
        if "#token#" in headers:
            headers = headers.replace("#token#", self.token)

        # 查询之前查余额
        user_money = self.db.query("SELECT leave_amount FROM member WHERE id ={}".format(self.member_id))
        before_money = user_money["leave_amount"]
        resp = requests_handler.visit(
            url=env_data.yaml_data["host"] + case_info["url"],
            method=case_info["method"],
            headers=json.loads(headers),
            json=json.loads(data)
        )
        expected = json.loads(case_info["expected"])
        self.assertTrue(expected["code"], resp["code"])
        self.assertTrue(expected["msg"], resp["msg"])

        if resp["code"] == 0:
            user_money = self.db.query("SELECT leave_amount FROM member WHERE id ={}".format(self.member_id))
            after_money = user_money["leave_amount"]
            self.assertTrue(before_money + data["amount"] == after_money)

        pass


if __name__ == '__main__':
    unittest.main()
