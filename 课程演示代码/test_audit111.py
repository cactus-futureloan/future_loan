import json
import unittest
from decimal import Decimal

import ddt

from middleware import handler
from common import requests_handler

env_data = handler.MiddleHandler()
logger = env_data.logger
cases = env_data.excel.read_data("audit")
print(cases)


@ddt.ddt
class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
    # 普通用户登录
        cls.token = env_data.token
        cls.member_id = env_data.member_id
    # 管理员用户登录
    # 在yaml中添加管理员的账号和密码
    # 封装admin_login函数进行登录，放到handler中
        cls.admin_token = env_data.admin_token
    def setUp(self):
        # 添加项目
        self.loan_id = env_data.loan_id
        self.db = env_data.db_class()

    def tearDown(self):
        self.db.close()

    @ddt.data(*cases)
    def test_audit(self, case_info):
        """测试提现接口"""
        logger.info("正在执行第{}条用例：{}".format(case_info["case_id"], case_info["title"]))
        data = case_info["data"]
        if "#loan_id#" in data:
            data = data.replace("#loan_id#", str(self.loan_id))
        data = eval(data)
        print(data)

        headers = case_info["headers"]
        if "#token#" in headers:
            headers = headers.replace("#token#", self.token)
        headers = eval(headers)

        if "#admin_token#" in headers:
            headers = headers.replace("#token#", self.admin_token)
        headers = eval(headers)
         # 动态生成一个已经不是审核状态的标
        # 直接在数据库中查找status ！= 1，
        data = case_info["data"]
        if "#pass_loan_id#" in data:
            data = self.db.query("SELECT * FROM loan WHERE status != 1")

        data = eval(data)

        data = case_info["data"]
        if "#pass_loan_id#" in data:
            data = data.replace("#loan_id#", str(env_data.pass_loan_id))
        data = eval(data)


        resp = requests_handler.visit(
            url=env_data.yaml_data["host"] + case_info["url"],
            method=case_info["method"],
            json=data,
            headers=headers
        )
        # x = json.loads(data["amount"])
        # print(x)
        try:
            expected = json.loads(case_info["expected"])
            for k,v in expected.items():
                print(resp[k])
                self.assertTrue(v == resp[k])

            if resp["code"] == 0:
            # 验证数据库状态
                loan = self.db.query(
                    "SELECT * FROM loan WHERE id={}".format(self.loan_id)
                )
                self.assertTrue(loan["status"] == expected["status"])
                env_data.pass_loan_id = loan["id"]
            logger.info("第{}条测试用例通过".format(case_info["case_id"]))
        except AssertionError as e:
            logger.error("第{}条测试用例无法通过：{}".format(case_info["case_id"], e))
            raise e


if __name__ == '__main__':
    unittest.main()
