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

Some frameworks (e.g. Django) require `UUID` instances from the standard-library `uuid` module,
not a custom subclass. Use `uuid_utils.compat` for a drop-in replacement that returns stdlib
`uuid.UUID` instances while still outperforming the standard library.

```py
>>> import uuid_utils.compat as uuid

>>> uuid.uuid4()
UUID('ffe95fcc-b818-4aca-a350-e0a35b9de6ec')
```

## Benchmarks

| Benchmark             |    Min     |   Median   |    Max     |    ×    |
| :-------------------- | :--------: | :--------: | :--------: | :-----: |
| **uuid4()**           |            |            |            |         |
| stdlib_uuid4          | 1207.988ns | 1245.685ns | 1858.940ns | 21.916x |
| compat_uuid4          |  394.893ns |  402.400ns |  428.825ns |  7.080x |
| uuid_utils_uuid4      |   55.966ns |   56.839ns |   58.002ns |  1.000x |
| **uuid7()**           |            |            |            |         |
| stdlib_uuid7          | 1374.710ns | 1389.047ns | 1424.699ns | 16.680x |
| compat_uuid7          |  414.879ns |  430.362ns |  507.907ns |  5.168x |
| uuid_utils_uuid7      |   82.275ns |   83.277ns |   84.009ns |  1.000x |
| **UUID from hex**     |            |            |            |         |
| stdlib_from_hex       |  407.829ns |  421.818ns |  698.335ns |  5.282x |
| uuid_utils_from_hex   |   76.947ns |   79.863ns |   84.505ns |  1.000x |
| **UUID from bytes**   |            |            |            |         |
| stdlib_from_bytes     |  370.876ns |  393.131ns |  559.383ns |  3.888x |
| uuid_utils_from_bytes |   98.012ns |  101.120ns |  106.267ns |  1.000x |

*times in nanoseconds, lower is better*

Python 3.14.2 · macOS-26.3.1 · Apple M3 Pro · 10 × 100,000 rounds · 2026-05-08 11:24:30

## How to develop locally

```shell
$ make build
$ make test
```

Or:

```shell
$ maturin develop --release
```
