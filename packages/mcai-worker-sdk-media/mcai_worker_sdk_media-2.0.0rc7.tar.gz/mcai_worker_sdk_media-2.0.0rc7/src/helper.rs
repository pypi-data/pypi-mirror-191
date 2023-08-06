#[cfg(not(feature = "media"))]
use pyo3::{
  prelude::*,
  types::{PyDict, PyList, PyString},
};

#[cfg(not(feature = "media"))]
pub fn get_destination_paths(response: &PyAny) -> Option<Vec<String>> {
  if response.is_none() {
    return None;
  }

  response
    .downcast::<PyDict>()
    .map(|object| {
      object
        .get_item("destination_paths")
        .and_then(|response_paths| {
          response_paths
            .downcast::<PyList>()
            .map(|path_list| {
              let destination_paths = path_list
                .iter()
                .map(|item| item.downcast::<PyString>())
                .filter(|downcast| downcast.is_ok())
                .map(|value| value.unwrap().to_string())
                .collect();

              Some(destination_paths)
            })
            .unwrap_or(None)
        })
    })
    .unwrap_or(None)
}

#[test]
#[cfg(not(feature = "media"))]
pub fn test_get_destination_paths() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let destination_paths = vec![
      "/path/to/destination/file_1".to_string(),
      "/path/to/destination/file_2".to_string(),
      "/path/to/destination/file_3".to_string(),
    ];

    let py_list = PyList::new(py, destination_paths.clone());
    let py_dict = PyDict::new(py);
    let result = py_dict.set_item("destination_paths", py_list);
    assert!(result.is_ok());

    let py_any: &PyAny = py_dict.into();

    let result = get_destination_paths(py_any);
    assert!(result.is_some());
    assert_eq!(destination_paths, result.unwrap());
  });
}

#[test]
#[cfg(not(feature = "media"))]
pub fn test_get_destination_paths_without_key() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let py_dict = PyDict::new(py);

    let py_any: &PyAny = py_dict.into();

    let result = get_destination_paths(py_any);
    assert!(result.is_none());
  });
}

#[test]
#[cfg(not(feature = "media"))]
pub fn test_get_destination_paths_without_list_value() {
  pyo3::prepare_freethreaded_python();

  Python::with_gil(|py| {
    let py_dict = PyDict::new(py);
    let result = py_dict.set_item("destination_paths", "some_value");
    assert!(result.is_ok());

    let py_any: &PyAny = py_dict.into();

    let result = get_destination_paths(py_any);
    assert!(result.is_none());
  });
}
