from uuid import UUID

from typing_extensions import TypeAlias

# Because UUID has properties called int and bytes we need to rename these temporarily.
_Int: TypeAlias = int
_Bytes: TypeAlias = bytes

def uuid1(node: _Int | None = None, clock_seq: _Int | None = None) -> UUID:
    """Generate a UUID from a host ID, sequence number, and the current time.
    If 'node' is not given, getnode() is used to obtain the hardware
    address.  If 'clock_seq' is given, it is used as the sequence number;
    otherwise a random 14-bit sequence number is chosen."""
    ...

def uuid3(namespace: UUID, name: str) -> UUID:
    """Generate a UUID from the MD5 hash of a namespace UUID and a name."""
    ...

def uuid4() -> UUID:
    """Generate a random UUID."""
    ...

def uuid5(namespace: UUID, name: str) -> UUID:
    """Generate a UUID from the SHA-1 hash of a namespace UUID and a name."""
    ...

def uuid6(node: _Int | None = None, timestamp: _Int | None = None) -> UUID:
    """Generate a version 6 UUID using the given timestamp and a host ID.
    This is similar to version 1 UUIDs,
    except that it is lexicographically sortable by timestamp.
    """
    ...

def uuid7(timestamp: _Int | None = None) -> UUID:
    """Generate a version 7 UUID using a time value and random bytes."""
    ...

def uuid8(bytes: _Bytes) -> UUID:
    """Generate a custom UUID comprised almost entirely of user-supplied bytes.."""
    ...
