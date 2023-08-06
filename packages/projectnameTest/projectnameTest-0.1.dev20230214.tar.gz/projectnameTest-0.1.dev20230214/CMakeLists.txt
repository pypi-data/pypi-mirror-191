# SPDX-FileCopyrightText: 2022  mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

cmake_minimum_required(VERSION 3.18 FATAL_ERROR)
option(DUNE_ENABLE_PYTHONBINDINGS "Enable Python bindings" ON)
option(DUNE_PYTHON_ALLOW_GET_PIP "Allow dune-common to install pip into venv" ON)



project(
        projectnameTest
  VERSION 0.1
  LANGUAGES C CXX
)

# find dune packages to make cmake modules available
#set (CMAKE_PREFIX_PATH "/duneci/dunebuild/dune-common/build-cmake;/duneci/dunebuild/dune-grid/build-cmake;/duneci/dunebuild/dune-geometry/build-cmake")
find_package(dune-common REQUIRED EXCLUDE_FROM_ALL)
list(APPEND CMAKE_MODULE_PATH "${PROJECT_SOURCE_DIR}/cmake/modules" ${dune-common_MODULE_PATH})
include(DuneMacros)

dune_project()
dune_enable_all_packages()

add_subdirectory(projectnameTest)


if(DUNE_ENABLE_PYTHONBINDINGS)
  add_subdirectory(python)
endif()

# finalize the dune project, e.g. generating config.h etc.
finalize_dune_project(GENERATE_CONFIG_H_CMAKE)
