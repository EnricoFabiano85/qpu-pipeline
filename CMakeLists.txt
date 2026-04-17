cmake_minimum_required(VERSION 3.20.0)
project(QuantumEngine VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(OpenMP REQUIRED)
find_package(Python3 COMPONENTS Interpreter Development.Module REQUIRED)

execute_process(
  COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
  OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
  OUTPUT_STRIP_TRAILING_WHITESPACE
)
list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_CMAKE_DIR}")
find_package(pybind11 CONFIG REQUIRED)

pybind11_add_module(quantum_engine src/engine.cpp)

target_link_libraries(quantum_engine PRIVATE OpenMP::OpenMP_CXX)

target_compile_options(quantum_engine PRIVATE
    $<$<CXX_COMPILER_ID:GNU>: -O3 -march=native -Wall -Wextra -Werror>
)
