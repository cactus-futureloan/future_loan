import json
import os
import unittest
import ddt

from common.excel_handler import ExcelHandler
from common.requests_handler import visit
from middleware import handler

env_data = handler.MiddleHandler()
cases = env_data.excel.read_data("invest")
print(cases)
logger = env_data.logger


@ddt.ddt
class TestInvest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 登录
        cls.token = env_data.token
        cls.member_id = env_data.member_id


    def setUp(self):
        self.db = env_data.db_class()
        # self.loan_id = env_data.loan_id
        self.pass_loan_id = env_data.pass_loan_id
        env_data.recharge()

    def tearDown(self):
        self.db.close()

    @ddt.data(*cases)
    def test_invest(self, case_info):
        """测试投资接口"""
        # before_data = self.db.query(
        #     "SELECT COUNT(*) as berfore_num FROM loan WHERE member_id={};".format(self.member_id))
        # before_num = before_data["berfore_num"]
        logger.info("正在执行第{}条用例：{}".format(case_info["case_id"], case_info["title"]))
        data = case_info["data"]
        if "#member_id#" in data:
            data = data.replace("#member_id#", str(self.member_id))

        headers = case_info["headers"]
        if "#token#" in headers:
            headers = headers.replace("#token#", self.token)

        if "#loan_id#" in data:
            data = data.replace("#loan_id#", str(self.pass_loan_id))

        # 访问接口
        data_1 = self.db.query("SELECT * FROM loan WHERE id = {}".format(self.pass_loan_id))
        resp = visit(
            url=env_data.yaml_data["host"] + case_info["url"],
            method=case_info["method"],
            json=eval(data),
            headers=eval(headers)
        )
        print(resp)
        data_path = os.path.join(env_data.config.DATA_PATH, "testcases.xlsx")
        try:
            for k, v in json.loads(case_info["expected"]).items():
                self.assertTrue(v == resp[k])
            # if resp["code"] == 0:
            #     after_data = self.db.query(
            #         "SELECT COUNT(*) as after_num FROM loan WHERE member_id={};".format(self.member_id))
            #     after_num = after_data["after_num"]
            #     self.assertTrue(before_num + 1 == after_num)
            self.result = "PASS"
            logger.info("第{}条测试用例通过".format(case_info["case_id"]))

        except AssertionError as e:
            self.result = "FAIL"
            logger.error("第{}条测试用例无法通过：{}".format(case_info["case_id"], e))
            raise e
        finally:
            ExcelHandler(data_path).write(sheet_name="add", row=case_info["case_id"] + 1, column=9,
                                          data=self.result)




if __name__ == '__main__':
    unittest.main()
