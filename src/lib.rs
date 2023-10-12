use pyo3::prelude::*;
use rand::prelude::Distribution;
use rand::Rng;
use rand::SeedableRng;
use std::any::Any;
use pyo3::types;
use std::convert::TryInto;

trait Space<T> {
    fn _sample(&mut self) -> T;
    fn _sample_batch(&mut self, n: usize) -> Vec<T>;
    fn _contains(&self, value: &dyn Any) -> bool; // Need to have a different name so we can export the `.contains` method in the #[pymethods] block.
    fn _seed(&mut self, seed: u64);
}

#[pyclass]
struct Discrete {
    n: usize,
    rng: rand::rngs::StdRng,
}

#[pymethods]
impl Discrete {
    #[new]
    fn newbob(n: usize, rng_seed: Option<u64>) -> Self {
        let rng = match rng_seed {
            Some(seed) => rand::rngs::StdRng::seed_from_u64(seed),
            None => rand::rngs::StdRng::from_entropy(),
        };
        Discrete {
            n,
            rng,
            // start: start.unwrap_or(0),
        }
    }
    fn sample(&mut self) -> usize {
        // sample a random value of type T in the range [0, self.n]
        return self._sample()
        // return rand::random::<u32>() % self.n;
    }
    fn sample_batch(&mut self, n: usize) -> Vec<usize> {
        // sample a random value of type T in the range [0, self.n]
        return self._sample_batch(n)
    }

    fn contains(&self, value: isize) -> bool {
        return self._contains(&value);
    }
    fn __contains__(&self, value: &PyAny) -> bool {
        // if value.downcast::<pyo3::types::PyInt>().is_err(){
        //     return false
        // }
        // return value.downcast::<pyo3::types::PyInt>().is_ok_and(|x| 0 <= x && x < self.n);

        return value.downcast::<pyo3::types::PyInt>().is_ok_and(|x| self._contains(x));
        // let is_contained = match option {
        //     Ok(v) => self._contains(&v),
        //     Err(_) => false,
        // };
        // return is_contained
    }

    fn seed(&mut self, state: u64) {
        self._seed(state)
    }
    fn __repr__(slf: &PyCell<Self>) -> PyResult<String> {
        // This is the equivalent of `self.__class__.__name__` in Python.
        let class_name: &str = slf.get_type().name()?;
        // To access fields of the Rust struct, we need to borrow the `PyCell`.
        Ok(format!("{}({})", class_name, slf.borrow().n))
    }
}

impl Space<usize> for Discrete {
    fn _sample(&mut self) -> usize {
        // sample a random value of type T in the range [0, self.n]
        return self.rng.gen_range(0..self.n);
        // return rand::random::<u32>() % self.n;
    }
    fn _sample_batch(&mut self, n: usize) -> Vec<usize> {
        // sample a random value of type T in the range [0, self.n]
        let dist_iter = rand::distributions::Uniform::new(0, self.n).sample_iter(self.rng.clone());
        return dist_iter.take(n).into_iter().collect();
    }
    fn _contains(&self, value: &dyn Any) -> bool {
        // Returns False if the value cannot be casted into an integer, or if it is not in the range [0, self.n]
        let value = match value.downcast_ref::<isize>() {
            Some(value) => *value,
            None => return false,
        };
        return (0 <= value) && (value < self.n.try_into().unwrap());
    }

    fn _seed(&mut self, state: u64) {
        self.rng = rand::rngs::StdRng::seed_from_u64(state);
    }
}

#[pymodule]
fn spatial(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    // m.add_wrapped(Discrete);
    // m.add_wrapped(wrap_pyfunction!(get_42))?;
    // m.add_class::<Space>()?;
    m.add_class::<Discrete>()?;
    Ok(())
}
