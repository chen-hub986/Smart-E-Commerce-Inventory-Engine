cmake_minimum_required(VERSION 4.2)
project(Smart_E_Commerce_Inventory_Engine LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)

# Executable (optional)
add_executable(Smart_E_Commerce_Inventory_Engine
        "src/main.cpp"
)

# Find Python (interpreter + development headers/libs)
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

execute_process(
        COMMAND python -m pybind11 --cmakedir
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(pybind11 REQUIRED)

# Build Python extension module from mymodule.cpp
pybind11_add_module(Smart_Inventory_Engine_module
        "src/Smart_Inventory_Engine_module.cpp"
)
