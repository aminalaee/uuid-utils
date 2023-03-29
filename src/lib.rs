use pyo3::{
    exceptions::{PyTypeError, PyValueError},
    prelude::*,
    pyclass::CompareOp,
    types::{PyBytes, PyTuple},
};
use std::hash::Hasher;
use std::{collections::hash_map::DefaultHasher, hash::Hash};
use uuid::{Builder, Bytes, Context, Timestamp, Uuid, Variant, Version};

pub const RESERVED_NCS: &str = "reserved for NCS compatibility";
pub const RFC_4122: &str = "specified in RFC 4122";
pub const RESERVED_MICROSOFT: &str = "reserved for Microsoft compatibility";
pub const RESERVED_FUTURE: &str = "reserved for future definition";

#[pyclass(subclass, module="uuid_utils")]
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
    fn new(
        hex: Option<&str>,
        bytes: Option<&PyBytes>,
        bytes_le: Option<&PyBytes>,
        fields: Option<&PyTuple>,
        int: Option<u128>,
        version: Option<u8>,
    ) -> PyResult<Self> {
        let result = match (hex, bytes, bytes_le, fields, int) {
            (Some(hex), None, None, None, None) => Self::from_hex(hex),
            (None, Some(bytes), None, None, None) => Self::from_bytes(bytes),
            (None, None, Some(bytes_le), None, None) => Self::from_bytes_le(bytes_le),
            // (None, None, None, Some(fields), None) => Self::from_fields(fields),
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

    #[getter]
    fn hex(&self) -> PyResult<String> {
        Ok(self.uuid.simple().to_string())
    }

    #[getter]
    fn bytes(&self) -> &[u8] {
        self.uuid.as_bytes()
    }

    #[getter]
    fn bytes_le<'py>(&self, py: Python<'py>) -> &'py PyBytes {
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
    fn node(&self) -> u128 {
        self.int() & 0xffffffffffff
    }

    #[getter]
    fn time_low(&self) -> u128 {
        self.int().wrapping_shr(96)
    }

    #[getter]
    fn time_mid(&self) -> u128 {
        (self.int().wrapping_shr(80)) & 0xffff
    }

    #[getter]
    fn time_hi_version(&self) -> u128 {
        (self.int().wrapping_shr(64)) & 0xffff
    }

    #[getter]
    fn clock_seq_hi_variant(&self) -> u128 {
        (self.int().wrapping_shr(56)) & 0xff
    }

    #[getter]
    fn clock_seq_low(&self) -> u128 {
        (self.int().wrapping_shr(48)) & 0xff
    }

    #[getter]
    fn clock_seq(&self) -> u128 {
        ((self.clock_seq_hi_variant() & 0x3f).wrapping_shl(8)) | self.clock_seq_low()
    }

    #[getter]
    fn time(&self) -> u128 {
        ((self.time_hi_version() & 0x0fff).wrapping_shl(48))
            | (self.time_mid().wrapping_shl(32))
            | self.time_low()
    }

    #[getter]
    fn fields(&self) -> PyResult<(u128, u128, u128, u128, u128, u128)> {
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
    fn from_bytes(bytes: &PyBytes) -> PyResult<UUID> {
        let bytes: Bytes = bytes.extract()?;
        Ok(UUID {
            uuid: Uuid::from_bytes(bytes),
        })
    }

    #[staticmethod]
    fn from_bytes_le(bytes: &PyBytes) -> PyResult<UUID> {
        let bytes: Bytes = bytes.extract()?;
        Ok(UUID {
            uuid: Uuid::from_bytes_le(bytes),
        })
    }

    // #[staticmethod]
    // fn from_fields(fields: &PyTuple) -> PyResult<UUID> {
    //     Ok(UUID {
    //         uuid: Uuid::new_v4(),
    //     })
    // }

    #[staticmethod]
    fn from_int(int: u128) -> PyResult<UUID> {
        Ok(UUID {
            uuid: Uuid::from_u128(int),
        })
    }
}

#[pyfunction]
fn uuid1(node: u128, clock_seq: Option<u64>) -> PyResult<UUID> {
    let node = node.to_ne_bytes();
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
fn uuid4() -> PyResult<UUID> {
    Ok(UUID {
        uuid: Uuid::new_v4(),
    })
}

#[pyfunction]
fn uuid5(namespace: &UUID, name: &str) -> PyResult<UUID> {
    Ok(UUID {
        uuid: Uuid::new_v5(&namespace.uuid, name.as_bytes()),
    })
}

#[pyfunction]
fn uuid6(node: u128, timestamp: Option<u64>) -> PyResult<UUID> {
    let node = node.to_ne_bytes();
    let node = &[node[0], node[1], node[2], node[3], node[4], node[5]];

    let uuid = match timestamp {
        Some(timestamp) => {
            let timestamp = Timestamp::from_unix(&Context::new_random(), timestamp, 0);
            return Ok(UUID {
                uuid: Uuid::new_v6(timestamp, node),
            });
        }
        None => Uuid::now_v6(node),
    };
    Ok(UUID { uuid })
}

#[pyfunction]
fn uuid7(timestamp: Option<u64>) -> PyResult<UUID> {
    let uuid = match timestamp {
        Some(timestamp) => {
            let timestamp = Timestamp::from_unix(&Context::new_random(), timestamp, 0);
            return Ok(UUID {
                uuid: Uuid::new_v7(timestamp),
            });
        }
        None => Uuid::now_v7(),
    };
    Ok(UUID { uuid })
}

#[pyfunction]
fn uuid8(bytes: &PyBytes) -> PyResult<UUID> {
    let bytes: Bytes = bytes.extract()?;
    Ok(UUID {
        uuid: Uuid::new_v8(bytes),
    })
}

#[pymodule]
fn _uuid_utils(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_class::<UUID>()?;
    m.add_function(wrap_pyfunction!(uuid1, m)?)?;
    m.add_function(wrap_pyfunction!(uuid4, m)?)?;
    m.add_function(wrap_pyfunction!(uuid5, m)?)?;
    m.add_function(wrap_pyfunction!(uuid6, m)?)?;
    m.add_function(wrap_pyfunction!(uuid7, m)?)?;
    m.add_function(wrap_pyfunction!(uuid8, m)?)?;
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
