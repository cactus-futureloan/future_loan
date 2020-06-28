import jsonpath

user = {"data":{"username":"yuz","pwd":"123456"}}
print(jsonpath.jsonpath(user,"$..username"))

res = {
    "code": 0,
    "msg": "OK",
    "data": {
        "id": 15055,
        "leave_amount": 20.0,
        "mobile_phone": "18810979246",
        "reg_name": "cactus",
        "reg_time": "2020-06-13 20:17:48.0",
        "type": 1,
        "token_info": {
            "token_type": "Bearer",
            "expires_in": "2020-06-16 21:11:50",
            "token": "eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjE1MDU1LCJleHAiOjE1OTIzMTMxMTB9.50dBCQBVy4yMOWW3jZf2lCbcUC9H5mvT2Wq-AB-26Fjx4t1kvy24Jx_-kdDeTOTtR7lL1_fKGvOgWB3iqHMB4w"
        }
    },
    "copyright": "Copyright 柠檬班 © 2017-2020 湖南省零檬信息技术有限公司 All Rights Reserved"
}

token_type = jsonpath.jsonpath(res,"$..token_type")
token = jsonpath.jsonpath(res,"$..token")
member_id = jsonpath.jsonpath(res,"$..id")
