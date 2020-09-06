CMAKE_MINIMUM_REQUIRED(VERSION 3.16)

PROJECT(kaitaiAnimalReader)

set(CMake_Misc_Dir "${CMAKE_CURRENT_SOURCE_DIR}/cmake")
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMake_Misc_Dir}")

include_directories(${CMAKE_PREFIX_PATH}/include)

include(Hardening)
include(FetchContent)
include(DownloadCLI11)

find_library(CPU-KERNELS awkward-cpu-kernels HINTS ${CMAKE_PREFIX_PATH}/lib)
find_library(LIBAWKWARD awkward HINTS ${CMAKE_PREFIX_PATH}/lib)
message(STATUS "Libraries: ${LIBAWKWARD} ${CPU-KERNELS}")

downloadCLI11IfNeeded("CLI11")

set(CMAKE_USE_RELATIVE_PATHS TRUE)
set(Source_dir "${CMAKE_CURRENT_SOURCE_DIR}/src")
set(kaitai_struct_cpp_runtime_DIR "${CMAKE_CURRENT_SOURCE_DIR}/kaitai_struct_cpp_stl_runtime")

get_cmake_property(_variableNames VARIABLES)
list (SORT _variableNames)
foreach (_variableName ${_variableNames})
    message(STATUS "${_variableName}=${${_variableName}}")
endforeach()

file(GLOB_RECURSE SRCFILES "${Source_dir}/*.c" "${Source_dir}/*.cpp")
if(MSVC_IDE)
	file(GLOB_RECURSE HDRFILES "${Source_dir}/*.h")
endif()

add_subdirectory("${kaitai_struct_cpp_runtime_DIR}")

add_executable(kaitaiAnimalReader "${SRCFILES}")
target_link_libraries(kaitaiAnimalReader kaitai_struct_cpp_stl_runtime ${CPU-KERNELS} ${LIBAWKWARD})
target_include_directories(kaitaiAnimalReader  PUBLIC "${kaitai_struct_cpp_runtime_DIR}" "${CLI11_INCLUDE_DIR}")

set_target_properties(kaitaiAnimalReader PROPERTIES CXX_VISIBILITY_PRESET hidden)
#target_link_libraries(kaitaiAnimalReader PRIVATE ${CPU-KERNELS} ${LIBAWKWARD})

set_property(TARGET kaitaiAnimalReader PROPERTY CXX_STANDARD 20)
set_property(TARGET kaitaiAnimalReader PROPERTY PREFIX "")
harden(kaitaiAnimalReader)
