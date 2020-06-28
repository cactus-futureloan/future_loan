"""运行所有的用例"""
import os
import unittest
from config import config
from libs.HTMLTestRunnerNew import HTMLTestRunner
from datetime import datetime

loader = unittest.TestLoader()
test_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"tests")
suite = loader.discover(test_path)
# 测试报告的路径
now_time = datetime.now().strftime("%y-%m-%d-%H-%M-%S")
reports_filename = "reports-{}.html".format(now_time)
reports_path = os.path.join(config.REPORTS_PATH,reports_filename)


# 运行用例
with open(reports_path,"wb") as f:
    runner = HTMLTestRunner(f,
                            title="cactus的自动化测试报告",
                            description="这是cactus的自动化测试报告",
                            tester="cactus")
    runner.run(suite)


if __name__ == '__main__':
    unittest.main()