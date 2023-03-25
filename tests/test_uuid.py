from uuid import getnode

import pytest

import uuid_utils


def test_uuid_str() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert uuid.hex == "a8098c1af86e11dabd1a00112444be1e"


def test_uuid_repr() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert repr(uuid) == "UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')"


def test_uuid_from_hex() -> None:
    uuid = uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert uuid.hex == "a8098c1af86e11dabd1a00112444be1e"

    with pytest.raises(ValueError):
        uuid_utils.UUID("0-0-0-0-0")


def test_uuid_from_bytes() -> None:
    uuid = uuid_utils.UUID(
        bytes=b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e"
    )

    assert uuid.bytes == b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e"

    with pytest.raises(ValueError):
        uuid_utils.UUID(bytes=b"\xa8\t\x8c\x1a\xf8n\x11")


def test_uuid_from_bytes_le() -> None:
    uuid = uuid_utils.UUID(
        bytes_le=b"\x1a\x8c\t\xa8n\xf8\xda\x11\xbd\x1a\x00\x11$D\xbe\x1e"
    )
    assert uuid.bytes_le == b"\x1a\x8c\t\xa8n\xf8\xda\x11\xbd\x1a\x00\x11$D\xbe\x1e"


def test_uuid_from_int() -> None:
    uuid = uuid_utils.UUID(int=223359875637754765292326297443183672862)

    assert uuid.int == 223359875637754765292326297443183672862
    assert uuid.__int__() == 223359875637754765292326297443183672862


def test_uuid_setattr() -> None:
    uuid = uuid_utils.UUID(int=223359875637754765292326297443183672862)

    with pytest.raises(TypeError):
        uuid.int = 123  # type: ignore


def test_uuid1() -> None:
    uuid = uuid_utils.uuid1(node=8155362240700)
    assert isinstance(uuid, uuid_utils.UUID)

    uuid = uuid_utils.uuid1(node=8155362240700, clock_seq=123)
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid4() -> None:
    uuid = uuid_utils.uuid4()
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid5() -> None:
    uuid = uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid6() -> None:
    uuid = uuid_utils.uuid6(getnode(), 1679665408)
    assert isinstance(uuid, uuid_utils.UUID)

    uuid = uuid_utils.uuid6(getnode())
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid7() -> None:
    uuid = uuid_utils.uuid7(1679665408)
    assert isinstance(uuid, uuid_utils.UUID)

    uuid = uuid_utils.uuid7()
    assert isinstance(uuid, uuid_utils.UUID)


def test_uuid8() -> None:
    uuid = uuid_utils.uuid8(b"1234567812345678")
    assert isinstance(uuid, uuid_utils.UUID)
