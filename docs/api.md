## `class` **`uuid_utils.UUID`**

| Property    | Description                                                                                                                                     |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `bytes`     | The UUID as a 16-byte string (containing the six integer fields in big-endian byte order)                                                       |
| `bytes_le`  | The UUID as a 16-byte string (with time_low, time_mid, and time_hi_version in little-endian byte order)                                         |
| `fields`    | A tuple of the six integer fields of the UUID, which are also available as six individual attributes and two derived attributes                 |
| `hex`       | The UUID as a 32-character hexadecimal string                                                                                                   |
| `int`       | The UUID as a 128-bit integer                                                                                                                   |
| `urn`       | The UUID as a URN as specified in RFC 4122                                                                                                      |
| `variant`   | The UUID variant (one of the constants RESERVED_NCS, RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE).                                         |
| `version`   | The UUID version number                                                                                                                         |
| `is_safe`   | An enum indicating whether the UUID has been generated in a way that is safe for multiprocessing applications, via `uuid_generate_time_safe(3)` |
| `timestamp` | The timestamp of the UUID in milliseconds since epoch. Only works for UUID versions 1, 6 and 7, otherwise raises `ValueError`                   |

## `module` **`uuid_utils`**

| Function  | Description                                                                                                                                                                                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uuid1`   | Generate a UUID from a host ID, sequence number, and the current time. If `node` is not given, `getnode()` is used to obtain the hardware address.  If `clock_seq` is given, it is used as the sequence number; otherwise a random 14-bit sequence number is chosen. |
| `uuid3`   | Generate a UUID from the MD5 hash of a namespace UUID and a name.                                                                                                                                                                                                    |
| `uuid4`   | Generate a random UUID.                                                                                                                                                                                                                                              |
| `uuid5`   | Generate a UUID from the SHA-1 hash of a namespace UUID and a name.                                                                                                                                                                                                  |
| `uuid6`   | Similar to `uuid1` but where fields are ordered differently for improved DB locality.                                                                                                                                                                                |
| `uuid7`   | Generate a UUID from a Unix timestamp in milliseconds and random bits.                                                                                                                                                                                               |
| `uuid8`   | Generate a UUID from three custom blocks.                                                                                                                                                                                                                            |
| `getnode` | Get the hardware address as a 48-bit positive integer.                                                                                                                                                                                                               |
| `NIL`     | The nil UUID with all 128 bits set to zero.                                                                                                                                                                                                                          |
| `MAX`     | The max UUID with all 128 bits set to one.                                                                                                                                                                                                                           |

### `function` **`uuid1(node: int = None, clock_seq: int = None)`**
Generate a UUID from a host ID, sequence number, and the current time. If `node` is not given, `getnode()` is used to obtain the hardware address.  If `clock_seq` is given, it is used as the sequence number; otherwise a random 14-bit sequence number is chosen.

| Parameter   | Type  | Description                                                                                |
| ----------- | ----- | ------------------------------------------------------------------------------------------ |
| `node`      | `int` | Defines the host ID. If undefined, host ID will be derived from the result of `getnode()`. |
| `clock_seq` | `int` | Defines the sequence number. If undefined, a random 14-bit number sequence will be used.   |

### `function` **`uuid3(namespace: UUID, name: str | bytes)`**
Generate a UUID from the MD5 hash of a namespace UUID and a name.

| Parameter   | Type          | Description                                                         |
| ----------- | ------------- | ------------------------------------------------------------------- |
| `namespace` | `UUID`        | Defines the UUID to be hashed.                                      |
| `name`      | `str` `bytes` | A bytes or string object. No upper limit on bytes or string length. |

### `function` `uuid4()`
Generate a random UUID.

### `function` `uuid5(namespace: UUID, name: str | bytes)`
Generate a UUID from the SHA-1 hash of a namespace UUID and a name.

| Parameter   | Type          | Description                                                         |
| ----------- | ------------- | ------------------------------------------------------------------- |
| `namespace` | `UUID`        | Defines the UUID to be hashed.                                      |
| `name`      | `str` `bytes` | A bytes or string object. No upper limit on bytes or string length. |

### `function` `uuid6(node: int = None, clock_seq: int = None)`
Similar to `uuid1` but where fields are ordered differently for improved DB locality.

More precisely, given a 60-bit timestamp value as specified for UUIDv1, for UUIDv6 the first 48 most significant bits are stored first, followed by the 4-bit version (same position), followed by the remaining 12 bits of the original 60-bit timestamp.

| Parameter   | Type  | Description                                                                                |
| ----------- | ----- | ------------------------------------------------------------------------------------------ |
| `node`      | `int` | Defines the host ID. If undefined, host ID will be derived from the result of `getnode()`. |
| `clock_seq` | `int` | Defines the 14-bit clock sequence. If undefined, a random value is used.                   |

### `function` **`uuid7()`**
Generate a UUID from a Unix timestamp in milliseconds and random bits.

UUIDv7 objects feature monotonicity within a millisecond.

### `function` **`uuid8(a: int = None, b: int = None, c: int = None)`**
Generate a UUID from three custom blocks.

* `a` is the first 48-bit chunk of the UUID (octets 0-5);
* `b` is the mid 12-bit chunk (octets 6-7);
* `c` is the last 62-bit chunk (octets 8-15).

When a value is not specified, a pseudo-random value is generated.
