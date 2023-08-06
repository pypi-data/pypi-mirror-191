extern crate nalgebra as na;

pub mod bindings;
mod core;

use crate::bindings::edg::PyEventDrivenGas;
use crate::bindings::random_walk::{one_a, one_b};
use pyo3::prelude::*;
use pyo3::wrap_pymodule;

/// A Rust based numerics library
#[pymodule]
fn smumerix(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_wrapped(wrap_pymodule!(preex))?;
    m.add_function(wrap_pyfunction!(main, m)?)?;
    m.add_class::<PyEventDrivenGas>()?;
    Ok(())
}

/// Functions needed for pre exercise
#[pymodule]
fn preex(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(one_a, m)?)?;
    m.add_function(wrap_pyfunction!(one_b, m)?)?;
    Ok(())
}

#[pyfunction]
fn main() -> PyResult<()> {
    println!("Hello world from rust");
    Ok(())
}
