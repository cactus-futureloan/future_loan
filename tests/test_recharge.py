import os
import unittest
import ddt
import json

from common import requests_handler
from common.excel_handler import ExcelHandler
from middleware import handler
from decimal import Decimal

# 初始化数据
cases = handler.MiddleHandler.excel.read_data("recharge")
logger = handler.MiddleHandler.logger
env_data = handler.MiddleHandler()


def add(*args):
    sum = 0
    for i in args:
        sum += i
    return sum

def sub(a,b):
    return a-b

def mulit(a,b):
    return a*b

def demo(*args):
    pass

def demo01(a,b):
    pass

def demo02(a):
    pass


@ddt.ddt
class TestRecharge(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 登录
        cls.token = env_data.token
        cls.member_id = env_data.member_id

    def setUp(self):
        self.db = env_data.db_class()

    def tearDown(self):
        self.db.close()

    @ddt.data(*cases)
    def test_recharge(self, case_info):
        """测试充值接口"""

        # data = case_info["data"]
        # if "#member_id#" in data:
        #     data = data.replace("#member_id#", str(self.member_id))
        # data = eval(data)
        #
        # headers = case_info["headers"]
        # if "#token#" in headers:
        #     headers = headers.replace("#token#", self.token)

        data = env_data.replace_data(case_info["data"])
        print(data)
        headers = env_data.replace_data(case_info["headers"])
        print(headers)

        # 充值之前查余额
        user_money = self.db.query("SELECT leave_amount FROM member WHERE id ={}".format(self.member_id))
        before_amount = user_money["leave_amount"]
        # 金额大于500000调用提现接口
        if before_amount >= 500000:
            env_data.withdraw()
        logger.info("正在执行第{}条用例：{}".format(case_info["case_id"], case_info["title"]))
        data = json.loads(data)
        resp = requests_handler.visit(
            url=env_data.yaml_data["host"] + case_info["url"],
            method=case_info["method"],
            headers=json.loads(headers),
            json=data
        )
        print(resp)
        data_path = os.path.join(env_data.config.DATA_PATH, "testcases.xlsx")
        try:
            expected = eval(case_info["expected"])
            self.assertTrue(expected["code"] == resp["code"])
            self.assertTrue(expected["msg"] == resp["msg"])

            if resp["code"] == 0:
                user_money = self.db.query("SELECT leave_amount FROM member WHERE id ={}".format(self.member_id))
                after_amount = user_money["leave_amount"]
                self.assertTrue(Decimal(str(before_amount)) + Decimal(str(data["amount"])) == Decimal(str(after_amount)))
            self.result = "PASS"
            logger.info("第{}条测试用例通过".format(case_info["case_id"]))
        except AssertionError as e:
            self.result = "FAIL"
            logger.error("第{}条测试用例无法通过：{}".format(case_info["case_id"], e))
            raise e
        finally:
            ExcelHandler(data_path).write(sheet_name="recharge", row=case_info["case_id"] + 1, column=9,
                                          data=self.result)


if __name__ == '__main__':
    unittest.main()
