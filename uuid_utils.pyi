import sys
from enum import Enum

from _typeshed import Unused
from typing_extensions import TypeAlias

# Because UUID has properties called int and bytes we need to rename these temporarily.
_Int: TypeAlias = int
_Bytes: TypeAlias = bytes
_FieldsType: TypeAlias = tuple[int, int, int, int, int, int]

class SafeUUID(Enum):
    safe: int
    unsafe: int
    unknown: None

class UUID:
    r"""Create a UUID from either a string of 32 hexadecimal digits,
        a string of 16 bytes as the 'bytes' argument, a string of 16 bytes
        in little-endian order as the 'bytes_le' argument, a tuple of six
        integers (32-bit time_low, 16-bit time_mid, 16-bit time_hi_version,
        8-bit clock_seq_hi_variant, 8-bit clock_seq_low, 48-bit node) as
        the 'fields' argument, or a single 128-bit integer as the 'int'
        argument.  When a string of hex digits is given, curly braces,
        hyphens, and a URN prefix are all optional.  For example, these
        expressions all yield the same UUID:
        UUID('{12345678-1234-5678-1234-567812345678}')
        UUID('12345678123456781234567812345678')
        UUID('urn:uuid:12345678-1234-5678-1234-567812345678')
        UUID(bytes='\x12\x34\x56\x78'*4)
        UUID(bytes_le='\x78\x56\x34\x12\x34\x12\x78\x56' +
                      '\x12\x34\x56\x78\x12\x34\x56\x78')
        UUID(fields=(0x12345678, 0x1234, 0x5678, 0x12, 0x34, 0x567812345678))
        UUID(int=0x12345678123456781234567812345678)
        Exactly one of 'hex', 'bytes', 'bytes_le', 'fields', or 'int' must
        be given.  The 'version' argument is optional; if given, the resulting
        UUID will have its variant and version set according to RFC 4122,
        overriding the given 'hex', 'bytes', 'bytes_le', 'fields', or 'int'.
        is_safe is an enum exposed as an attribute on the instance.  It
        indicates whether the UUID has been generated in a way that is safe
        for multiprocessing applications, via uuid_generate_time_safe(3).
        """

    def __init__(
        self,
        hex: str | None = None,
        bytes: _Bytes | None = None,
        bytes_le: _Bytes | None = None,
        fields: _FieldsType | None = None,
        int: _Int | None = None,
        version: _Int | None = None,
        *,
        is_safe: SafeUUID = ...,
    ) -> None: ...
    @property
    def is_safe(self) -> SafeUUID: ...
    @property
    def bytes(self) -> _Bytes: ...
    @property
    def bytes_le(self) -> _Bytes: ...
    @property
    def clock_seq(self) -> _Int: ...
    @property
    def clock_seq_hi_variant(self) -> _Int: ...
    @property
    def clock_seq_low(self) -> _Int: ...
    @property
    def fields(self) -> _FieldsType: ...
    @property
    def hex(self) -> str: ...
    @property
    def int(self) -> _Int: ...
    @property
    def node(self) -> _Int: ...
    @property
    def time(self) -> _Int: ...
    @property
    def time_hi_version(self) -> _Int: ...
    @property
    def time_low(self) -> _Int: ...
    @property
    def time_mid(self) -> _Int: ...
    @property
    def urn(self) -> str: ...
    @property
    def variant(self) -> str: ...
    @property
    def version(self) -> _Int | None: ...
    def __int__(self) -> _Int: ...
    def __eq__(self, other: object) -> bool: ...
    def __lt__(self, other: UUID) -> bool: ...
    def __le__(self, other: UUID) -> bool: ...
    def __gt__(self, other: UUID) -> bool: ...
    def __ge__(self, other: UUID) -> bool: ...

if sys.version_info >= (3, 9):
    def getnode() -> int: ...

else:
    def getnode(*, getters: Unused = None) -> int: ...  # undocumented

def uuid1(node: _Int, clock_seq: _Int | None = None) -> UUID:
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

def uuid6(node: _Int, timestamp: _Int | None = None) -> UUID:
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

NAMESPACE_DNS: UUID
NAMESPACE_URL: UUID
NAMESPACE_OID: UUID
NAMESPACE_X500: UUID
