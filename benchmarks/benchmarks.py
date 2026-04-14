import sys
import os
import numpy as np
import time
import quantum_engine

cwd = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.abspath(os.path.join(cwd, '..'))
if root_dir not in sys.path: sys.path.insert(0, root_dir)

from prototype.baseline import compute_entropy

def run_benchmark():
    
  n_qbits = 24
  N = 2**n_qbits

  print(f"Generating {n_qbits}-qubit state vector (N = {N:,}) elements...")
  
  print(f"Allocating complex memory for {N} quantum states...")

  state = (np.random.rand(N) + 1j*np.random.rand(N)).astype(np.complex128)
  
  out_probs = np.zeros(N, dtype=np.float64)

  print("\n--- Running Baseline ---")
  start_time = time.perf_counter()

  probs_ref, entropy_ref = compute_entropy(state)
  
  numpy_time = time.perf_counter() - start_time
  print(f"Python Execution Time: {numpy_time:.5f} seconds")
  print(f"Python Entropy:        {entropy_ref:.8f}")

  print("\n--- Running C++ OpenMP Engine ---")
  # Warmup
  quantum_engine.process_state(state[:100], out_probs[:100])

  start_time = time.perf_counter()
  
  cpp_entropy = quantum_engine.process_state(state, out_probs)
  
  cpp_time = time.perf_counter() - start_time
  print(f"C++ Execution Time:   {cpp_time:.5f} seconds")
  print(f"C++ Entropy:          {cpp_entropy:.8f}")

  probs_match = np.allclose(probs_ref, out_probs, atol=1e-12)
  entropy_match = np.isclose(entropy_ref, cpp_entropy, rtol=1e-05)

  if not probs_match and not entropy_match:
    print("Python and C++ results differ!.")

  print(f"\nSpeedup: {numpy_time / cpp_time:.2f}x")

if __name__ == "__main__":
  run_benchmark()