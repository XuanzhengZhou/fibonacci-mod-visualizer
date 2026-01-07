#!/bin/bash

echo "编译斐波那契模周期计算器..."

# 检测操作系统
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    echo "检测到 macOS，使用 clang++ 编译..."
    clang++ -std=c++11 -O3 -march=native -ffast-math -DNDEBUG \
        -o fibonacci_mod fibonacci_mod.cpp
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    echo "检测到 Linux，使用 g++ 编译..."
    g++ -std=c++11 -O3 -march=native -ffast-math -DNDEBUG \
        -o fibonacci_mod fibonacci_mod.cpp
else
    # 其他系统
    echo "检测到其他系统，尝试使用 g++ 编译..."
    g++ -std=c++11 -O3 -o fibonacci_mod fibonacci_mod.cpp
fi

if [ $? -eq 0 ]; then
    echo "编译成功！生成了可执行文件: cpp/fibonacci_mod"
    echo ""
    echo "使用方法:"
    echo "  ./cpp/fibonacci_mod <模数>"
    echo "  ./fibonacci_mod 1000              # 计算模1000的周期"
    echo "  ./fibonacci_mod 10000 > data.json # 结果保存到文件"
    echo ""
    echo "性能提示:"
    echo "  - 模数 < 1000: 非常快 (< 1秒)"
    echo "  - 模数 < 10000: 较快 (几秒)"
    echo "  - 模数 < 100000: 较慢 (几分钟)"
    echo "  - 模数 > 100000: 很慢 (可能需要几十分钟)"
else
    echo "编译失败！请检查编译器是否安装。"
    echo "在macOS上安装XCode Command Line Tools: xcode-select --install"
    echo "在Linux上安装g++: sudo apt-get install g++"
fi