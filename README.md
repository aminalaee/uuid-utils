# Python UUID Utils

<p align="center">
<a href="https://pypi.org/project/uuid-utils/">
    <img src="https://badge.fury.io/py/uuid-utils.svg" alt="Package version">
</a>
<a href="https://pypi.org/project/uuid-utils" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/uuid-utils.svg?color=%2334D058" alt="Supported Python versions">
</a>
</p>

---

Python UUID implementation using Rust's UUID library.
This will make `uuid4` function around 10x faster.

This package can be a drop-in replacement to the standard library UUID
which implements existing UUID versions like V4 in Rust
and also adds draft UUID versions like V6.

Avaialble UUID versions:

- `uuid1` - Version 1 UUIDs using a timestamp and monotonic counter.
- `uuid3` - Version 3 UUIDs based on the MD5 hash of some data.
- `uuid4` - Version 4 UUIDs with random data.
- `uuid5` - Version 5 UUIDs based on the SHA1 hash of some data.
- `uuid6` - Version 6 UUIDs using a timestamp and monotonic counter.
- `uuid7` - Version 7 UUIDs using a Unix timestamp ordered by time.
- `uuid8` - Version 8 UUIDs using user-defined data.

<sup>Please note that UUID versions 6, 7 and 8 are still in draft RFC.</sup><br>

## Installation

```shell
$ pip install uuid-utils
```

## Example

```shell
>>> import uuid_utils as uuid

>>> # make a random UUID
>>> uuid.uuid4()
UUID('ffe95fcc-b818-4aca-a350-e0a35b9de6ec')

>>> # make a random UUID using a Unix timestamp which is time-ordered.
>>> uuid.uuid7()
UUID('16ada4b8-b7b1-4e6c-b857-012bc678552b')

>>> # make a UUID using a SHA-1 hash of a namespace UUID and a name
>>> uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

>>> # make a UUID using an MD5 hash of a namespace UUID and a name
>>> uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')
```

## Benchmarks

|       Benchmark | Min     | Max     | Mean    | Min (+)         | Max (+)         | Mean (+)        |
|-----------------|---------|---------|---------|-----------------|-----------------|-----------------|
|         UUID V1 | 0.058   | 0.059   | 0.058   | 0.005 (12.0x)   | 0.005 (11.9x)   | 0.005 (12.0x)   |
|         UUID V4 | 0.041   | 0.041   | 0.041   | 0.004 (11.1x)   | 0.004 (10.8x)   | 0.004 (10.9x)   |
|         UUID V5 | 0.064   | 0.066   | 0.065   | 0.008 (8.1x)    | 0.008 (8.1x)    | 0.008 (8.1x)    |
|   UUID from hex | 0.024   | 0.025   | 0.024   | 0.004 (6.7x)    | 0.004 (6.6x)    | 0.004 (6.6x)    |
| UUID from bytes | 0.024   | 0.025   | 0.024   | 0.004 (6.7x)    | 0.004 (6.6x)    | 0.004 (6.7x)    |
|   UUID from int | 0.024   | 0.025   | 0.024   | 0.004 (6.6x)    | 0.004 (6.7x)    | 0.004 (6.6x)    |

## Limitations

- The `getnode` function is not available.
- The `uuid1` and `uuid6` take `node` argument as mandatory.
- The `uuid3` function is not available.
