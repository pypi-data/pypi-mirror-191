use pyo3::prelude::*;
use unicode_linebreak::{linebreaks as rust_linebreaks, BreakOpportunity::{Mandatory}};

#[pyfunction]
fn linebreaks(text: &str) -> PyResult<Vec<(usize, bool)>> {
    let mut vec = Vec::new();
    for val in rust_linebreaks(text) {
        vec.push((val.0, val.1 == Mandatory));
    }
    Ok(vec)
}

#[pymodule]
#[pyo3(name = "unicode_linebreak")]
fn py_unicode_linebreak(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(linebreaks, m)?)?;
    Ok(())
}
