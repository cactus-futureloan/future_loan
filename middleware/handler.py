import json
import os

from pymysql.cursors import DictCursor

from common import yaml_handler, requests_handler
from common.excel_handler import ExcelHandler
from common.logging_handler import logging_handler
from common.mysql_handler import MysqlHandler
from config import config
from jsonpath import jsonpath


class MysqlMiddle(MysqlHandler):

    def __init__(self):
        # 读取配置文件
        cof_db = MiddleHandler.yaml_data["db"]
        super().__init__(
            host=cof_db["host"],
            port=cof_db["port"],
            user=cof_db["user"],
            password=cof_db["password"],
            charset=cof_db["charset"],
            database=cof_db["database"],
            cursorclass=DictCursor
        )


class MiddleHandler:
    """初始化所有的数据，
    在其他的模块中可以重复使用
    """
    # 加载配置文件
    config = config

    # 获取yaml数据
    yaml_data = yaml_handler.read_yaml(os.path.join(config.CONFIG_PATH, "config.yml"))

    # 读取excel数据
    excel_path = config.DATA_PATH
    excel_filename = yaml_data["excel"]["file"]
    excel = ExcelHandler(os.path.join(excel_path, excel_filename))

    # 初始化logger
    logger_config = yaml_data["log"]
    logger = logging_handler(
        logger_name=logger_config["loggername"],
        file=os.path.join(config.LOG_PATH, logger_config["file"]),
        logger_level=logger_config["logger_level"],
        stream_level=logger_config["stream_level"],
        file_level=logger_config["file_level"],
    )

    db_class = MysqlMiddle

    def login(self, user):
        """登录测试账号"""
        res = requests_handler.visit(
            url=MiddleHandler.yaml_data["host"] + "/member/login",
            method="post",
            headers={"X-Lemonban-Media-Type": "lemonban.v2"},
            json=user
        )

        # 提取token
        # jsonpath
        token_type = jsonpath(res, "$..token_type")[0]
        token_str = jsonpath(res, "$..token")[0]
        token = " ".join([token_type, token_str])
        member_id = jsonpath(res, "$..id")[0]
        return {"token": token, "member_id": member_id}

    def recharge(self):
        data = {"member_id": self.member_id, "amount": 500000}
        resp = requests_handler.visit(
            url=MiddleHandler.yaml_data["host"] + "/member/recharge",
            method="post",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data
        )

    def withdraw(self):
        data = {"member_id": self.member_id, "amount": 500000}
        resp = requests_handler.visit(
            url=MiddleHandler.yaml_data["host"] + "/member/withdraw",
            method="post",
            headers={"X-Lemonban-Media-Type": "lemonban.v2", "Authorization": self.token},
            json=data
        )

    def add_project(self):
        data = {"member_id":self.member_id,
                "title":"借钱去月球看星星",
                "amount":100000,
                "loan_rate":12.0,
                "loan_term":3,
                "loan_date_type":1,
                "bidding_days":5}
        resp = requests_handler.visit(
            url=MiddleHandler.yaml_data["host"] + "/loan/add",
            method="post",
            headers={"X-Lemonban-Media-Type":"lemonban.v2", "Authorization": self.token},
            json=data
        )
        return jsonpath(resp,"$..id")[0]

    def audit(self):
        data = {"loan_id":self.loan_id,"approved_or_not":True}
        resp = requests_handler.visit(
            url=MiddleHandler.yaml_data["host"] + "/loan/audit",
            method="patch",
            headers={"X-Lemonban-Media-Type":"lemonban.v2", "Authorization": self.admin_token},
            json=data
        )
        return data["loan_id"]

    def replace_data(self, data):
        import re
        patten = r"#(.+?)#"
        while re.search(patten, data):
            key = re.search(patten, data).group(1)
            value = getattr(self, key, "")
            data = re.sub(patten, str(value) , data, 1)
        return data

    @property
    def token(self):
        return self.login(self.yaml_data["user"])["token"]

    @property
    def member_id(self):
        return self.login(self.yaml_data["user"])["member_id"]

    @property
    def admin_token(self):
        return self.login(self.yaml_data["admin_user"])["token"]

    @property
    def loan_id(self):
        return self.add_project()

    @property
    def pass_loan_id(self):
        return self.audit()

if __name__ == '__main__':
    # print(MiddleHandler.excel)
    # print(MiddleHandler.yaml_data)
    # print(MysqlMiddle())
    # 测试login函数
    # print(login())
    # print(MiddleHandler().token)
    # print(MiddleHandler().token)
    # print(MiddleHandler().member_id)
    # excel = MiddleHandler().excel
    # data = excel.read_data("login")
    # print(data)
    # print(type(MiddleHandler().loan_id))
    MiddleHandler().audit()