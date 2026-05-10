import uuid

import uuid_utils
import uuid_utils.compat as uuid_compat

node = uuid.getnode()


def stdlib_uuid1() -> None:
    uuid.uuid1(node)


def uuid_utils_uuid1() -> None:
    uuid_utils.uuid1(node)


def compat_uuid1() -> None:
    uuid_compat.uuid1(node)


def stdlib_uuid3() -> None:
    uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name="python.org")


def uuid_utils_uuid3() -> None:
    uuid_utils.uuid3(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


def compat_uuid3() -> None:
    uuid_compat.uuid3(namespace=uuid_compat.NAMESPACE_DNS, name="python.org")


def stdlib_uuid4() -> None:
    uuid.uuid4()


def uuid_utils_uuid4() -> None:
    uuid_utils.uuid4()


def compat_uuid4() -> None:
    uuid_compat.uuid4()


def stdlib_uuid5() -> None:
    uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name="python.org")


def uuid_utils_uuid5() -> None:
    uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


def compat_uuid5() -> None:
    uuid_compat.uuid5(namespace=uuid_compat.NAMESPACE_DNS, name="python.org")


def stdlib_uuid6() -> None:
    uuid.uuid6()  # type: ignore[attr-defined]


def uuid_utils_uuid6() -> None:
    uuid_utils.uuid6()


def compat_uuid6() -> None:
    uuid_compat.uuid6()


def stdlib_uuid7() -> None:
    uuid.uuid7()  # type: ignore[attr-defined]


def uuid_utils_uuid7() -> None:
    uuid_utils.uuid7()


def compat_uuid7() -> None:
    uuid_compat.uuid7()


__benchmarks__ = [
    ("uuid1()", [stdlib_uuid1, uuid_utils_uuid1, compat_uuid1]),
    ("uuid3()", [stdlib_uuid3, uuid_utils_uuid3, compat_uuid3]),
    ("uuid4()", [stdlib_uuid4, uuid_utils_uuid4, compat_uuid4]),
    ("uuid5()", [stdlib_uuid5, uuid_utils_uuid5, compat_uuid5]),
    ("uuid6()", [stdlib_uuid6, uuid_utils_uuid6, compat_uuid6]),
    ("uuid7()", [stdlib_uuid7, uuid_utils_uuid7, compat_uuid7]),
]
