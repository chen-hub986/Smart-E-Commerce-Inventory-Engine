cmake_minimum_required(VERSION 3.14)
project(Smart_E_Commerce_Inventory_Engine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# Note: avoid forcing -static for Python extension modules; leave linkage default

# Executable (optional)
add_executable(Smart_E_Commerce_Inventory_Engine main.cpp)
target_compile_features(Smart_E_Commerce_Inventory_Engine PRIVATE cxx_std_20)

# Find Python (interpreter + development headers/libs)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

# Try to obtain pybind11 cmake config via the Python installation (if pybind11
# was installed via pip, python -m pybind11 --cmakedir returns its cmake dir)
execute_process(
    COMMAND "${Python3_EXECUTABLE}" -m pybind11 --cmakedir
    OUTPUT_VARIABLE PYBIND11_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

if(PYBIND11_DIR)
    list(APPEND CMAKE_PREFIX_PATH "${PYBIND11_DIR}")
endif()

# First try to find an installed pybind11 package; if not found, fall back to FetchContent
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    message(STATUS "pybind11 not found via find_package; will try using Python-provided path or FetchContent.")
    if(PYBIND11_DIR)
        find_package(pybind11 CONFIG QUIET PATHS "${PYBIND11_DIR}")
    endif()
endif()

if(NOT pybind11_FOUND)
    include(FetchContent)
    message(STATUS "Fetching pybind11 from GitHub...")
    FetchContent_Declare(
        pybind11
        GIT_REPOSITORY https://github.com/pybind/pybind11.git
        GIT_TAG        v2.11.1 # you can pin a specific release or change to main
    )
    FetchContent_MakeAvailable(pybind11)
    # After FetchContent_MakeAvailable, pybind11's targets (pybind11::module, etc.)
    # are available without requiring a separate find_package call.
endif()


# Build Python extension module from mymodule.cpp
pybind11_add_module(Smart_Inventory_Engine_module MODULE Smart_Inventory_Engine_module.cpp)
target_compile_features(Smart_Inventory_Engine_module PRIVATE cxx_std_20)
