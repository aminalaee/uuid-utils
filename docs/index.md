# Python UUID Utils

<div align="center">

<a href="https://pypi.org/project/uuid-utils/" target="_blank">
    <img src="https://badge.fury.io/py/uuid-utils.svg" alt="Package version">
</a>
<a href="https://pypi.org/project/uuid-utils/" target="_blank">
    <img src="https://img.shields.io/pypi/dm/uuid-utils.svg" alt="Downloads">
</a>
<a href="https://pypi.org/project/uuid-utils" target="_blank">
    <img src="https://img.shields.io/pypi/pyversions/uuid-utils.svg?color=%2334D058" alt="Supported Python versions">
</a>
<a href="https://codspeed.io/aminalaee/uuid-utils?utm_source=badge" target="_blank">
    <img src="https://img.shields.io/endpoint?url=https://codspeed.io/badge.json" alt="Codspeed">
</a>

</div>

---

Fast, drop-in replacement for Python's uuid module, powered by Rust.

Available UUID versions:

- `uuid1` - Version 1 UUIDs using a timestamp and monotonic counter.
- `uuid3` - Version 3 UUIDs based on the MD5 hash of some data.
- `uuid4` - Version 4 UUIDs with random data.
- `uuid5` - Version 5 UUIDs based on the SHA1 hash of some data.
- `uuid6` - Version 6 UUIDs using a timestamp and monotonic counter.
- `uuid7` - Version 7 UUIDs using a Unix timestamp ordered by time.
- `uuid8` - Version 8 UUIDs using user-defined data.

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

## Compatibility with Python UUID

In some cases, for example if you are using `Django`, you might need `UUID` instances to be returned
from the standard-library `uuid`, not a custom `UUID` class.
In that case you can use the `uuid_utils.compat` which comes with a performance penalty
in comparison with the `uuid_utils` default behaviour, but is still faster than the standard-library.

```py
>>> import uuid_utils.compat as uuid

>>> # make a random UUID
>>> uuid.uuid4()
UUID('ffe95fcc-b818-4aca-a350-e0a35b9de6ec')
```

## Benchmarks

| Benchmark              |        Min |     Median |        Max |       × |
| :--------------------- | ---------: | ---------: | ---------: | ------: |
| **uuid4()**            |            |            |            |         |
| stdlib_uuid4           | 1163.498ns | 1214.832ns | 1270.172ns | 22.528x |
| compat_uuid4           |  380.432ns |  382.615ns |  388.044ns |  7.095x |
| uuid_utils_uuid4       |   53.499ns |   53.924ns |   55.577ns |  1.000x |
| **uuid7()**            |            |            |            |         |
| stdlib_uuid7           | 1417.852ns | 1466.774ns | 1706.159ns | 17.417x |
| compat_uuid7           |  461.170ns |  466.757ns |  651.171ns |  5.542x |
| uuid_utils_uuid7       |   83.197ns |   84.216ns |   92.744ns |  1.000x |
| **UUID from hex**      |            |            |            |         |
| stdlib_from_hex        |  416.020ns |  423.380ns |  428.571ns |  5.679x |
| uuid_utils_from_hex    |   73.406ns |   74.549ns |   76.518ns |  1.000x |
| **UUID from bytes**    |            |            |            |         |
| stdlib_from_bytes      |  357.460ns |  362.705ns |  369.997ns |  3.716x |
| uuid_utils_from_bytes  |   97.227ns |   97.603ns |   98.170ns |  1.000x |

*times in nanoseconds, lower is better*

Python 3.14.2 · macOS-26.3.1 · Apple M3 Pro · 10 × 100,000 rounds · 2026-05-08 10:34:14

## How to develop locally

```shell
$ make build
$ make test
```

Or:

```shell
$ maturin develop --release
```
