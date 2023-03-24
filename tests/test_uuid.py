from pyuuid import UUID, uuid1, uuid4

import pytest


def test_uuid_str() -> None:
    uuid = UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert uuid.hex == "a8098c1af86e11dabd1a00112444be1e"


def test_uuid_repr() -> None:
    uuid = UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert repr(uuid) == "UUID('a8098c1a-f86e-11da-bd1a-00112444be1e')"


def test_uuid_from_hex() -> None:
    uuid = UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")
    assert uuid.hex == "a8098c1af86e11dabd1a00112444be1e"

    with pytest.raises(ValueError):
        UUID("0-0-0-0-0")


def test_uuid_from_bytes() -> None:
    uuid = UUID(bytes=b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e")

    assert uuid.bytes == b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e"

    with pytest.raises(ValueError):
        UUID(bytes=b"\xa8\t\x8c\x1a\xf8n\x11")


def test_uuid_from_bytes_le() -> None:
    uuid = UUID(bytes_le=b"\x1a\x8c\t\xa8n\xf8\xda\x11\xbd\x1a\x00\x11$D\xbe\x1e")
    assert uuid.bytes_le == b"\x1a\x8c\t\xa8n\xf8\xda\x11\xbd\x1a\x00\x11$D\xbe\x1e"


def test_uuid_from_int() -> None:
    uuid = UUID(int=223359875637754765292326297443183672862)

    assert uuid.int == 223359875637754765292326297443183672862
    assert uuid.__int__() == 223359875637754765292326297443183672862


def test_uuid_setattr() -> None:
    uuid = UUID(int=223359875637754765292326297443183672862)

    with pytest.raises(TypeError):
        uuid.int = 123


def test_uuid1() -> None:
    uuid = uuid1(node=8155362240700)
    assert isinstance(uuid, UUID)

    uuid = uuid1(node=8155362240700, clock_seq=123)
    assert isinstance(uuid, UUID)


def test_uuid4() -> None:
    uuid = uuid4()
    assert isinstance(uuid, UUID)
