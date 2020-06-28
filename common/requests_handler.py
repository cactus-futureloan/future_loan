import requests


# from common.logging_handler import logging_handler
# from common.os_handler import logs_path


def visit(
        url=None,
        method=None,
        # headers=None,
        params=None,
        data=None,
        json=None,
        **kwargs

):
    res = requests.request(
        url = url,
        method = method,
        params=params,
        data=data,
        json=json,
        **kwargs
    )
    return res.json()
    # log_path = logs_path("my.log")
    # logger=logging_handler("test_logger",file = log_path)

    # try:
    #     logger.info("返回结果是：{}".format(res.json()))

    # except Exception as e:
    #     logger.error("返回数据格式不是json格式的：{}".format(e))
    #     return None


# if __name__ == '__main__':
#     url = "http://api.keyou.site:8000/interfaces/"
#     headers = {
#             "Authorization":"JWT eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImxlbW9uMSIsImV4cCI6MTU5MTQ5ODQzMiwiZW1haWwiOiJsZW1vbjEwMEBxcS5jb20ifQ._WO8YGbwHKPFUGwmvEdPdRHu9KMdAWqnYkd4-UMbaG"
#         }
#     user = {
#         "username": "lemon1",
#         "password": "123456"
#     }
#     data = visit("post",url,json=user,headers=headers)
#     print(data)
if __name__ == '__main__':
#     # url = "http://api.lemonban.com/futureloan/member/register"
#     url = "http://120.78.128.25:8766/member/register"
    data = {"pwd": "12345678", "type": 1}
    url = "http://api.lemonban.com/futureloan/member/register"
    headers = {"X-Lemonban-Media-Type": "lemonban.v2"}
    resp = visit(
        url,
        method="post",
        json=data,
        headers=headers
    )
    print(resp)
#     print(res)
