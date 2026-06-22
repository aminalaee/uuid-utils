import uuid

from uuid_utils.compat import (
    MAX,
    NAMESPACE_DNS,
    NAMESPACE_OID,
    NAMESPACE_URL,
    NAMESPACE_X500,
    NIL,
    uuid1,
    uuid3,
    uuid4,
    uuid5,
    uuid6,
    uuid7,
    uuid8,
)


def assert_stdlib_uuid(value: uuid.UUID, version: int) -> None:
    assert type(value) is uuid.UUID
    assert value.version == version
    assert value.variant == uuid.RFC_4122


def test_constants_match_stdlib() -> None:
    assert NAMESPACE_DNS == uuid.NAMESPACE_DNS
    assert NAMESPACE_URL == uuid.NAMESPACE_URL
    assert NAMESPACE_OID == uuid.NAMESPACE_OID
    assert NAMESPACE_X500 == uuid.NAMESPACE_X500
    assert NIL == uuid.UUID(int=0)
    assert MAX == uuid.UUID(int=(1 << 128) - 1)


def test_uuid1() -> None:
    assert_stdlib_uuid(uuid1(), 1)


def test_uuid1_preserves_fields() -> None:
    node, clock_seq = 0x123456789ABC, 1234
    result = uuid1(node, clock_seq)
    assert_stdlib_uuid(result, 1)
    assert result.node == node
    assert result.clock_seq == clock_seq


def test_uuid3_matches_stdlib() -> None:
    result = uuid3(uuid.NAMESPACE_DNS, "python.org")
    assert_stdlib_uuid(result, 3)
    assert result == uuid.uuid3(uuid.NAMESPACE_DNS, "python.org")


def test_uuid4() -> None:
    assert_stdlib_uuid(uuid4(), 4)


def test_uuid5_matches_stdlib() -> None:
    result = uuid5(uuid.NAMESPACE_DNS, "python.org")
    assert_stdlib_uuid(result, 5)
    assert result == uuid.uuid5(uuid.NAMESPACE_DNS, "python.org")


def test_uuid6_preserves_fields() -> None:
    node, clock_seq = 0x123456789ABC, 1234
    result = uuid6(node, clock_seq)
    assert_stdlib_uuid(result, 6)
    assert result.node == node
    assert result.clock_seq == clock_seq


def test_uuid7() -> None:
    assert_stdlib_uuid(uuid7(), 7)


def test_uuid8() -> None:
    assert_stdlib_uuid(uuid8(0x123456789ABC, 0xDEF, 0x3FFFFFFFFFFFFFFF), 8)
