#include <cmath>
#include <complex>
#include <omp.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <span>
#include <stdexcept>

namespace quantum_engine {

namespace py = pybind11;

double compute_entropy_impl(std::span<const std::complex<double>> state, std::span<double> out_probs) 
{
  auto constexpr THRESHOLD = 1e-12;

  auto norm_sq = 0.0;
#pragma omp parallel for simd reduction(+ : norm_sq)
  for (size_t i = 0; i < state.size(); ++i) {
      auto const prob = std::norm(state[i]);
      out_probs[i] = prob;
      norm_sq += prob;
  }

  auto const inv_norm = 1./norm_sq;

  auto total_entropy = 0.0;
#pragma omp parallel for simd reduction(+ : total_entropy)
  for (size_t i = 0; i < state.size(); ++i) 
  {
    auto const prob = out_probs[i] * inv_norm;
    out_probs[i] = prob;
    auto const safe_log = prob > THRESHOLD ? prob : 1.0;

    total_entropy += (prob * std::log2(safe_log));
  }
  return -total_entropy;
}

double compute_entropy(py::array_t<std::complex<double>> state_py, py::array_t<double> out_py) 
{
  py::buffer_info state_buf = state_py.request();
  py::buffer_info out_buf = out_py.request();

  if (state_buf.ndim != 1 || out_buf.ndim != 1)
    throw std::runtime_error("Input and output tensors must be 1-dimensional");

  if (state_buf.size != out_buf.size)
    throw std::runtime_error("Input and output tensors must have same size");

  auto state = std::span<const std::complex<double>>(static_cast<std::complex<double>*>(state_buf.ptr), 
                                                     state_buf.shape[0]);
  auto out_probs = std::span<double>(static_cast<double*>(out_buf.ptr),
                                    out_buf.shape[0]);

  return compute_entropy_impl(state, out_probs);
}
}


PYBIND11_MODULE(quantum_engine, m) {
  m.doc() = "Zero-Copy Quantum State Processor";

  m.def("process_state", &quantum_engine::compute_entropy,
        "Calculate Shannon entropy and extract probabilities in-place");

  m.def("set_nume_threads", &omp_set_num_threads, pybind11::arg("n"),
        "Set number of OMP threads.");
}