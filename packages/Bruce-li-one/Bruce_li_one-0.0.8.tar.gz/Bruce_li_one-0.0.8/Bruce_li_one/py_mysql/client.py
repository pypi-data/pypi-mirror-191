# encoding: utf-8

import pymysql


class Bruce_mysql():
    # 初始化
    def __init__(self,dbName, host="127.0.0.1",port=3306, user="root", passwd="123456"):
        self.host = host
        self.port=port
        self.user = user
        self.passwd = passwd
        self.dbName = dbName
        self.connet()

    # 连接数据库，需要传数据库地址、用户名、密码、数据库名称，默认设置了编码信息
    def connet(self):
        try:
            self.db = pymysql.connect(host=self.host,
                                      port=self.port,
                                      user=self.user,
                                      password=self.passwd,
                                      db=self.dbName,
                                      use_unicode=True,
                                      charset='utf8')
            self.cursor = self.db.cursor()
        except Exception as e:
            return e

    # 关闭数据库连接
    def close(self):
        try:
            self.cursor.close()
            self.db.close()
        except Exception as e:
            return e

    # 查询操作，查询单条数据
    def get_one(self, sql):
        # res = None
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchone()
            self.close()
        except Exception:
            res = None
        return res

    # 查询操作，查询多条数据
    def get_all(self, sql):
        # res = ()
        try:
            self.connet()
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
            self.close()
        except Exception:
            res = ()
        return res

    # 查询数据库对象
    def get_all_obj(self, sql, tableName, *args):
        resList = []
        fieldsList = []
        try:
            if (len(args) > 0):
                for item in args:
                    fieldsList.append(item)
            else:
                fieldsSql = "select COLUMN_NAME from information_schema.COLUMNS where table_name = '%s' and table_schema = '%s'" % (
                    tableName, self.dbName)
                fields = self.get_all(fieldsSql)
                for item in fields:
                    fieldsList.append(item[0])

            # 执行查询数据sql
            res = self.get_all(sql)
            for item in res:
                obj = {}
                count = 0
                for x in item:
                    obj[fieldsList[count]] = x
                    count += 1
                resList.append(obj)
            return resList
        except Exception as e:
            return e

    # 数据库插入、更新、删除操作
    def insert(self, sql):
        return self.__edit(sql)

    def update(self, sql):
        return self.__edit(sql)

    def delete(self, sql):
        return self.__edit(sql)

    def __edit(self, sql):
        # count = 0
        try:
            self.connet()
            count = self.cursor.execute(sql)
            self.db.commit()
            self.close()
        except Exception as e:
            self.db.rollback()
            count = 0
        return count
