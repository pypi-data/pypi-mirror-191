#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @Time :2023/2/13 
# @Author :wsli
# @File : client.py
# @Software: PyCharm
import redis
import json
class Bruce_redis:
    def __init__(self,host="127.0.0.1",port=6379,password="",db=0,decode_responses=True):
        self.redis_client=redis.Redis(host=host,
                                      port=port,
                                      password=password,
                                      db=db,
                                      decode_responses=decode_responses)

    def get(self, key):
        """
        获取单个值
        :param key:
        :return:
        """
        value = self.redis_client.get(key)
        return value

    def mget(self, *args):
        """
        获取多个值
        :param args:
        :return:
        """
        value = self.redis_client.mget(*args)
        return value

    def set(self, key, value):
        """
        设置单个值
        :param key:
        :param value:
        :return:
        """
        value = self.redis_client.set(key, value)
        return value

    def mset(self, *args, **kwargs):
        """
        设置多个键值
        :return:
        """
        value = self.redis_client.mset(*args, **kwargs)
        return value

    def is_key_true(self, key):
        """
        判断key值是否存在
        :return:
        """
        status = self.redis_client.exists(key)
        return status

    def del_key(self, key):
        """
        删除key
        :param key:
        :return:
        """
        status = self.redis_client.delete(key)
        return status

    def clear_db_data(self):
        """
        清除当前数据库中所有数据
        :return:
        """
        pass

    def clear_dball_data(self):
        """
        清除所有库中所有数据
        :return:
        """
        pass

    def set_json(self, keyName, jsonstr):
        """
        存入json到redis中
        :return:
        """
        jsonstr = json.dumps(jsonstr)
        status=self.redis_client.set(keyName, jsonstr)
        return status

    def get_json(self, keyName):
        """
        获取key的json值
        :param keyName:
        :return:
        """

        val = self.get(keyName)
        return json.loads(val)