import copy
import os
import pickle
import sys
import time
from uuid import SafeUUID, getnode

import pytest
import uuid_utils


def test_uuid_str() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert str(uuid) == "a8098c1a-f86e-11da-bd1a-00112444be1e"


def test_uuid_repr() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert repr(uuid) == "UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')"


def test_uuid_constructor() -> None:
    with pytest.raises(TypeError):
        uuid_utils.UUID()


def test_uuid_from_hex() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert str(uuid) == "a8098c1a-f86e-11da-bd1a-00112444be1e"

    with pytest.raises(ValueError):
        uuid_utils.UUID("0-0-0-0-0")


def test_uuid_from_bytes() -> None:
    uuid = uuid_utils.UUID(
        bytes=b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e"
    )
    assert str(uuid) == "a8098c1a-f86e-11da-bd1a-00112444be1e"

    with pytest.raises(ValueError):
        uuid_utils.UUID(bytes=b"\xa8\t\x8c\x1a\xf8n\x11")


def test_uuid_from_bytes_le() -> None:
    uuid = uuid_utils.UUID(
        bytes_le=b"\x1a\x8c\t\xa8n\xf8\xda\x11\xbd\x1a\x00\x11$D\xbe\x1e"
    )
    assert str(uuid) == "a8098c1a-f86e-11da-bd1a-00112444be1e"


def test_uuid_from_int() -> None:
    uuid = uuid_utils.UUID(int=223359875637754765292326297443183672862)
    assert str(uuid) == "a8098c1a-f86e-11da-bd1a-00112444be1e"


def test_uuid_from_fields() -> None:
    uuid = uuid_utils.UUID(fields=(2819197978, 63598, 4570, 189, 26, 73622928926))
    assert str(uuid) == "a8098c1a-f86e-11da-bd1a-00112444be1e"


def test_uuid_from_fields_node_out_of_range() -> None:
    with pytest.raises(ValueError, match="field 6 out of range"):
        uuid_utils.UUID(fields=(0, 0, 0, 0, 0, 2**48))


def test_uuid_setattr() -> None:
    uuid = uuid_utils.UUID(int=223359875637754765292326297443183672862)

    with pytest.raises(TypeError):
        uuid.int = 123  # type: ignore[misc]  # ty: ignore[invalid-assignment]


def test_uuid1() -> None:
    uuid = uuid_utils.uuid1()
    assert isinstance(uuid, uuid_utils.UUID)

    uuid = uuid_utils.uuid1(node=getnode())
    assert uuid.node == getnode()

    uuid = uuid_utils.uuid1(node=getnode(), clock_seq=123)
    assert isinstance(uuid, uuid_utils.UUID)
    assert uuid.node == getnode()
    assert uuid.clock_seq == 123


@pytest.mark.parametrize("name", ["python.org", b"python.org"])
def test_uuid3(name: str) -> None:
    uuid = uuid_utils.uuid3(namespace=uuid_utils.NAMESPACE_DNS, name=name)
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid4() -> None:
    uuid = uuid_utils.uuid4()
    assert isinstance(uuid, uuid_utils.UUID)


@pytest.mark.parametrize("name", ["python.org", b"python.org"])
def test_uuid5(name: str) -> None:
    uuid = uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name=name)
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid6() -> None:
    uuid = uuid_utils.uuid6()
    assert isinstance(uuid, uuid_utils.UUID)
    assert uuid.version == 6

    uuid = uuid_utils.uuid6(getnode())
    assert isinstance(uuid, uuid_utils.UUID)
    assert uuid.node == getnode()

    uuid = uuid_utils.uuid6(getnode(), 1234)
    assert uuid.node == getnode()
    assert uuid.clock_seq == 1234


def test_uuid7() -> None:
    uuid = uuid_utils.uuid7()
    assert isinstance(uuid, uuid_utils.UUID)
    assert uuid.version == 7


def test_uuid8() -> None:
    uuid = uuid_utils.uuid8()
    assert isinstance(uuid, uuid_utils.UUID)
    assert uuid.version == 8

    uuid = uuid_utils.uuid8(0x123456789ABC)
    assert uuid.version == 8

    uuid = uuid_utils.uuid8(0x123456789ABC, 0xDEF)
    assert uuid.version == 8

    uuid = uuid_utils.uuid8(0x123456789ABC, 0xDEF, 0x3FFFFFFFFFFFFFFF)
    assert uuid.version == 8


def test_uuid_comparisons() -> None:
    uuid_1 = uuid_utils.uuid8(0, 0, 1)
    uuid_2 = uuid_utils.uuid8(0, 0, 2)

    assert uuid_1 < uuid_2
    assert uuid_1 <= uuid_2
    assert uuid_1 != uuid_2
    assert uuid_2 > uuid_1
    assert uuid_2 >= uuid_1

    uuid_1 = uuid_utils.uuid8(0, 0, 1)
    uuid_2 = uuid_utils.uuid8(0, 0, 1)

    assert uuid_1 == uuid_2
    assert hash(uuid_1) == hash(uuid_2)


TIME_CASES = [
    ("a8098c1a-f86e-11da-bd1a-00112444be1e", 133692293110139930),  # v1
    ("1ec9414c-232a-6b00-b3c8-9e6bdeced846", 138648505420000000),  # v6
    ("017f22e2-79b0-7cc3-98c4-dc0c0c07398f", 1645557742000),  # v7
    ("a8098c1a-f86e-41da-bd1a-00112444be1e", 133692293110139930),  # v4
    ("017f22e2-79b0-7cc3-18c4-dc0c0c07398f", 919712545760027362),  # non-RFC4122
    ("00000000-0000-0000-0000-000000000000", 0),  # nil
]


@pytest.mark.parametrize("value, expected", TIME_CASES)
def test_time(value: str, expected: int) -> None:
    assert uuid_utils.UUID(value).time == expected


@pytest.mark.parametrize("version", [1, 2, 3, 4, 5, 7, 8])
def test_uuid_version(version: int) -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e", version=version)
    assert uuid.version == version


def test_uuid_version_none_for_non_rfc4122() -> None:
    uuid = uuid_utils.UUID(int=0)
    assert uuid.version is None


def test_uuid_illegal_version() -> None:
    with pytest.raises(ValueError):
        uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e", version=0)

    with pytest.raises(ValueError):
        uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e", version=9)


def test_uuid_properties() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")

    assert uuid.bytes == b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e"
    assert uuid.bytes_le == b"\x1a\x8c\t\xa8n\xf8\xda\x11\xbd\x1a\x00\x11$D\xbe\x1e"
    assert uuid.clock_seq_hi_variant == 189
    assert uuid.clock_seq_low == 26
    assert uuid.clock_seq == 15642
    assert uuid.fields == (2819197978, 63598, 4570, 189, 26, 73622928926)
    assert uuid.hex == "a8098c1af86e11dabd1a00112444be1e"
    assert uuid.int == 223359875637754765292326297443183672862
    assert uuid.node == 73622928926
    assert uuid.time == 133692293110139930
    assert uuid.time_low == 2819197978
    assert uuid.time_mid == 63598
    assert uuid.time_hi_version == 4570
    assert uuid.urn == "urn:uuid:a8098c1a-f86e-11da-bd1a-00112444be1e"
    assert uuid.variant == "specified in RFC 4122"
    assert uuid.version == 1


def test_uuid_timestamp() -> None:
    now_ms = int(time.time() * 1000)
    assert abs(uuid_utils.uuid7().timestamp - now_ms) < 10_000

    with pytest.raises(ValueError):
        uuid_utils.uuid4().timestamp


def test_pickle() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    uuid_pickle = pickle.dumps(uuid)
    uuid_unpickle = pickle.loads(uuid_pickle)
    assert uuid_unpickle == uuid


def test_copy() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert copy.copy(uuid) == uuid
    assert copy.deepcopy(uuid) == uuid


def test_is_safe() -> None:
    assert uuid_utils.uuid1().is_safe is SafeUUID.unknown
    assert uuid_utils.uuid4().is_safe is SafeUUID.unknown


def test_getnode() -> None:
    node = uuid_utils.getnode()
    assert 0 < node < (1 << 48)
    assert uuid_utils.getnode() == node


@pytest.mark.skipif(
    sys.platform in ("win32", "emscripten", "wasi"),
    reason="Does not run on Windows or WASM",
)
def test_reseed_is_called_when_forking() -> None:
    read_end, write_end = os.pipe()
    uuid_utils.uuid4()

    pid = os.fork()
    if pid == 0:
        os.close(read_end)
        next_uuid_child = str(uuid_utils.uuid4())
        with os.fdopen(write_end, "w") as write_pipe:
            write_pipe.write(next_uuid_child)
        os._exit(0)

    os.close(write_end)
    next_parent_uuid = uuid_utils.uuid4()
    os.waitpid(pid, 0)
    with os.fdopen(read_end) as read_pipe:
        uuid_from_pipe = uuid_utils.UUID(read_pipe.read())

    assert next_parent_uuid != uuid_from_pipe


def test_max_and_nil() -> None:
    assert uuid_utils.UUID("ffffffff-ffff-ffff-ffff-ffffffffffff") == uuid_utils.MAX
    assert uuid_utils.UUID("00000000-0000-0000-0000-000000000000") == uuid_utils.NIL
