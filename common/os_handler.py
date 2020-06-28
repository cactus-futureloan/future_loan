import os
import time


def reports_path():
    """测试报告路径"""
    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    report_name = "report_" + now + ".html"
    report_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reports"),
                               report_name)
    return report_path


def logs_path(log_name):
    """日志路径"""
    # now = time.strftime("%Y-%m-%d-%H-%M-%S", time.gmtime())
    # log_name = "log_" + now + ".txt"
    log_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs"), log_name)
    return log_path


def conf_path(config_name):
    """配置文件路径"""
    conf_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config"),
                             config_name)
    return conf_path


def cases_path(cases_name):
    """测试数据路径"""
    cases_path = os.path.join(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"),
                              cases_name)
    return cases_path


def test_path():
    """测试用例路径"""
    test_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "tests")
    return test_path


if __name__ == '__main__':
    report_path = reports_path()
    print(report_path)
    log_path = logs_path()
    print(log_path)
