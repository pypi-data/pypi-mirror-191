# -*- coding: utf-8 -*-
import json

from redis import Redis, RedisCluster


def flatten(items):
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item


def get_values(values):
    return list(flatten(values))


def list_or_args(keys, args):
    try:
        iter(keys)
        if isinstance(keys, (bytes, str)):
            keys = [keys]
        else:
            keys = list(keys)
    except TypeError:
        keys = [keys]
    keys.extend(get_values(args))
    return keys


class SetMixin:
    def set_add(self, key, value, *args):
        """
        向集合添加一个或多个成员
        :param key: 集合的key
        :param value: 集合的值
        :return: 添加成功的个数
        """
        values = list_or_args(value, args)
        return self.redis.sadd(key, *values)

    def set_rem(self, key, value, *args):
        """
        移除集合中一个或多个成员
        :param key: 集合的key
        :param value: 集合的值
        :return: 移除成功的个数
        """
        values = list_or_args(value, args)
        return self.redis.srem(key, *values)

    def set_members(self, key):
        """
        返回集合中的所有成员
        :param key: 集合的key
        :return: 集合中的所有成员
        """
        return self.redis.smembers(key)

    def set_ismember(self, key, value, *args):
        """
        判断 value 元素是否是集合 key 的成员
        :param key: 集合的key
        :param value: 集合的值
        :return:
        """
        if args:
            return self.redis.smismember(key, value, *args)
        return self.redis.sismember(key, value)

    def set_card(self, key):
        """
        获取集合的成员数
        :param key: 集合的key
        :return:
        """
        return self.redis.scard(key)

    sadd = set_add
    srem = set_rem
    smembers = set_members
    sismember = set_ismember
    scard = set_card


class ListMixin:

    def list_push(self, key, value, *args, left=False, plus=False):
        """
        将一个或多个值 value 插入到列表 key 的表头或表尾
        :param key: 列表的key
        :param value: 列表的值
        :param left: 是否插入到表头
        :param plus: 使用 lpushx 或 rpushx 命令
        :return: 执行 (L/R)PUSH[X] 命令后，列表的长度
        """
        values = list_or_args(value, args)

        if left:
            return self.redis.lpushx(key, *values) if plus else self.redis.lpush(key, *values)
        else:
            return self.redis.rpushx(key, *values) if plus else self.redis.rpush(key, *values)

    def list_pop(self, key, count=None, left=False):
        """
        移除并返回列表 key 的头元素或尾元素
        :param key: 列表的key
        :param count: 移除的个数
        :param left: 是否移除头元素
        :return: 列表的头元素或尾元素
        """
        return self.redis.lpop(key, count) if left else self.redis.rpop(key, count)

    def list_iteral(self, key):
        """
        迭代列表
        :param key: 列表的key
        :return:
        """
        count = self.llen(key)
        for i in range(count):
            yield self.lindex(key, i)

    lpush = lambda self, key, value, *args: self.list_push(key, value, *args, left=True)  # noqa
    rpush = lambda self, key, value, *args: self.list_push(key, value, *args, left=False)  # noqa
    lpushx = lambda self, key, value, *args: self.list_push(key, value, *args, left=True, plus=True)  # noqa
    rpushx = lambda self, key, value, *args: self.list_push(key, value, *args, left=False, plus=True)  # noqa

    lpop = lambda self, key, count=None: self.list_pop(key, count, left=True)  # noqa
    rpop = lambda self, key, count=None: self.list_pop(key, count, left=False)  # noqa

    literal = list_iteral

    llen = list_len = lambda self, key: self.redis.llen(key)  # noqa
    lindex = list_index = lambda self, key, index: self.redis.lindex(key, index)  # noqa
    linsert = list_insert = lambda self, key, refvalue, value, left=False: self.redis.linsert(key,
                                                                                              'BEFORE' if left else 'AFTER',
                                                                                              refvalue, value)  # noqa
    lset = list_set = lambda self, key, index, value: self.redis.lset(key, index, value)  # noqa


class HashMixin:
    def hash_set(self, name, key=None, value=None, mapping=None, nx=False):
        """
        将哈希表 key 中的域 field 的值设为 value
        :param name: 哈希表的name
        :param key: 哈希表的域
        :param value: 哈希表的值
        :param mapping: 哈希表的映射
        :param nx: 只有在域 field 不存在时，设置哈希表字段的值
        :return: 如果 field 是哈希表中的一个新建域，并且值设置成功，返回 1 。如果哈希表中域 field 已经存在且旧值已被新值覆盖，返回 0
        """
        if nx:
            return self.redis.hsetnx(name, key, value)
        return self.redis.hset(name, key, value, mapping)

    def hash_get(self, name, key):
        """
        返回哈希表 key 中给定域 field 的值
        :param name: 哈希表的name
        :param key: 哈希表的域
        :return: 给定域的值
        """
        return self.redis.hget(name, key)

    def hash_mget(self, name, key, *args):
        """
        返回哈希表 key 中，一个或多个给定域的值
        :param name: 哈希表的name
        :param key: 哈希表的域
        :return: 给定域的值
        """
        return self.redis.hmget(name, key, *args)

    def hash_del(self, name, key, *args):
        """
        删除哈希表 key 中的一个或多个指定域，不存在的域将被忽略
        :param name: 哈希表的name
        :param key: 哈希表的域
        :return: 被成功移除的域的数量，不包括被忽略的域
        """
        keys = list_or_args(key, args)
        return self.redis.hdel(name, *keys)

    def hash_exists(self, name, key):
        """
        查看哈希表 key 中，给定域 field 是否存在
        :param name: 哈希表的name
        :param key: 哈希表的域
        :return: 如果哈希表含有给定域，返回 1 。如果哈希表不含有给定域，或 key 不存在，返回 0
        """
        return self.redis.hexists(name, key)

    def hash_getall(self, name):
        """
        返回哈希表 name 中，所有的域和值
        :param name: 哈希表的name
        :return: 以列表形式返回哈希表的域和域的值
        """
        return self.redis.hgetall(name)


class RedisStore(SetMixin, ListMixin, HashMixin):
    def __init__(self, url=None, cluster=False, **kwargs):
        """
        :param url: redis://[:password@]host:port/db
        :param cluster: 是否集群
        """
        self.cluster = cluster
        redis_cls = RedisCluster if cluster else Redis

        if url is not None:
            self.redis_instance = redis_cls.from_url(url, **kwargs)
        else:
            self.redis_instance = redis_cls(**kwargs)

    @property
    def redis(self) -> Redis:
        return self.redis_instance


if __name__ == '__main__':
    uri = 'redis://localhost:6379/0'
    redis_conn = RedisStore(uri, decode_responses=True)
    # redis_conn.set_add('test', '1', '2', '3')
    # redis_conn.set_rem('test', '1234', '3333', ['12222', '3333'], ('1222'))
    # print(redis_conn.set_card('test'))
    # print(redis_conn.set_members('test'))
    # print(redis_conn.set_ismember('test', 'test'))
    # print(redis_conn.set_ismember('test', 'test', 'test1'))

    # redis_conn.list_push('list_test', '1', '2', '3')
    # print(redis_conn.llen('list_test'))
    #
    # for x in redis_conn.literal('list_test'):
    #     print(x)

    # redis_conn.hash_set('hash_test', mapping={'name': 'test', 'age': 18})
    _dict = {
        "data_list": [
            # 数据格式：
            # {'key': '短信模板key', 'name': '可读名称', 'codes': '代码', 'crawler': '谁来爬'}
            # or
            # {'crawler': '谁来爬', 'stuffs': [{'key': '短信模板key', 'name': '可读名称', 'codes': '代码'}]}

            # {'key': 'tong', 'name': '铜', 'code': 'JO_112062', 'crawler': 'CNGold'},   # 更改渠道
            {'crawler': 'CCMN', 'stuffs': [
                {'key': 'tong', 'name': '铜', 'code': '1#铜'},
            ]},

            {'key': 'lv', 'name': '铝', 'code': 'JO_112063', 'crawler': 'CNGold'},
            {'key': 'guigang', 'name': '硅钢', 'code': 'JO_112450', 'crawler': 'CNGold'},

            {'crawler': 'MySteel', 'stuffs': [
                {'key': 'lxc', 'name': '铝型材', 'code': 'ID01198849'},
                {'key': 'l201', 'name': '冷轧卷板 201-LH/2B', 'code': 'ID00003350'},
                {'key': 'l304', 'name': '冷轧卷板 304/2B', 'code': 'ID01225622'}
            ]}
        ]
    }
    redis_conn.hash_set('default.group', 'job.stuff', json.dumps(_dict))
