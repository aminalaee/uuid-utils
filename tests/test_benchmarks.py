import pytest
import uuid_utils

pytest.importorskip("pytest_codspeed")


@pytest.mark.benchmark
def test_getnode() -> None:
    uuid_utils.getnode()


@pytest.mark.benchmark
def test_uuid1_() -> None:
    uuid_utils.uuid1()


@pytest.mark.benchmark
def test_uuid3() -> None:
    uuid_utils.uuid3(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


@pytest.mark.benchmark
def test_uuid4() -> None:
    uuid_utils.uuid4()


@pytest.mark.benchmark
def test_uuid5() -> None:
    uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


@pytest.mark.benchmark
def test_uuid6() -> None:
    uuid_utils.uuid6()


@pytest.mark.benchmark
def test_uuid7() -> None:
    uuid_utils.uuid7()


@pytest.mark.benchmark
def test_uuid8() -> None:
    uuid_utils.uuid8(bytes=b"\x00" * 16)


@pytest.mark.benchmark
def test_uuid_from_hex() -> None:
    uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


def test_uuid_from_bytes(benchmark) -> None:  # type: ignore[no-untyped-def]
    hex_bytes = bytes.fromhex("a8098c1af86e11dabd1a00112444be1e")
    benchmark(lambda: uuid_utils.UUID(bytes=hex_bytes))


@pytest.mark.benchmark
def test_uuid_from_int() -> None:
    int_value = 223338299594506624080436508043913872926
    uuid_utils.UUID(int=int_value)


@pytest.mark.benchmark
def test_uuid_from_fields_utils() -> None:
    uuid_utils.UUID(fields=(2819197978, 63598, 4570, 189, 26, 73622928926))
