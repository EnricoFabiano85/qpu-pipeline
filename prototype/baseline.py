import numpy as np
import time

def compute_entropy(state: np.ndarray) -> tuple[np.ndarray, float]:
  """
  baseline numpy script to compute state entropy
  """

  #compute probabilities
  probabilities = np.abs(state)**2

  #filter out zero probabilities
  non_zero_mask = probabilities > 1e-12
  p_non_zero = probabilities[non_zero_mask]

  #compute entropy
  entropy = -np.sum(p_non_zero * np.log2(p_non_zero))

  return probabilities, float(entropy)

if __name__ == "__main__":

  n_qbits = 24
  N = 2**n_qbits

  print(f"Generating {n_qbits}-qubit state vector (N = {N:,}) elements...")

  state = np.random.rand(N) + 1j*np.random.rand(N)

  print("Executing baseline...")
  start = time.perf_counter()
  probs, entropy = compute_entropy(state)
  end = time.perf_counter()

  print("-"*30)
  print(f"Entropy: {entropy:.6f}")
  print(f"Execution time: {end - start:.4f} seconds")  
  print("-"*30)