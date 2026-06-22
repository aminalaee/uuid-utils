import sys
from typing import Final
from uuid import (
    NAMESPACE_DNS,
    NAMESPACE_OID,
    NAMESPACE_URL,
    NAMESPACE_X500,
    RESERVED_FUTURE,
    RESERVED_MICROSOFT,
    RESERVED_NCS,
    RFC_4122,
    UUID,
    SafeUUID,
    getnode,
)

def uuid1(node: int | None = None, clock_seq: int | None = None) -> UUID:
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""
    ...

if sys.version_info >= (3, 12):
    def uuid3(namespace: UUID, name: str | bytes) -> UUID:
        """Generate a UUID from the MD5 hash of a namespace UUID and a name."""
        ...

else:
    def uuid3(namespace: UUID, name: str) -> UUID:
        """Generate a UUID from the MD5 hash of a namespace UUID and a name."""
        ...

def uuid4() -> UUID:
    """Generate a random UUID."""
    ...

if sys.version_info >= (3, 12):
    def uuid5(namespace: UUID, name: str | bytes) -> UUID:
        """Generate a UUID from the SHA-1 hash of a namespace UUID and a name."""
        ...
else:
    def uuid5(namespace: UUID, name: str) -> UUID:
        """Generate a UUID from the SHA-1 hash of a namespace UUID and a name."""
        ...

def uuid6(node: int | None = None, clock_seq: int | None = None) -> UUID:
    """Similar to `uuid1` but where fields are ordered differently
    for improved DB locality.

    More precisely, given a 60-bit timestamp value as specified for UUIDv1,
    for UUIDv6 the first 48 most significant bits are stored first, followed
    by the 4-bit version (same position), followed by the remaining 12 bits
    of the original 60-bit timestamp.
    """
    ...

def uuid7() -> UUID:
    """Generate a UUID from a Unix timestamp in milliseconds and random bits.

    UUIDv7 objects feature monotonicity within a millisecond.
    """
    ...

def uuid8(bytes: bytes) -> UUID:
    """Generate a custom UUID comprised almost entirely of user-supplied bytes."""
    ...

NIL: Final[UUID]
MAX: Final[UUID]
__version__: str

__all__ = [
    "MAX",
    "NAMESPACE_DNS",
    "NAMESPACE_OID",
    "NAMESPACE_URL",
    "NAMESPACE_X500",
    "NIL",
    "RESERVED_FUTURE",
    "RESERVED_MICROSOFT",
    "RESERVED_NCS",
    "RFC_4122",
    "UUID",
    "SafeUUID",
    "__version__",
    "getnode",
    "uuid1",
    "uuid3",
    "uuid4",
    "uuid5",
    "uuid6",
    "uuid7",
    "uuid8",
]
