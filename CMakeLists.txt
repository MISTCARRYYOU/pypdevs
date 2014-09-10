cmake_minimum_required (VERSION 2.8.11)
project (PyPDEVS)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
find_package(PythonInterp REQUIRED)
find_package(Sphinx REQUIRED)

add_subdirectory(src)
add_subdirectory(docs)
add_subdirectory(test)
