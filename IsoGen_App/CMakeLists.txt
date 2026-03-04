
cmake_minimum_required(VERSION 3.20)
project(IsoGen_App LANGUAGES CXX)

find_package(opencascade CONFIG REQUIRED)

add_executable(IsoGen_App src/main.cpp )