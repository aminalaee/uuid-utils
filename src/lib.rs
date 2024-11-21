use mac_address::get_mac_address;
use pyo3::{
    exceptions::{PyTypeError, PyValueError},
    ffi,
    prelude::*,
    pyclass::CompareOp,
    types::{PyBytes, PyDict},
};
use rand::RngCore;
use std::{collections::hash_map::DefaultHasher, hash::Hash};
use std::{hash::Hasher, sync::atomic::AtomicPtr};
use std::{
    ptr::null_mut,
    sync::atomic::{AtomicU64, Ordering},
};
use uuid::{Builder, Bytes, Context, Timestamp, Uuid, Variant, Version};

static NODE: AtomicU64 = AtomicU64::new(0);

pub const RESERVED_NCS: &str = "reserved for NCS compatibility";
pub const RFC_4122: &str = "specified in RFC 4122";
pub const RESERVED_MICROSOFT: &str = "reserved for Microsoft compatibility";
pub const RESERVED_FUTURE: &str = "reserved for future definition";

#[derive(FromPyObject)]
enum StringOrBytes {
    #[pyo3(transparent, annotation = "str")]
    String(String),
    #[pyo3(transparent, annotation = "bytes")]
    Bytes(Vec<u8>),
}

#[pyclass(subclass, module = "uuid_utils")]
#[derive(Clone, Debug)]
struct UUID {
    uuid: Uuid,
}

#[pymethods]
impl UUID {
    pub const NAMESPACE_DNS: UUID = UUID {
        uuid: Uuid::NAMESPACE_DNS,
    };
    pub const NAMESPACE_URL: UUID = UUID {
        uuid: Uuid::NAMESPACE_URL,
    };
    pub const NAMESPACE_OID: UUID = UUID {
        uuid: Uuid::NAMESPACE_OID,
    };
    pub const NAMESPACE_X500: UUID = UUID {
        uuid: Uuid::NAMESPACE_X500,
    };

    #[new]
    #[pyo3(signature = (hex=None, bytes=None, bytes_le=None, fields=None, int=None, version=None))]
    fn new(
        hex: Option<&str>,
        bytes: Option<&Bound<'_, PyBytes>>,
        bytes_le: Option<&Bound<'_, PyBytes>>,
        fields: Option<(u32, u16, u16, u8, u8, u64)>,
        int: Option<u128>,
        version: Option<u8>,
    ) -> PyResult<Self> {
        let result = match (hex, bytes, bytes_le, fields, int) {
            (Some(hex), None, None, None, None) => Self::from_hex(hex),
            (None, Some(bytes), None, None, None) => Self::from_bytes(bytes),
            (None, None, Some(bytes_le), None, None) => Self::from_bytes_le(bytes_le),
            (None, None, None, Some(fields), None) => Self::from_fields(fields),
            (None, None, None, None, Some(int)) => Self::from_int(int),
            _ => Err(PyTypeError::new_err(
                "one of the hex, bytes, bytes_le, fields, or int arguments must be given",
            )),
        };

        match version {
            Some(v) => result.unwrap().set_version(v),
            None => result,
        }
    }

    fn __int__(&self) -> u128 {
        self.uuid.as_u128()
    }

    fn __str__(&self) -> String {
        self.uuid.hyphenated().to_string()
    }

    fn __repr__(&self) -> String {
        format!("UUID('{}')", self.__str__())
    }

    fn __richcmp__(&self, other: UUID, op: CompareOp) -> PyResult<bool> {
        match op {
            CompareOp::Lt => Ok(self.uuid < other.uuid),
            CompareOp::Le => Ok(self.uuid <= other.uuid),
            CompareOp::Eq => Ok(self.uuid == other.uuid),
            CompareOp::Ne => Ok(self.uuid != other.uuid),
            CompareOp::Gt => Ok(self.uuid > other.uuid),
            CompareOp::Ge => Ok(self.uuid >= other.uuid),
        }
    }

    fn __hash__(&self) -> PyResult<isize> {
        let mut hasher = DefaultHasher::new();
        self.uuid.hash(&mut hasher);
        Ok(hasher.finish() as isize)
    }

    fn set_version(&self, version: u8) -> PyResult<UUID> {
        let version = match version {
            1 => Version::Mac,
            2 => Version::Dce,
            3 => Version::Md5,
            4 => Version::Random,
            5 => Version::Sha1,
            6 => Version::SortMac,
            7 => Version::SortRand,
            8 => Version::Custom,
            _ => return Err(PyErr::new::<PyValueError, &str>("illegal version number.")),
        };

        let mut builder = Builder::from_u128(self.uuid.as_u128());
        builder.set_version(version);

        Ok(UUID {
            uuid: builder.into_uuid(),
        })
    }

    #[allow(unused_variables)]
    fn __setattr__(&self, name: &str, value: PyObject) -> PyResult<()> {
        Err(PyTypeError::new_err("UUID objects are immutable"))
    }

    fn __getnewargs__(&self) -> (String,) {
        (self.__str__(),)
    }

    pub fn __deepcopy__(&self, py: Python, _memo: &Bound<'_, PyDict>) -> Py<PyAny> {
        self.clone().into_pyobject(py).unwrap().into_any().unbind()
    }

    #[getter]
    fn hex(&self) -> PyResult<String> {
        Ok(self.uuid.simple().to_string())
    }

    #[getter]
    fn bytes(&self) -> &[u8] {
        self.uuid.as_bytes()
    }

    #[getter]
    fn bytes_le<'py>(&self, py: Python<'py>) -> Bound<'py, PyBytes> {
        let bytes = *self.uuid.as_bytes();
        let bytes = [
            bytes[3], bytes[2], bytes[1], bytes[0], bytes[5], bytes[4], bytes[7], bytes[6],
            bytes[8], bytes[9], bytes[10], bytes[11], bytes[12], bytes[13], bytes[14], bytes[15],
        ];
        PyBytes::new(py, &bytes)
    }

    #[getter]
    fn int(&self) -> u128 {
        self.uuid.as_u128()
    }

    #[getter]
    fn urn(&self) -> PyResult<String> {
        Ok(self.uuid.urn().to_string())
    }

    #[getter]
    fn version(&self) -> usize {
        self.uuid.get_version_num()
    }

    #[getter]
    fn variant(&self) -> &str {
        match self.uuid.get_variant() {
            Variant::NCS => RESERVED_NCS,
            Variant::RFC4122 => RFC_4122,
            Variant::Microsoft => RESERVED_MICROSOFT,
            Variant::Future => RESERVED_FUTURE,
            _ => RESERVED_FUTURE,
        }
    }

    #[getter]
    fn node(&self) -> u64 {
        (self.int() & 0xffffffffffff) as u64
    }

    #[getter]
    fn time_low(&self) -> u32 {
        self.int().wrapping_shr(96) as u32
    }

    #[getter]
    fn time_mid(&self) -> u16 {
        ((self.int().wrapping_shr(80)) & 0xffff) as u16
    }

    #[getter]
    fn time_hi_version(&self) -> u16 {
        ((self.int().wrapping_shr(64)) & 0xffff) as u16
    }

    #[getter]
    fn clock_seq_hi_variant(&self) -> u8 {
        ((self.int().wrapping_shr(56)) & 0xff) as u8
    }

    #[getter]
    fn clock_seq_low(&self) -> u8 {
        ((self.int().wrapping_shr(48)) & 0xff) as u8
    }

    #[getter]
    fn clock_seq(&self) -> u16 {
        let high = (self.clock_seq_hi_variant()) as u16 & 0x3f;
        high.wrapping_shl(8) | self.clock_seq_low() as u16
    }

    #[getter]
    fn time(&self) -> u64 {
        let high = self.time_hi_version() as u64 & 0x0fff;
        let mid = (self.time_mid()) as u64;
        high.wrapping_shl(48) | mid.wrapping_shl(32) | self.time_low() as u64
    }

    #[getter]
    fn timestamp(&self) -> PyResult<u64> {
        match self.uuid.get_timestamp() {
            Some(timestamp) => {
                let (secs, nanos) = timestamp.to_unix();
                Ok(secs * 1_000 + nanos as u64 / 1_000 / 1_000)
            }
            _ => {
                return Err(PyErr::new::<PyValueError, &str>(
                    "UUID version should be one of (v1, v6 or v7).",
                ))
            }
        }
    }

    #[getter]
    fn fields(&self) -> PyResult<(u32, u16, u16, u8, u8, u64)> {
        Ok((
            self.time_low(),
            self.time_mid(),
            self.time_hi_version(),
            self.clock_seq_hi_variant(),
            self.clock_seq_low(),
            self.node(),
        ))
    }

    #[staticmethod]
    fn from_hex(hex: &str) -> PyResult<UUID> {
        match Uuid::parse_str(hex) {
            Ok(uuid) => Ok(UUID { uuid }),
            _ => Err(PyValueError::new_err(
                "badly formed hexadecimal UUID string",
            )),
        }
    }

    #[staticmethod]
    fn from_bytes(bytes: &Bound<'_, PyBytes>) -> PyResult<UUID> {
        let bytes: Bytes = bytes.extract()?;
        Ok(UUID {
            uuid: Uuid::from_bytes(bytes),
        })
    }

    #[staticmethod]
    fn from_bytes_le(bytes: &Bound<'_, PyBytes>) -> PyResult<UUID> {
        let bytes: Bytes = bytes.extract()?;
        Ok(UUID {
            uuid: Uuid::from_bytes_le(bytes),
        })
    }

    #[staticmethod]
    fn from_fields(fields: (u32, u16, u16, u8, u8, u64)) -> PyResult<UUID> {
        let time_low = fields.0 as u128;
        let time_mid = fields.1 as u128;
        let time_hi_version = fields.2 as u128;
        let clock_seq_hi_variant = fields.3 as u128;
        let clock_seq_low = fields.4 as u128;
        let node = fields.5 as u128;
        let clock_seq = clock_seq_hi_variant.wrapping_shl(8) | clock_seq_low;

        let value = time_low.wrapping_shl(96)
            | time_mid.wrapping_shl(80)
            | time_hi_version.wrapping_shl(64)
            | clock_seq.wrapping_shl(48)
            | node;

        Ok(UUID {
            uuid: Uuid::from_u128(value),
        })
    }

    #[staticmethod]
    fn from_int(int: u128) -> PyResult<UUID> {
        Ok(UUID {
            uuid: Uuid::from_u128(int),
        })
    }

    #[getter]
    fn is_safe(&self) -> *mut ffi::PyObject {
        return SAFE_UUID_UNKNOWN.load(Ordering::Relaxed);
    }
}

#[pyfunction]
#[pyo3(signature = (node=None, clock_seq=None))]
fn uuid1(node: Option<u64>, clock_seq: Option<u64>) -> PyResult<UUID> {
    let node = match node {
        Some(node) => node.to_ne_bytes(),
        None => _getnode().to_ne_bytes(),
    };
    let node = &[node[0], node[1], node[2], node[3], node[4], node[5]];
    let uuid = match clock_seq {
        Some(clock_seq) => {
            let ts = Timestamp::from_unix(&Context::new_random(), clock_seq, 0);
            Uuid::new_v1(ts, node)
        }
        None => Uuid::now_v1(node),
    };
    Ok(UUID { uuid })
}

#[pyfunction]
fn uuid3(namespace: UUID, name: StringOrBytes) -> PyResult<UUID> {
    match name {
        StringOrBytes::String(name) => Ok(UUID {
            uuid: Uuid::new_v3(&namespace.uuid, name.as_bytes()),
        }),
        StringOrBytes::Bytes(name) => Ok(UUID {
            uuid: Uuid::new_v3(&namespace.uuid, &name),
        }),
    }
}

#[pyfunction]
fn uuid4() -> PyResult<UUID> {
    Ok(UUID {
        uuid: Uuid::new_v4(),
    })
}

#[pyfunction]
fn uuid5(namespace: &UUID, name: StringOrBytes) -> PyResult<UUID> {
    match name {
        StringOrBytes::String(name) => Ok(UUID {
            uuid: Uuid::new_v5(&namespace.uuid, name.as_bytes()),
        }),
        StringOrBytes::Bytes(name) => Ok(UUID {
            uuid: Uuid::new_v5(&namespace.uuid, &name),
        }),
    }
}

#[pyfunction]
#[pyo3(signature = (node=None, timestamp=None, nanos=None))]
fn uuid6(node: Option<u64>, timestamp: Option<u64>, nanos: Option<u32>) -> PyResult<UUID> {
    let node = match node {
        Some(node) => node.to_ne_bytes(),
        None => _getnode().to_ne_bytes(),
    };
    let node = &[node[0], node[1], node[2], node[3], node[4], node[5]];

    let uuid = match timestamp {
        Some(timestamp) => {
            let timestamp =
                Timestamp::from_unix(&Context::new_random(), timestamp, nanos.unwrap_or(0));
            return Ok(UUID {
                uuid: Uuid::new_v6(timestamp, node),
            });
        }
        None => Uuid::now_v6(node),
    };
    Ok(UUID { uuid })
}

#[pyfunction]
#[pyo3(signature = (timestamp=None, nanos=None))]
fn uuid7(timestamp: Option<u64>, nanos: Option<u32>) -> PyResult<UUID> {
    let uuid = match timestamp {
        Some(timestamp) => {
            let timestamp =
                Timestamp::from_unix(&Context::new_random(), timestamp, nanos.unwrap_or(0));
            return Ok(UUID {
                uuid: Uuid::new_v7(timestamp),
            });
        }
        None => Uuid::now_v7(),
    };
    Ok(UUID { uuid })
}

#[pyfunction]
fn uuid8(bytes: &Bound<'_, PyBytes>) -> PyResult<UUID> {
    let bytes: Bytes = bytes.extract()?;
    Ok(UUID {
        uuid: Uuid::new_v8(bytes),
    })
}

fn _getnode() -> u64 {
    let cached_node = NODE.load(Ordering::Relaxed);
    if cached_node != 0 {
        return cached_node;
    }
    let bytes = match get_mac_address() {
        Ok(Some(mac_address)) => mac_address.bytes(),
        _ => {
            let mut bytes = [0u8; 6];
            rand::thread_rng().fill_bytes(&mut bytes);
            bytes[0] = bytes[0] | 0x01;
            bytes
        }
    };

    let node = ((bytes[0] as u64).wrapping_shl(40))
        + ((bytes[1] as u64).wrapping_shl(32))
        + ((bytes[2] as u64).wrapping_shl(24))
        + ((bytes[3] as u64).wrapping_shl(16))
        + ((bytes[4] as u64).wrapping_shl(8))
        + (bytes[5] as u64);

    NODE.store(node, Ordering::Relaxed);
    node
}

// ptr to python stdlib uuid.SafeUUID.unknown
static SAFE_UUID_UNKNOWN: AtomicPtr<ffi::PyObject> = AtomicPtr::new(null_mut());

#[pyfunction]
fn getnode() -> PyResult<u64> {
    Ok(_getnode())
}

#[pymodule]
fn _uuid_utils(m: &Bound<'_, PyModule>) -> PyResult<()> {
    let safe_uuid_unknown = Python::with_gil(|py| {
        return PyModule::import(py, "uuid")
            .unwrap()
            .getattr("SafeUUID")
            .unwrap()
            .getattr("unknown")
            .unwrap()
            .unbind();
    });

    SAFE_UUID_UNKNOWN.store(safe_uuid_unknown.into_ptr(), Ordering::Relaxed);

    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_class::<UUID>()?;
    m.add_function(wrap_pyfunction!(uuid1, m)?)?;
    m.add_function(wrap_pyfunction!(uuid3, m)?)?;
    m.add_function(wrap_pyfunction!(uuid4, m)?)?;
    m.add_function(wrap_pyfunction!(uuid5, m)?)?;
    m.add_function(wrap_pyfunction!(uuid6, m)?)?;
    m.add_function(wrap_pyfunction!(uuid7, m)?)?;
    m.add_function(wrap_pyfunction!(uuid8, m)?)?;
    m.add_function(wrap_pyfunction!(getnode, m)?)?;
    m.add("NAMESPACE_DNS", UUID::NAMESPACE_DNS)?;
    m.add("NAMESPACE_URL", UUID::NAMESPACE_URL)?;
    m.add("NAMESPACE_OID", UUID::NAMESPACE_OID)?;
    m.add("NAMESPACE_X500", UUID::NAMESPACE_X500)?;
    m.add("RESERVED_NCS", RESERVED_NCS)?;
    m.add("RFC_4122", RFC_4122)?;
    m.add("RESERVED_MICROSOFT", RESERVED_MICROSOFT)?;
    m.add("RESERVED_FUTURE", RESERVED_FUTURE)?;
    Ok(())
}
