import time
from random import random
from typing import Any

from axolpy.util.helper.string import generate_random_string
from locust import User, events, tag, task
from rediscluster import RedisCluster


class RedisClient(object):
    """
    A redis client to perform load test on redis cluster.
    """

    def __init__(
            self,
            host="localhost",
            port=6379,
            password=None):
        """
        Initialize the redis client.

        :param host: The host of the redis server.
        :type host: str
        :param port: The port of the redis server.
        :type port: int
        :param password: The password of the redis server.
        :type password: str
        """

        self.rc = RedisCluster(startup_nodes=[{"host": host, "port": port}],
                               password=password,
                               decode_responses=True)

    def set_string(self, name: str) -> str:
        """
        Set a string value to the redis server.

        :param name: The name of the string.
        :type name: str

        :return: The value of the string replied from redis server.
        :rtype: str
        """

        request_type = "SET"
        result: str = None

        start_time = time.time()
        try:
            result = self.rc.set(
                name=name,
                value=generate_random_string(
                    length=10,
                    with_digits=True,
                    with_punctuation=True))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def get_string(self, name: str) -> str:
        """
        Get a string value from the redis server.

        :param name: The name of the string.
        :type name: str

        :return: The value of the string replied from redis server.
        :rtype: str
        """

        request_type = "GET"
        result: str = None

        start_time = time.time()
        try:
            result = self.rc.get(name=name)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def push_list_elements(self, name: str) -> int:
        """
        Push a list of elements to the redis server.

        :param name: The name of the list.
        :type name: str

        :return: The length of the list replied from redis server.
        :rtype: int
        """

        request_type = "LPUSH"
        result: int = -1
        size = random.randint(1, 5)
        elements = list()
        for _ in range(size):
            elements.append(generate_random_string(
                length=random.randint(5, 10),
                with_digits=True,
                with_punctuation=True))

        start_time = time.time()
        try:
            result = self.rc.lpush(name, *elements)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = result.bit_length()
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def add_set_members(self, name: str) -> int:
        """
        Add a set of members to the redis server.

        :param name: The name of the set.
        :type name: str

        :return: The number of members added to the set replied from redis server.
        :rtype: int
        """

        request_type = "SADD"
        result: int = -1
        size = random.randint(1, 5)
        members = set()
        for _ in range(size):
            members.add(generate_random_string(
                length=random.randint(5, 10),
                with_digits=True,
                with_punctuation=True))

        start_time = time.time()
        try:
            result = self.rc.sadd(name, *members)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def set_hash_elements(self, name: str) -> int:
        """
        Set a hash of elements to the redis server.

        :param name: The name of the hash.
        :type name: str

        :return: The number of fields that were added to the hash replied from redis server.
        :rtype: int
        """

        request_type = "HSET"
        result: int = -1
        elements = list()
        for i in range(4):
            elements.append(str(i))
            elements.append(
                generate_random_string(
                    length=random.randint(5, 10),
                    with_digits=True,
                    with_punctuation=True))

        start_time = time.time()
        try:
            result = self.rc.hset(name, *elements)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def get_hash_element(self, name: str) -> Any | None:
        """
        Get an element of a hash from the redis server.

        :param name: The name of the hash.
        :type name: str

        :return: The hash of elements replied from redis server.
        :rtype: Any | None
        """

        request_type = "HGET"
        result: Any | None = None

        start_time = time.time()
        try:
            result = self.rc.hget(
                name=name,
                key=random.randint(0, 3))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def del_hash_element(self, name: str) -> int:
        """
        Delete an element of a hash from the redis server.

        :param name: The name of the hash.
        :type name: str

        :return: The number of fields that were deleted from the hash replied from redis server.
        :rtype: int
        """

        request_type = "HDEL"
        result: int = -1

        start_time = time.time()
        try:
            result = self.rc.hdel(name, random.randint(0, 3))
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def add_sorted_set_member(self, name: str) -> int:
        """
        Add elements to a sorted set.

        :param name: The name of the sorted set.
        :type name: str

        :return: The number of elements added to the sorted set replied from redis server.
        :rtype: int
        """

        request_type = "ZADD"
        result: int = -1
        member = generate_random_string(
            length=5,
            with_digits=True,
            with_punctuation=True)
        score = random.randint(1, 100)

        start_time = time.time()
        try:
            result = self.rc.zadd(name, {member: score}, nx=False)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(result.encode())
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result

    def get_sorted_set_members(self, name: str) -> list:
        """
        Get members from a sorted set.

        :param name: The name of the sorted set.
        :type name: str

        :return: The members of the sorted set replied from redis server.
        :rtype: list
        """

        request_type = "ZRANGE"
        result: list = None

        start_time = time.time()
        try:
            result = self.rc.zrange(name, 0, 100)
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=total_time,
                response_length=length)

        return result


class RedisUserStaticKey(User):
    """
    A user that uses static keys.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = RedisClient()

    @ task
    @ tag("string")
    def string(self):
        self._client.set_string(name="string_load_test")
        self._client.get_string(name="string_load_test")

    @ task
    @ tag("list")
    def list(self):
        self._client.push_list_elements("list_lpush_operation")

    @ task
    @ tag("set")
    def set(self):
        self._client.add_set_members("set_sadd_operation")

    @ task
    @ tag("hash")
    def hash(self):
        self._client.set_hash_elements("hash_load_test")
        self._client.get_hash_element("hash_load_test")
        self._client.del_hash_element("hash_load_test")

    @ task
    @ tag("sorted-set")
    def sorted_set(self):
        self._client.add_sorted_set_member("sorted_set_add_load_test")
        self._client.get_sorted_set_members("sorted_set_range_load_test")
