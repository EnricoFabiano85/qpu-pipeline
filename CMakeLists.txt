cmake_minimum_required(VERSION 3.20)
project(${SKBUILD_PROJECT_NAME} VERSION ${SKBUILD_PROJECT_VERSION} LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Python COMPONENTS Interpreter Development.Module REQUIRED)
find_package(pybind11 CONFIG REQUIRED)
find_package(OpenMP REQUIRED)

pybind11_add_module(quantum_engine src/engine.cpp)
target_link_libraries(quantum_engine PRIVATE OpenMP::OpenMP_CXX)
target_compile_options(quantum_engine PRIVATE
    $<$<CXX_COMPILER_ID:GNU>:-O3 -march=native -Wall -Wextra -Werror>
)

install(TARGETS quantum_engine LIBRARY DESTINATION .)