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
  auto total_entropy = 0.0;
  auto constexpr THRESHOLD = 1e-12;

#pragma omp parallel for simd reduction(+ : total_entropy)
  for (size_t i = 0; i < state.size(); ++i) 
  {
    auto const prob = std::max(std::norm(state[i]), THRESHOLD);
    out_probs[i] = prob;

    total_entropy += (prob * std::log2(prob));
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
}