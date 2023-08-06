use markdown_utils;
use pyo3::prelude::*;

#[pyfunction]
#[pyo3(name = "modify_headings_offset")]
fn py_modify_headings_offset(text: &str, offset: i8) -> PyResult<String> {
    Ok(markdown_utils::heading::modify_headings_offset(text, offset))
}

#[pyfunction]
#[pyo3(name = "n_backticks_to_wrap_codespan")]
fn py_n_backticks_to_wrap_codespan(character: char, text: &str) -> PyResult<usize> {
    Ok(markdown_utils::codespan::n_backticks_to_wrap_codespan(
        character, text,
    ))
}

#[pyfunction]
#[pyo3(name = "parse_link_references")]
fn py_parse_link_references(text: &str) -> PyResult<Vec<Vec<String>>> {
    Ok(markdown_utils::link::parse_link_references(text))
}

#[pymodule]
#[pyo3(name = "markdown_utils")]
fn py_markdown_utils(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(py_modify_headings_offset, m)?)?;
    m.add_function(wrap_pyfunction!(py_n_backticks_to_wrap_codespan, m)?)?;
    m.add_function(wrap_pyfunction!(py_parse_link_references, m)?)?;
    Ok(())
}
