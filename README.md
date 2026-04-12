This repo demonstrates the high-performance post processing of a simulated quantum state.

The initial, inefficient post processing is performed exclusively in python. In the high-performance 
post-processing engine, the quantum simulation is mocked in python by generating the quantum 
state using a random number generator (numpy random). The state is then passed to C++ for fast
computation of Shannon's entropy using a FFI, zero-copy approach with pybind11. The acceleration
of Shannon's computation is performed with openmp CPU pragmas, although alternative strategies have also
been considered.

## Build and execution
The architecture is fully containerized using a minimal `python3:11-slim` image

1. **Build and launch docker:**
```bash
docker build -t quantum-engine .
docker run -it -v $(pwd):/app quantum-engine /bin/bash
```

## Roadmap
+ **Phase 1**
Demonstrate high-performance, zero-copy FFI post processing. Python owns the memory and simulates the quantum computer.
+ **Phase 2**
The C++ backend will own the memory and will simulate the quantum computer The python frontend will communicate with the compute engine via small payloads