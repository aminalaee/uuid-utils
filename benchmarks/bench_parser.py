import uuid

import uuid_utils

HEX = "a8098c1a-f86e-11da-bd1a-00112444be1e"
BYTES = uuid.UUID(HEX).bytes
INT = uuid.UUID(HEX).int
FIELDS = (2819197978, 63598, 4570, 189, 26, 73622928926)


def stdlib_from_hex() -> None:
    uuid.UUID(HEX)


def uuid_utils_from_hex() -> None:
    uuid_utils.UUID(HEX)


def stdlib_from_bytes() -> None:
    uuid.UUID(bytes=BYTES)


def uuid_utils_from_bytes() -> None:
    uuid_utils.UUID(bytes=BYTES)


def stdlib_from_int() -> None:
    uuid.UUID(int=INT)


def uuid_utils_from_int() -> None:
    uuid_utils.UUID(int=INT)


def stdlib_from_fields() -> None:
    uuid.UUID(fields=FIELDS)


def uuid_utils_from_fields() -> None:
    uuid_utils.UUID(fields=FIELDS)


__benchmarks__ = [
    ("UUID from hex", [stdlib_from_hex, uuid_utils_from_hex]),
    ("UUID from bytes", [stdlib_from_bytes, uuid_utils_from_bytes]),
    ("UUID from int", [stdlib_from_int, uuid_utils_from_int]),
    ("UUID from fields", [stdlib_from_fields, uuid_utils_from_fields]),
]
