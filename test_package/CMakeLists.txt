PROJECT(MyHello)
cmake_minimum_required(VERSION 2.8.12)

add_definitions (-D_GLIBCXX_USE_CXX11_ABI=0)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()


ADD_EXECUTABLE(client client.cpp)
ADD_EXECUTABLE(server server.cpp)
TARGET_LINK_LIBRARIES(client ${CONAN_LIBS})
TARGET_LINK_LIBRARIES(server ${CONAN_LIBS})
