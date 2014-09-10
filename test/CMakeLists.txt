add_custom_target(basic_tests
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND ${PYTHON_EXECUTABLE} "test_basic.py")
add_custom_target(mpi_tests
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND ${PYTHON_EXECUTABLE} "test_mpi.py")
add_custom_target(realtime_tests
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND ${PYTHON_EXECUTABLE} "test_realtime.py")
add_custom_target(test
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    COMMAND ${PYTHON_EXECUTABLE} "test_basic.py"
    COMMAND ${PYTHON_EXECUTABLE} "test_mpi.py"
    COMMAND ${PYTHON_EXECUTABLE} "test_realtime.py"
    )
