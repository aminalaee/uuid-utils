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
which implements existing UUID versions like v4 in Rust
and also adds draft UUID versions like v6.

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
Using `pip`:
```shell
$ pip install uuid-utils
```
or, using `conda`:

```shell
$ conda install -c conda-forge uuid-utils
```

## Example

```shell
>>> import uuid_utils as uuid

>>> # make a random UUID
>>> uuid.uuid4()
UUID('ffe95fcc-b818-4aca-a350-e0a35b9de6ec')

>>> # make a random UUID using a Unix timestamp which is time-ordered.
>>> uuid.uuid7()
UUID('018afa4a-0d21-7e6c-b857-012bc678552b')

>>> # make a UUID using a SHA-1 hash of a namespace UUID and a name
>>> uuid.uuid5(uuid.NAMESPACE_DNS, 'python.org')
UUID('886313e1-3b8a-5372-9b90-0c9aee199e5d')

>>> # make a UUID using an MD5 hash of a namespace UUID and a name
>>> uuid.uuid3(uuid.NAMESPACE_DNS, 'python.org')
UUID('6fa459ea-ee8a-3ca4-894e-db77e160355e')
```

## Compatibility

In some cases, for example if you are using `Django`, you might need `UUID` instances to be returned
from the standrad-library `uuid`, not a custom `UUID` class.
In that case you can use the `uuid_utils.compat` which comes with a performance penalty
in comparison with the `uuid_utils` default behaviour, but is still faster than the standard-library.

```py
>>> import uuid_utils.compat as uuid

>>> # make a random UUID
>>> uuid.uuid4()
UUID('ffe95fcc-b818-4aca-a350-e0a35b9de6ec')
```

## Benchmarks

|        Benchmark | Min     | Max     | Mean    | Min (+)         | Max (+)         | Mean (+)        |
|------------------|---------|---------|---------|-----------------|-----------------|-----------------|
|          UUID v1 | 0.061   | 0.299   | 0.194   | 0.019 (3.3x)    | 0.019 (15.4x)   | 0.019 (10.1x)   |
|          UUID v3 | 0.267   | 0.307   | 0.293   | 0.035 (7.6x)    | 0.041 (7.5x)    | 0.039 (7.5x)    |
|          UUID v4 | 0.145   | 0.301   | 0.249   | 0.004 (38.5x)   | 0.005 (54.8x)   | 0.005 (53.0x)   |
|          UUID v5 | 0.058   | 0.189   | 0.146   | 0.008 (7.6x)    | 0.038 (5.0x)    | 0.016 (9.0x)    |
|    UUID from hex | 0.128   | 0.139   | 0.135   | 0.016 (8.2x)    | 0.017 (8.0x)    | 0.016 (8.3x)    |
|  UUID from bytes | 0.031   | 0.135   | 0.093   | 0.016 (2.0x)    | 0.016 (8.6x)    | 0.016 (5.9x)    |
|    UUID from int | 0.027   | 0.102   | 0.043   | 0.003 (8.3x)    | 0.004 (25.0x)   | 0.003 (12.4x)   |
| UUID from fields | 0.031   | 0.162   | 0.077   | 0.005 (6.0x)    | 0.005 (30.6x)   | 0.005 (14.7x)   |

<sup>Benchmark results might vary in different environments, but in most cases the uuid_utils should outperform stdlib uuid.</sup><br>

## How to develop locally

```shell
$ make build
$ make test
```

Or:

```shell
$ RUSTFLAGS="--cfg uuid_unstable" maturin develop --release
```
