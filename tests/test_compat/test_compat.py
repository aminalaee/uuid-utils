import uuid
from typing import Callable

import pytest
from uuid_utils.compat import uuid1, uuid3, uuid4, uuid5, uuid6, uuid7, uuid8


@pytest.mark.parametrize("generator", [uuid1, uuid4, uuid6, uuid7])
def test_uuid(generator: Callable[..., uuid.UUID]) -> None:
    assert isinstance(generator(), uuid.UUID)


def test_uuid3() -> None:
    assert isinstance(uuid3(uuid.NAMESPACE_DNS, "python.org"), uuid.UUID)


def test_uuid5() -> None:
    assert isinstance(uuid5(uuid.NAMESPACE_DNS, "python.org"), uuid.UUID)


def test_uuid8() -> None:
    assert isinstance(uuid8(b"1234567812345678"), uuid.UUID)
