"""Performance benchmarks for uuid_utils using pytest-codspeed."""

import uuid

import pytest
import uuid_utils


@pytest.fixture
def node():
    """Get the hardware node for UUID v1 generation."""
    return uuid.getnode()


@pytest.mark.benchmark
def test_bench_uuid1(node):
    """Benchmark UUID v1 generation with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.uuid1(node)


@pytest.mark.benchmark
def test_bench_uuid3():
    """Benchmark UUID v3 generation with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.uuid3(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


@pytest.mark.benchmark
def test_bench_uuid4():
    """Benchmark UUID v4 generation with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.uuid4()


@pytest.mark.benchmark
def test_bench_uuid5():
    """Benchmark UUID v5 generation with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.uuid5(namespace=uuid_utils.NAMESPACE_DNS, name="python.org")


@pytest.mark.benchmark
def test_bench_uuid6(node):
    """Benchmark UUID v6 generation with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.uuid6(node)


@pytest.mark.benchmark
def test_bench_uuid7():
    """Benchmark UUID v7 generation with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.uuid7()


@pytest.mark.benchmark
def test_bench_uuid_from_hex():
    """Benchmark UUID parsing from hex string with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.UUID("a8098c1a-f86e-11da-bd1a-00112444be1e")


@pytest.mark.benchmark
def test_bench_uuid_from_bytes():
    """Benchmark UUID creation from bytes with uuid_utils."""
    test_bytes = b"\xa8\t\x8c\x1a\xf8n\x11\xda\xbd\x1a\x00\x11$D\xbe\x1e"
    for _ in range(10_000):
        uuid_utils.UUID(bytes=test_bytes)


@pytest.mark.benchmark
def test_bench_uuid_from_int():
    """Benchmark UUID creation from int with uuid_utils."""
    test_int = 223338299594347266940234570490933248542
    for _ in range(10_000):
        uuid_utils.UUID(int=test_int)


@pytest.mark.benchmark
def test_bench_uuid_from_fields():
    """Benchmark UUID creation from fields with uuid_utils."""
    for _ in range(10_000):
        uuid_utils.UUID(fields=(2819197978, 63598, 4570, 189, 26, 73622928926))
