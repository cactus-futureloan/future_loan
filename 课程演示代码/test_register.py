import random
import unittest
import ddt
import json

from common import requests_handler
from common import mysql_handler
from middleware import handler

# 获取excel数据
test_data = handler.MiddleHandler.excel.read_data("register_success")
print(test_data)
# 初始化logger
logger = handler.MiddleHandler.logger


@ddt.ddt
class TestRegister(unittest.TestCase):

    @ddt.data(*test_data)
    def test_register(self, test_info):
        """测试注册接口"""
        if "#phone#" in test_info["data"]:
            phone = self.random_phonenum()
            test_info["data"] = test_info["data"].replace("#phone#", phone)

        logger.info("正在执行第{}条用例：{}".format(test_info["case_id"], test_info["title"]))
        logger.info("第{}条测试用例的数据是{}".format(test_info["case_id"], test_info))
        # 访问接口
        logger.info("第{}次访问注册接口".format(test_info["case_id"]))
        resp = requests_handler.visit(
            test_info["url"],
            method=test_info["method"],
            json=json.loads(test_info["data"]),
            headers=json.loads(test_info["headers"])
        )

        try:
            for k, v in json.loads(test_info["expected"]).items():
                self.assertTrue(v == resp[k])
            # 登录成功的断言
            if resp["code"] == 0:
                # 查询数据库
                sql_data = "SELECT * FROM member WHERE  mobile_phone = {}".format(
                    json.loads(test_info["data"])["mobile_phone"])
                data = mysql_handler.MysqlHandler(
                    host="120.78.128.25",
                    user="future",
                    password="123456",
                    database="futureloan"
                ).query(sql_data)
                self.assertTrue(data["mobile_phone"] == json.loads(test_info["data"])["mobile_phone"])
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))
        # 登录失败记录日志并抛出异常
        except AssertionError as e:
            logger.handle("第{}条测试用例无法通过：{}".format(test_info["case_id"], e))
            raise e

    def random_phonenum(self):
        """随机生成手机号，用于注册成功的用例"""
        while True:
            phone = "15"
            for i in range(9):
                last_num = random.randint(0, 9)
                phone += str(last_num)

            db = handler.MiddleHandler.db()
            sql = "SELECT * FROM member WHERE mobile_phone = {};".format(phone)
            data = db.query(sql,one=True)
            if not data:
                db.close()
            return phone
            db.close()


if __name__ == '__main__':
    unittest.main()
