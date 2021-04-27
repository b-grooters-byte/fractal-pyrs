use fractal_rs::{Config, Mandelbrot, PixelFormat};
use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

#[pyfunction]
pub fn render(
    width: u32,
    height: u32,
    cx: f64,
    cy: f64,
    zoom: f64,
    iter: u16,
) -> PyResult<Vec<u8>> {
    let c = Config::new(width, height, cx, cy, zoom, iter, PixelFormat::RGBA8);
    let mut m = Mandelbrot::new(c);
    Ok(m.render())
}

#[pymodule]
pub fn fractal_pyrs(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(render, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    #[test]
    fn it_works() {
        assert_eq!(2 + 2, 4);
    }
}
