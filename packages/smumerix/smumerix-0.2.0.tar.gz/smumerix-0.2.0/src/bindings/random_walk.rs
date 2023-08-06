use crate::core::random_walk::{
    level_crossing_prob_sim, probability_distribution, start_point_sim,
};

use pyo3::prelude::*;

#[pyfunction]
pub fn one_a(num_loops: usize) -> PyResult<Vec<f64>> {
    let sim_res = start_point_sim(num_loops);
    Ok(probability_distribution(&sim_res))
}

#[pyfunction]
pub fn one_b(point: f64, num_loops: usize) -> PyResult<Vec<f64>> {
    let sim_res = level_crossing_prob_sim(point, num_loops);
    Ok(probability_distribution(&sim_res))
}
