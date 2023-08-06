# SPDX-FileCopyrightText: 2022  mueller@ibb.uni-stuttgart.de
# SPDX-License-Identifier: LGPL-3.0-or-later

cmake_minimum_required(VERSION 3.18)

set(sources foo.cpp)

dune_add_library(${PROJECT_NAME} ${sources})
target_link_libraries(${PROJECT_NAME} PUBLIC ${DUNE_LIBS})
target_link_dune_default_libraries(${PROJECT_NAME})

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_20)

if( DUNE_ENABLE_PYTHONBINDINGS )
    add_subdirectory(python)
endif()
