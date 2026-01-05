"""CodSpeed benchmarks for uuid-utils"""

import uuid

import pytest
import uuid_utils

node = uuid.getnode()


# UUID Generation Benchmarks
@pytest.mark.benchmark
def test_uuid1_stdlib(benchmark):
    benchmark(lambda: uuid.uuid1(node))


@pytest.mark.benchmark
def test_uuid1_utils(benchmark):
    benchmark(lambda: uuid_utils.uuid1(node))


@pytest.mark.benchmark
def test_uuid3_stdlib(benchmark):
    benchmark(lambda: uuid.uuid3(namespace=uuid.NAMESPACE_DNS, name="python.org"))


@pytest.mark.benchmark
def test_uuid3_utils(benchmark):
    benchmark(
        lambda: uuid_utils.uuid3(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")
    )


@pytest.mark.benchmark
def test_uuid4_stdlib(benchmark):
    benchmark(lambda: uuid.uuid4())


@pytest.mark.benchmark
def test_uuid4_utils(benchmark):
    benchmark(lambda: uuid_utils.uuid4())


@pytest.mark.benchmark
def test_uuid5_stdlib(benchmark):
    benchmark(lambda: uuid.uuid5(namespace=uuid.NAMESPACE_DNS, name="python.org"))


@pytest.mark.benchmark
def test_uuid5_utils(benchmark):
    benchmark(
        lambda: uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")
    )


# UUID Parsing Benchmarks
@pytest.mark.benchmark
def test_uuid_from_hex_stdlib(benchmark):
    benchmark(lambda: uuid.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e"))


@pytest.mark.benchmark
def test_uuid_from_hex_utils(benchmark):
    benchmark(lambda: uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e"))


@pytest.mark.benchmark
def test_uuid_from_bytes_stdlib(benchmark):
    hex_bytes = bytes.fromhex("a8098c1af86e11dabd1a00112444be1e")
    benchmark(lambda: uuid.UUID(bytes=hex_bytes))


@pytest.mark.benchmark
def test_uuid_from_bytes_utils(benchmark):
    hex_bytes = bytes.fromhex("a8098c1af86e11dabd1a00112444be1e")
    benchmark(lambda: uuid_utils.UUID(bytes=hex_bytes))


@pytest.mark.benchmark
def test_uuid_from_int_stdlib(benchmark):
    int_value = 223338299594506624080436508043913872926
    benchmark(lambda: uuid.UUID(int=int_value))


@pytest.mark.benchmark
def test_uuid_from_int_utils(benchmark):
    int_value = 223338299594506624080436508043913872926
    benchmark(lambda: uuid_utils.UUID(int=int_value))


@pytest.mark.benchmark
def test_uuid_from_fields_stdlib(benchmark):
    benchmark(lambda: uuid.UUID(fields=(2819197978, 63598, 4570, 189, 26, 73622928926)))


@pytest.mark.benchmark
def test_uuid_from_fields_utils(benchmark):
    benchmark(
        lambda: uuid_utils.UUID(fields=(2819197978, 63598, 4570, 189, 26, 73622928926))
    )
