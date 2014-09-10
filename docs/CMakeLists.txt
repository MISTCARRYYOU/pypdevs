find_package(Sphinx REQUIRED)

set(SPHINX_CACHE_DIR "${CMAKE_CURRENT_BINARY_DIR}/_doctrees")
set(SPHINX_HTML_DIR "${CMAKE_CURRENT_BINARY_DIR}/html")
set(BINARY_BUILD_DIR "${CMAKE_CURRENT_BINARY_DIR}/_build")

configure_file("${CMAKE_CURRENT_SOURCE_DIR}/conf.py.in" "${BINARY_BUILD_DIR}/conf.py")

add_custom_target(pypdevs_docs ALL
        ${SPHINX_EXECUTABLE}
            -b html
            -d "${SPHINX_CACHE_DIR}"
            -c "${BINARY_BUILD_DIR}"
            "${CMAKE_CURRENT_SOURCE_DIR}"
            "${SPHINX_HTML_DIR}"
        COMMENT "Building HTML documentation with Sphinx")
