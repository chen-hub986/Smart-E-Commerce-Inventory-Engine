cmake_minimum_required(VERSION 4.2)
project(Smart_E_Commerce_Inventory_Engine)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -static-libgcc -static-libstdc++")

add_executable(Smart_E_Commerce_Inventory_Engine main.cpp)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

execute_process(
        COMMAND python -m pybind11 --cmakedir
        OUTPUT_VARIABLE pybind11_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
)
find_package(pybind11 REQUIRED)

pybind11_add_module(Smart_E_Commerce_Inventory_Engine_module mymodule.cpp)
