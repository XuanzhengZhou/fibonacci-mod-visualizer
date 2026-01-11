#!/bin/bash

echo "Compiling Fibonacci Modulo Period Calculator..."

# Detect operating system
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "Detected macOS, compiling with clang++..."
    clang++ -std=c++11 -O3 -march=native -ffast-math -DNDEBUG \
        -o ../cpp/fibonacci_mod ../src/fibonacci_mod.cpp
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "Detected Linux, compiling with g++..."
    g++ -std=c++11 -O3 -march=native -ffast-math -DNDEBUG \
        -o ../cpp/fibonacci_mod ../src/fibonacci_mod.cpp
else
    # Other systems
    echo "Detected other system, trying to compile with g++..."
    g++ -std=c++11 -O3 -o ../cpp/fibonacci_mod ../src/fibonacci_mod.cpp
fi

if [ $? -eq 0 ]; then
    echo "Compilation successful! Executable generated: cpp/fibonacci_mod"
    echo ""
    echo "Usage:"
    echo "  ./cpp/fibonacci_mod <modulo>"
    echo "  ./fibonacci_mod 1000              # Calculate period for modulo 1000"
    echo "  ./fibonacci_mod 10000 > data.json # Save results to file"
    echo ""
    echo "Performance tips:"
    echo "  - Modulo < 1000: Very fast (< 1 second)"
    echo "  - Modulo < 10000: Fast (a few seconds)"
    echo "  - Modulo < 100000: Slow (a few minutes)"
    echo "  - Modulo > 100000: Very slow (may take tens of minutes)"
else
    echo "Compilation failed! Please check if compiler is installed."
    echo "Install XCode Command Line Tools on macOS: xcode-select --install"
    echo "Install g++ on Linux: sudo apt-get install g++"
fi