import os
import pymysql


class Database:
    def __init__(self):
        self.conn = None
        self.host = None
        self.database = None
        self.user = None
        self.password = None

        if 'DB_HOST' in os.environ:
            self.host = os.environ['DB_HOST']
        if 'DB_NAME' in os.environ:
            self.database = os.environ['DB_NAME']
        if 'DB_USER' in os.environ:
            self.user = os.environ['DB_USER']
        if 'DB_PASS' in os.environ:
            self.password = os.environ['DB_PASS']

        if 'DB_HOST' in os.environ and 'DB_NAME' in os.environ and 'DB_USER' in os.environ and 'DB_PASS' in os.environ:
            self.connet({
                'conn': self.conn,
                'database': self.database,
                'user': self.user,
                'password': self.password
            })


    def connect(self, conf):
        self.conn = pymysql.connect(
                host=conf['conn'],
                database=conf['database'],
                user=conf['user'],
                password=conf['password']
        )


    def sql(self, sql):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return cursor.fetchall()


    def commit(self):
        if self.conn is not None:
            return self.conn.commit()


    def query(self, sql):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            return self.conn.commit()


    def dict(self, sql, keys):
        if self.conn is not None:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            data = cursor.fetchall()
            return [dict(zip(keys, value)) for value in list(data)]


    def close(self):
        if self.conn is not None:
            return self.conn.close()
