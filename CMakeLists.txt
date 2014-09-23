cmake_minimum_required (VERSION 2.8.7)
project (PyPDEVS)
enable_testing()
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
set(PACKAGE_VERSION "2.2.4")
find_package(PythonInterp REQUIRED)

set(SETUP_PY_IN "${CMAKE_CURRENT_SOURCE_DIR}/setup.py.in")
set(SETUP_PY "${CMAKE_CURRENT_BINARY_DIR}/setup.py")
set(DEPS "${CMAKE_CURRENT_SOURCE_DIR}/pypdevs/__init__.py")
set(OUTPUT "${CMAKE_CURRENT_BINARY_DIR}/build/timestamp")

configure_file(${SETUP_PY_IN} ${SETUP_PY})

add_custom_command(OUTPUT ${OUTPUT}
                   COMMAND ${PYTHON_EXECUTABLE} setup.py build
                   COMMAND ${CMAKE_COMMAND} -E touch ${OUTPUT}
                   DEPENDS ${DEPS})
add_custom_target(target ALL DEPENDS ${OUTPUT})

install(CODE "execute_process(COMMAND ${PYTHON_EXECUTABLE} ${SETUP_PY} install --user)")

add_subdirectory(docs)
add_subdirectory(test)
