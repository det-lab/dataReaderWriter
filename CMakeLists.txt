cmake_minimum_required(VERSION 3.16)

# set the project name
project(readXIA)

# link/include awkward 
set(LINK_LIBS awkward awkward-cpu-kernels)

link_directories(/opt/awkward-1.0/build/lib.linux-x86_64-3.7/awkward1)

INCLUDE_DIRECTORIES(
  /opt/awkward-1.0/include
  /opt/awkward-1.0/rapidjson/include
  )

add_executable(Test tests/test.cpp)
target_link_libraries(Test PRIVATE ${LINK_LIBS})
set_target_properties(Test PROPERTIES CXX_VISIBILITY_PRESET hidden)
