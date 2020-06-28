import json
import os
import unittest
from decimal import Decimal

import ddt

from common.excel_handler import ExcelHandler
from middleware import handler
from common.requests_handler import visit

env_data = handler.MiddleHandler()
logger = env_data.logger
cases = env_data.excel.read_data("audit")
print(cases)

def add(*args):
    """加法函数"""
    sum = 0
    for item in args:
        sum += item
    return sum


@ddt.ddt
class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
    # 普通用户登录
        cls.token = env_data.token
        cls.member_id = env_data.member_id
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
            data = data.replace("#loan_id#",str(self.loan_id))

        if "#pass_loan_id#" in data:
            loan_info = self.db.query("SELECT * FROM loan WHERE status != 1")
            data = data.replace("#pass_loan_id#",str(loan_info["id"]))

        headers = case_info["headers"]
        if  "#admin_token#" in headers:
            headers = headers.replace("#admin_token#",self.admin_token)

        if  "#token#" in headers:
            headers = headers.replace("#token#",self.token)

        resp = visit(
            url=env_data.yaml_data["host"] + case_info["url"],
            method = case_info["method"],
            headers = eval(headers),
            json = eval(data)
        )
        print(resp)
        data_path = os.path.join(env_data.config.DATA_PATH, "testcases.xlsx")
        try:
            expected = json.loads(case_info["expected"])
            self.assertTrue(expected["code"] == resp["code"])
            self.assertTrue(expected["msg"] ==  resp["msg"])

            if resp["code"] == 0:
            # 验证数据库状态
                loan_info_after = self.db.query("SELECT * FROM loan WHERE id={}".format(self.loan_id))
                # a = loan_info_after["status"]
                # b = eval(case_info["expected"])["status"]
                # print(a)
                # print(b)
                self.assertTrue(loan_info_after["status"] == expected["status"])
            self.result = "PASS"
            logger.info("第{}条测试用例通过".format(case_info["case_id"]))
        except AssertionError as e:
            self.result = "FAIL"
            logger.error("第{}条测试用例无法通过：{}".format(case_info["case_id"], e))
            raise e
        finally:
            ExcelHandler(data_path).write(sheet_name="audit", row=case_info["case_id"] + 1, column=9,
                                          data=self.result)


if __name__ == '__main__':
    unittest.main()
