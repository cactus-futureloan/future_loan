import pymysql
from pymysql.cursors import DictCursor

class MysqlHandler:
    def __init__(self,
                 host=None,
                 port=3306,
                 user=None,
                 password=None,
                 charset="utf8",
                 cursorclass=DictCursor,
                 database = None
                 ):
        self.conn = pymysql.connect(
            host= host,
            port=3306,
            user=user,
            password=password,
            charset="utf8",
            database = database,
            cursorclass=DictCursor
        )
        self.cursor = self.conn.cursor()

    def query(self,sql,one=True):
        self.conn.commit() # 把最新的数据进行更新（提交事务）
        self.cursor.execute(sql)
        if one:
            return self.cursor.fetchone()
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()

if __name__ == '__main__':
    sql_data = "SELECT * FROM member LIMIT 1"
    data = MysqlHandler(
        host="120.78.128.25",
        user="future",
        password="123456",
        database="futureloan",
    ).query(sql_data)
    print(data)


