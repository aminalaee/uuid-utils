class `uuid_utils.UUID`

| Property    | Description                                                                                                                                     |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `bytes`     | the UUID as a 16-byte string (containing the six integer fields in big-endian byte order)                                                       |
| `bytes_le`  | the UUID as a 16-byte string (with time_low, time_mid, and time_hi_version in little-endian byte order)                                         |
| `fields`    | a tuple of the six integer fields of the UUID, which are also available as six individual attributes and two derived attributes                 |
| `hex`       | the UUID as a 32-character hexadecimal string                                                                                                   |
| `int`       | the UUID as a 128-bit integer                                                                                                                   |
| `urn`       | the UUID as a URN as specified in RFC 4122                                                                                                      |
| `variant`   | the UUID variant (one of the constants RESERVED_NCS, RFC_4122, RESERVED_MICROSOFT, or RESERVED_FUTURE)                                          |
| `version`   | the UUID version number                                                                                                                         |
| `is_safe`   | An enum indicating whether the UUID has been generated in a way that is safe for multiprocessing applications, via `uuid_generate_time_safe(3)` |
| `timestamp` | The timestamp of the UUID in milliseconds since epoch. Only works for UUID versions 1, 6 and 7, otherwise raises `ValueError`.                  |

module `uuid_utils`

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