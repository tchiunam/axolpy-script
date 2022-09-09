import random
import time
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

    def set_string(self, event_name: str, key_name: str) -> str:
        """
        Set a string value to the redis server.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the key.
        :tye key_name: str

        :return: The value of the string set.
        :rtype: str
        """

        request_type = "SET"
        result: str = None
        value = random_LDP()

        start_time = time.time()
        try:
            result = self.rc.set(name=key_name, value=value)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def get_string(self, event_name: str, key_name: str) -> str:
        """
        Get a string value from the redis server.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the key.
        :tye key_name: str

        :return: The value of the string obtained.
        :rtype: str
        """

        request_type = "GET"
        result: str = None

        start_time = time.time()
        try:
            result = self.rc.get(name=key_name)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def push_list_elements(self, event_name: str, key_name: str) -> int:
        """
        Push a list of elements to the redis server.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the list.
        :type key_name: str

        :return: The number of elements pushed to the list.
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
            result = self.rc.lpush(key_name, *elements)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def add_set_members(self, event_name: str, key_name: str) -> int:
        """
        Add a set of members to the redis server.

        :param event_name: The name of the event.
        :type event_name:str
        :param key_name: The name of the set.
        :type key_name: str

        :return: The number of members added to the set.
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
            result = self.rc.sadd(key_name, *members)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def set_hash_elements(self, event_name: str, key_name: str) -> int:
        """
        Set a hash of elements to the redis server.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the hash.
        :type key_name: str

        :return: The number of elements set to the hash.
        :rtype: int
        """

        request_type = "HSET"
        result: int = -1
        elements = dict()
        for i in range(4):
            elements[str(i)] = random_LDP(length=random.randint(5, 10))

        start_time = time.time()
        try:
            result = self.rc.hset(name=key_name, mapping=elements)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def get_hash_element(self, event_name: str, key_name: str) -> Any | None:
        """
        Get an element of a hash from the redis server.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the hash.
        :type key_name: str

        :return: The value of the element.
        :rtype: Any | None
        """

        request_type = "HGET"
        result: Any | None = None

        start_time = time.time()
        try:
            result = self.rc.hget(name=key_name, key=random.randint(0, 3))
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def del_hash_element(self, event_name: str, key_name: str) -> int:
        """
        Delete an element of a hash from the redis server.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the hash.
        :type key_name: str

        :return: The number of elements deleted from the hash.
        :rtype: int
        """

        request_type = "HDEL"
        result: int = -1

        start_time = time.time()
        try:
            result = self.rc.hdel(key_name, random.randint(0, 3))
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def add_sorted_set_member(self, event_name: str, key_name: str) -> int:
        """
        Add elements to a sorted set.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the sorted set.
        :type key_name: str

        :return: The number of members added to the sorted set.
        :rtype: int
        """

        request_type = "ZADD"
        result: int = -1
        member = random_LDP(length=5)
        score = random.randint(1, 100)

        start_time = time.time()
        try:
            result = self.rc.zadd(
                name=key_name,
                mapping={member: score}, nx=False
            )
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                exception=e
            )
        else:
            length = result
            events.request_success.fire(
                request_type=request_type,
                name=event_name,
                response_time=get_response_time_in_ms(
                    start_time=start_time,
                    end_time=time.time()
                ),
                response_length=length
            )

        return result

    def get_sorted_set_range(
            self,
            event_name: str,
            key_name: str,
            start: int = 0,
            end: int = -1) -> list:
        """
        Get a range of members from a sorted set.

        :param event_name: The name of the event.
        :type event_name: str
        :param key_name: The name of the sorted set.
        :type key_name: str
        :param start: The start index of the sorted set. Default is 0.
        :type start: int
        :param end: The end index of the sorted set. Default is -1.
        :type end: int

        :return: The members of the sorted set.
        :rtype: list
        """

        request_type = "ZRANGE"
        result: list = None

        start_time = time.time()
        try:
            result = self.rc.zrange(name=key_name, start=start, end=end)
        except Exception as e:
            events.request_failure.fire(
                request_type=request_type,
                name=event_name,
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
                name=event_name,
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
        name = "string_lt_static"
        self._client.set_string(event_name=name, key_name=name)
        self._client.get_string(event_name=name, key_name=name)

    @ task
    @ tag("list")
    def list(self):
        name = "list_lt_static"
        self._client.push_list_elements(event_name=name, key_name=name)

    @ task
    @ tag("set")
    def set(self):
        name = "set_lt_static"
        self._client.add_set_members(event_name=name, key_name=name)

    @ task
    @ tag("hash")
    def hash(self):
        name = "hash_lt_static"
        self._client.set_hash_elements(event_name=name, key_name=name)
        self._client.get_hash_element(event_name=name, key_name=name)
        self._client.del_hash_element(event_name=name, key_name=name)

    @ task
    @ tag("sorted-set")
    def sorted_set(self):
        name = "sorted_set_lt_static"
        self._client.add_sorted_set_member(event_name=name, key_name=name)
        self._client.get_sorted_set_range(
            event_name=name,
            key_name=name,
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
        event_name = "string_lt_dynamic"
        key_name = random_LDP()
        self._client.set_string(event_name=event_name, key_name=key_name)
        self._client.get_string(event_name=event_name, key_name=key_name)

    @ task
    @ tag("list")
    def list(self):
        event_name = "list_lt_dynamic"
        key_name = random_LDP()
        self._client.push_list_elements(
            event_name=event_name,
            key_name=key_name
        )

    @ task
    @ tag("set")
    def set(self):
        event_name = "set_lt_dynamic"
        key_name = random_LDP()
        self._client.add_set_members(event_name=event_name, key_name=key_name)

    @ task
    @ tag("hash")
    def hash(self):
        event_name = "hash_lt_dynamic"
        key_name = random_LDP()
        self._client.set_hash_elements(
            event_name=event_name,
            key_name=key_name
        )
        self._client.get_hash_element(event_name=event_name, key_name=key_name)
        self._client.del_hash_element(event_name=event_name, key_name=key_name)

    @ task
    @ tag("sorted-set")
    def sorted_set(self):
        event_name = "sorted_set_lt_dynamic"
        key_name = random_LDP()
        self._client.add_sorted_set_member(
            event_name=event_name,
            key_name=key_name
        )
        self._client.get_sorted_set_range(
            event_name=event_name,
            key_name=key_name
        )
