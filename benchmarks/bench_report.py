import uuid

import uuid_utils
import uuid_utils.compat as uuid_compat

HEX = "a8098c1a-f86e-11da-bd1a-00112444be1e"
BYTES = uuid.UUID(HEX).bytes


def stdlib_uuid4() -> None:
    uuid.uuid4()


def compat_uuid4() -> None:
    uuid_compat.uuid4()


def uuid_utils_uuid4() -> None:
    uuid_utils.uuid4()


def stdlib_uuid7() -> None:
    uuid.uuid7()


def compat_uuid7() -> None:
    uuid_compat.uuid7()


def uuid_utils_uuid7() -> None:
    uuid_utils.uuid7()


def stdlib_from_hex() -> None:
    uuid.UUID(HEX)


def uuid_utils_from_hex() -> None:
    uuid_utils.UUID(HEX)


def stdlib_from_bytes() -> None:
    uuid.UUID(bytes=BYTES)


def uuid_utils_from_bytes() -> None:
    uuid_utils.UUID(bytes=BYTES)


__benchmarks__ = [
    ("uuid4()", [stdlib_uuid4, compat_uuid4, uuid_utils_uuid4]),
    ("uuid7()", [stdlib_uuid7, compat_uuid7, uuid_utils_uuid7]),
    ("UUID from hex", [stdlib_from_hex, uuid_utils_from_hex]),
    ("UUID from bytes", [stdlib_from_bytes, uuid_utils_from_bytes]),
]
