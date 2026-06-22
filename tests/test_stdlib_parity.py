import sys
import uuid

import pytest
import uuid_utils

SAMPLE_UUIDS = [
    "a8098c1a-f86e-11da-bd1a-00112444be1e",  # v1
    "1ec9414c-232a-6b00-b3c8-9e6bdeced846",  # v6
    "017f22e2-79b0-7cc3-98c4-dc0c0c07398f",  # v7
    "320c3d4d-cc00-875b-8ec9-32d5f69181c0",  # v8
    "a8098c1a-f86e-41da-bd1a-00112444be1e",  # v4
    "00000000-0000-0000-0000-000000000000",  # nil
]

requires_stdlib_v6_v7_v8 = pytest.mark.skipif(
    sys.version_info < (3, 14),
    reason="stdlib uuid6/uuid7/uuid8 require Python 3.14",
)


def assert_fields_match(u, std) -> None:
    assert u.version == std.version
    assert u.variant == std.variant
    assert u.node == std.node
    assert u.clock_seq == std.clock_seq


@pytest.mark.parametrize("value", SAMPLE_UUIDS)
def test_parse_matches_stdlib(value: str) -> None:
    u = uuid_utils.UUID(value)
    std = uuid.UUID(value)

    assert u.bytes == std.bytes
    assert u.bytes_le == std.bytes_le
    assert u.clock_seq_hi_variant == std.clock_seq_hi_variant
    assert u.clock_seq_low == std.clock_seq_low
    assert u.clock_seq == std.clock_seq
    assert u.fields == std.fields
    assert u.hex == std.hex
    assert u.int == std.int
    assert u.node == std.node
    assert u.time_low == std.time_low
    assert u.time_mid == std.time_mid
    assert u.time_hi_version == std.time_hi_version
    assert u.urn == std.urn
    assert u.variant == std.variant
    assert u.version == std.version


@pytest.mark.parametrize("value", SAMPLE_UUIDS)
def test_constructor_inputs_match_stdlib(value: str) -> None:
    std = uuid.UUID(value)

    assert uuid_utils.UUID(hex=value).int == std.int
    assert uuid_utils.UUID(bytes=std.bytes).int == std.int
    assert uuid_utils.UUID(bytes_le=std.bytes_le).int == std.int
    assert uuid_utils.UUID(fields=std.fields).int == std.int
    assert uuid_utils.UUID(int=std.int).int == std.int


def test_hash_matches_stdlib() -> None:
    value = "a8098c1a-f86e-11da-bd1a-00112444be1e"
    assert hash(uuid_utils.UUID(value)) == hash(uuid.UUID(value))
    u = uuid_utils.UUID(value)
    assert hash(u) == hash(u.int)


@requires_stdlib_v6_v7_v8
@pytest.mark.parametrize("value", SAMPLE_UUIDS)
def test_time_matches_stdlib(value: str) -> None:
    assert uuid_utils.UUID(value).time == uuid.UUID(value).time


@pytest.mark.xfail(reason="getnode source may differ from stdlib in different systems")
def test_getnode_matches_stdlib() -> None:
    assert uuid_utils.getnode() == uuid.getnode()


def test_uuid1_shape_matches_stdlib() -> None:
    node, clock_seq = uuid.getnode(), 1234
    u = uuid_utils.uuid1(node, clock_seq)
    std = uuid.uuid1(node, clock_seq)
    assert_fields_match(u, std)


def test_uuid3_matches_stdlib() -> None:
    u = uuid_utils.uuid3(uuid_utils.NAMESPACE_DNS, "python.org")
    std = uuid.uuid3(uuid.NAMESPACE_DNS, "python.org")
    assert u.int == std.int


def test_uuid4_shape_matches_stdlib() -> None:
    u = uuid_utils.uuid4()
    std = uuid.uuid4()
    assert u.version == std.version == 4
    assert u.variant == std.variant


def test_uuid5_matches_stdlib() -> None:
    u = uuid_utils.uuid5(uuid_utils.NAMESPACE_DNS, "python.org")
    std = uuid.uuid5(uuid.NAMESPACE_DNS, "python.org")
    assert u.int == std.int


@requires_stdlib_v6_v7_v8
def test_uuid6_shape_matches_stdlib() -> None:
    node, clock_seq = uuid.getnode(), 1234
    u = uuid_utils.uuid6(node, clock_seq)
    std = uuid.uuid6(node, clock_seq)  # ty: ignore[unresolved-attribute]
    assert_fields_match(u, std)
    assert abs(u.time - std.time) < 10_000_000_000


@requires_stdlib_v6_v7_v8
def test_uuid7_shape_matches_stdlib() -> None:
    u = uuid_utils.uuid7()
    std = uuid.uuid7()  # ty: ignore[unresolved-attribute]
    assert u.version == std.version == 7
    assert u.variant == std.variant
    assert abs(u.time - std.time) < 10_000


@requires_stdlib_v6_v7_v8
def test_uuid8_matches_stdlib() -> None:
    a, b, c = 0x123456789ABC, 0xDEF, 0x3FFFFFFFFFFFFFFF
    u = uuid_utils.uuid8(a, b, c)
    std = uuid.uuid8(a, b, c)  # ty: ignore[unresolved-attribute]
    assert u.int == std.int
