import uuid

import uuid_utils

node = uuid.getnode()


def uuid_uuid1() -> None:
    for _ in range(10_000):
        uuid.uuid1(node)


def uuid_utils_uuid1() -> None:
    for _ in range(10_000):
        uuid_utils.uuid1(node)


def uuid_uuid3() -> None:
    for _ in range(10_000):
        uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name="python.org")


def uuid_utils_uuid3() -> None:
    for _ in range(10_000):
        uuid_utils.uuid3(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


def uuid_uuid4() -> None:
    for _ in range(10_000):
        uuid.uuid4()


def uuid_utils_uuid4() -> None:
    for _ in range(10_000):
        uuid_utils.uuid4()


def uuid_uuid5() -> None:
    for _ in range(10_000):
        uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name="python.org")


def uuid_utils_uuid5() -> None:
    for _ in range(10_000):
        uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


__benchmarks__ = [
    (uuid_uuid1, uuid_utils_uuid1, "UUID v1"),
    (uuid_uuid3, uuid_utils_uuid3, "UUID v3"),
    (uuid_uuid4, uuid_utils_uuid4, "UUID v4"),
    (uuid_uuid5, uuid_utils_uuid5, "UUID v5"),
]
