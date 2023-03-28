import uuid

import uuid_utils


def uuid_from_hex() -> None:
    for _ in range(10_000):
        uuid.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


def uuid_utils_from_hex() -> None:
    for _ in range(10_000):
        uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


def uuid_from_bytes() -> None:
    for _ in range(10_000):
        uuid.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


def uuid_utils_from_bytes() -> None:
    for _ in range(10_000):
        uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


def uuid_from_int() -> None:
    for _ in range(10_000):
        uuid.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


def uuid_utils_from_int() -> None:
    for _ in range(10_000):
        uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


__benchmarks__ = [
    (uuid_from_hex, uuid_utils_from_hex, "UUID from hex"),
    (uuid_from_bytes, uuid_utils_from_bytes, "UUID from bytes"),
    (uuid_from_int, uuid_utils_from_int, "UUID from int"),
]
