import pytest
import numpy as np
import quantum_engine

from prototype.baseline import compute_entropy as numpy_entropy

@pytest.mark.parametrize("nQbits", [4, 12, 18])
def test_cpp_engine_unit(nQbits):

  N = 2**nQbits

  state = (np.random.rand(N) + 1j*np.random.rand(N)).astype(np.complex128)

  probs_ref, entropy_ref = numpy_entropy(state)

  out_probs = np.zeros(N, dtype=np.float64)
  entropy = quantum_engine.process_state(state, out_probs)

  assert np.isclose(entropy_ref, entropy, rtol=1e-5)
  assert np.allclose(probs_ref, out_probs, rtol=1e-15)

@pytest.mark.benchmark(group="entropy")
def test_numpy_reference(benchmark):
    
    nQbits = 24
    N = 2**nQbits

    state = (np.random.rand(N) + 1j*np.random.rand(N)).astype(np.complex128)
    benchmark(numpy_entropy, state)

@pytest.mark.benchmark(group="entropy")
def test_benchmark_engine(benchmark):

  nQbits = 24
  N = 2**nQbits

  state = (np.random.rand(N) + 1j*np.random.rand(N)).astype(np.complex128)
  out_probs = np.zeros(N, dtype=np.float64)
  benchmark(quantum_engine.process_state, state, out_probs)