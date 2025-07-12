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
| `uuid6`   | Generate a version 6 UUID using the given timestamp and a host ID. This is similar to version 1 UUIDs, except that it is lexicographically sortable by timestamp.                                                                                                    |
| `uuid7`   | Generate a version 7 UUID using a time value and random bytes.                                                                                                                                                                                                       |
| `uuid8`   | Generate a custom UUID comprised almost entirely of user-supplied bytes.                                                                                                                                                                                             |
| `getnode` | Get the hardware address as a 48-bit positive integer.                                                                                                                                                                                                               |

### `function` **`uuid1(node: int = None, clock_seq: int = None)`**
Port of `uuid.uuid1()`. Generates a UUID from a host ID, sequence number, and the current time. Superceded by `uuid6()`.

| Parameter   | Type  | Description                                                                                |
| ----------- | ----- | ------------------------------------------------------------------------------------------ |
| `node`      | `int` | Defines the host ID. If undefined, host ID will be derived from the result of `getnode()`. |
| `clock_seq` | `int` | Defines the sequence number. If undefined, a random 14-bit number sequence will be used.   |

### `function` **`uuid3(namespace: UUID, name: str | bytes)`**
Port of `uuid.uuid3()`. Generates a UUID from the MD5 hash of a namespace UUID, and a name. Superceded by `uuid5()`. Both parameters must be met.

| Parameter   | Type          | Description                                                         |
| ----------- | ------------- | ------------------------------------------------------------------- |
| `namespace` | `UUID`        | Defines the UUID to be hashed.                                      |
| `name`      | `str` `bytes` | A bytes or string object. No upper limit on bytes or string length. |

### `function` `uuid4()`
Port of `uuid.uuid4()`. Generates an entirely random UUID.

### `function` `uuid5(namespace: UUID, name: str | bytes)`
Port of `uuid.uuid5()`. Generates a UUID from the SHA-1 hash of a namespace UUID, and a name. Supercedes `uuid3()`. Both parameters must be met.

| Parameter   | Type          | Description                                                         |
| ----------- | ------------- | ------------------------------------------------------------------- |
| `namespace` | `UUID`        | Defines the UUID to be hashed.                                      |
| `name`      | `str` `bytes` | A bytes or string object. No upper limit on bytes or string length. |

### `function` `uuid6(node: int = None, timestamp: int = None, nanos: int = None)`
Generates a lexicographically sortable UUID from a host ID, and a timestamp. Supercedes `uuid1()`.

| Parameter   | Type  | Description                                                                                                                             |
| ----------- | ----- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `node`      | `int` | Defines the host ID. If undefined, host ID will be derived from the result of `getnode()`.                                              |
| `timestamp` | `int` | A 10-digit integer defining the seconds elapsed since the UNIX epoch. If undefined, this will be derived from the system clock.         |
| `nanos`     | `int` | A 10-digit integer defining the sub-seconds elapsed since the UNIX epoch. If undefined, this will be derived from the system clock.     |

### `function` **`uuid7(timestamp: int = None, nanos: int = None)`**
Generates a lexicographically sortable random UUID from a timestamp.

| Parameter      | Type  | Description                                                                                                                          |
| -------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `timestamp`    | `int` | A 10-digit integer defining the seconds elapsed since the UNIX epoch. If undefined, this will be derived from the system clock.      |
| `nanos`        | `int` | A 10-digit integer defining the sub-seconds elapsed since the UNIX epoch. If undefined, this will be derived from the system clock.  |

### `function` **`uuid8(bytes: bytes)`**
Generates a UUID of a custom format from user-supplied bytes which may or may not be compliant to any specification.

| Parameter | Type    | Description                                                         |
| --------- | ------- | ------------------------------------------------------------------- |
| `bytes`   | `bytes` | 16 bytes corresponding to the 48, 12, and 62 bit segments of a UUID |
