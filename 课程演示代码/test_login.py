import unittest
import ddt
import json

from common import requests_handler
from middleware import handler

# 获取excel数据
test_data = handler.MiddleHandler.excel.read_data("login")

# 初始化logger
logger = handler.MiddleHandler.logger


@ddt.ddt
class TestLogin(unittest.TestCase):
    """测试登录接口"""
    @ddt.data(*test_data)
    def test_login(self, test_info):
        """测试登录接口"""
        logger.info("正在执行第{}条用例：{}".format(test_info["case_id"], test_info["title"]))
        logger.info("第{}条测试用例的数据是{}".format(test_info["case_id"], test_info))
        # 访问接口
        logger.info("第{}次访问登录接口".format(test_info["case_id"]))
        resp = requests_handler.visit(
            test_info["url"],
            method=test_info["method"],
            json=json.loads(test_info["data"]),
            headers=json.loads(test_info["headers"])
        )
        # 断言
        try:
            for k, v in json.loads(test_info["expected"]).items():
                self.assertTrue(v == resp[k])
            logger.info("第{}条测试用例通过".format(test_info["case_id"]))
        # 登录失败记录日志并抛出异常
        except AssertionError as e:
            logger.error("第{}条测试用例无法通过：{}".format(test_info["case_id"], e))
            raise e


if __name__ == '__main__':
    unittest.main()

