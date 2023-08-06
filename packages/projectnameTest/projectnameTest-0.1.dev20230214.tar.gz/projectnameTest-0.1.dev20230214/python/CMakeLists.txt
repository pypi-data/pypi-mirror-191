add_subdirectory(projectnameTest)
configure_file(setup.py.in setup.py)
dune_python_configure_bindings(
  PATH "."
  PACKAGENAME projectnameTest
  CMAKE_METADATA_FLAGS DUNE_OPTS_FILE
)
if(POLICY CMP0087)
  cmake_policy(SET CMP0087 NEW)
endif()
