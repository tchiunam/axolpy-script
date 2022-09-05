import time
from random import random
from typing import Any

from axolpy import configuration
from axolpy.util.helper.string import generate_random_string
from locust import User, events, tag, task
from rediscluster import RedisCluster


def random_LDP(length: int = 10) -> str:
    """
    Generate a simple random string with a length of 10 characters with
    letters, digits and punctuation.

    :param length: Length of the string. Default is 10.
    :type length: int

    :return: Random string.
    :rtype: str
    """

    return generate_random_string(
        length=length,
        with_digits=True,
        with_punctuation=True
    )


def get_response_time_in_ms(start_time: float, end_time: float) -> int:
    """
    Get the response time in milliseconds.

    :param start_time: Start time.
    :type start_time: float
    :param end_time: End time.
    :type end_time: float

    :return: Response time in milliseconds.
    :rtype: int
    """

    return int((end_time - start_time) * 1000)


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
        value = random_LDP()

        start_time = time.time()
        try:
            result = self.rc.set(name=name, value=value)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
        # Create a list of random length with random elements.
        elements = [random_LDP(
            length=random.randint(5, 10)
        )] * random.randint(1, 5)

        start_time = time.time()
        try:
            result = self.rc.lpush(name, *elements)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = result.bit_length()
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
        # Create a set of random length with random members.
        size = random.randint(1, 5)
        members = set()
        for _ in range(size):
            members.add(random_LDP(
                length=random.randint(5, 10),
            ))

        start_time = time.time()
        try:
            result = self.rc.sadd(name, *members)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
            elements.append(random_LDP(length=random.randint(5, 10)))

        start_time = time.time()
        try:
            result = self.rc.hset(name, *elements)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
            result = self.rc.hget(name=name, key=random.randint(0, 3))
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

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
        member = random_LDP(length=5)
        score = random.randint(1, 100)

        start_time = time.time()
        try:
            result = self.rc.zadd(name=name, mapping={member: score}, nx=False)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(result.encode())
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def get_sorted_set_range(
            self,
            name: str,
            start: int = 0,
            end: int = -1) -> list:
        """
        Get a range of members from a sorted set.

        :param name: The name of the sorted set.
        :type name: str
        :param start: The start index of the sorted set. Default is 0.
        :type start: int
        :param end: The end index of the sorted set. Default is -1.
        :type end: int

        :return: The members of the sorted set replied from redis server.
        :rtype: list
        """

        request_type = "ZRANGE"
        result: list = None

        start_time = time.time()
        try:
            result = self.rc.zrange(name=name, start=start, end=end)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = len(str(result))
            events.request_success.fire(
                request_type=request_type,
                name=name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result


config = configuration.AxolpyConfigManager.get_context(name="redis")


class RedisUserStaticKey(User):
    """
    A user that uses static keys.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = RedisClient(
            host=config["cluster-nodes"]["master.1.ip"],
            port=config["cluster-nodes"]["master.1.port"]
        )

    @ task
    @ tag("string")
    def string(self):
        self._client.set_string(name="string_load_test")
        self._client.get_string(name="string_load_test")

    @ task
    @ tag("list")
    def list(self):
        self._client.push_list_elements(name="list_load_test")

    @ task
    @ tag("set")
    def set(self):
        self._client.add_set_members(name="set_load_test")

    @ task
    @ tag("hash")
    def hash(self):
        self._client.set_hash_elements(name="hash_load_test")
        self._client.get_hash_element(name="hash_load_test")
        self._client.del_hash_element(name="hash_load_test")

    @ task
    @ tag("sorted-set")
    def sorted_set(self):
        self._client.add_sorted_set_member(name="sorted_set_add_load_test")
        self._client.get_sorted_set_range(
            name="sorted_set_range_load_test",
            end=100
        )


class RedisUserRandomKey(User):
    """
    A user that uses random keys.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = RedisClient(
            host=config["cluster-nodes"]["master.2.ip"],
            port=config["cluster-nodes"]["master.2.port"]
        )

    @ task
    @ tag("string")
    def string(self):
        name = random_LDP()
        self._client.set_string(name=name)
        self._client.get_string(name=name)

    @ task
    @ tag("list")
    def list(self):
        self._client.push_list_elements(name=random_LDP())

    @ task
    @ tag("set")
    def set(self):
        self._client.add_set_members(name=random_LDP())

    @ task
    @ tag("hash")
    def hash(self):
        name = random_LDP()
        self._client.set_hash_elements(name=name)
        self._client.get_hash_element(name=name)
        self._client.del_hash_element(name=name)

    @ task
    @ tag("sorted-set")
    def sorted_set(self):
        name = random_LDP()
        self._client.add_sorted_set_member(name=name)
        self._client.get_sorted_set_range(name=name)
