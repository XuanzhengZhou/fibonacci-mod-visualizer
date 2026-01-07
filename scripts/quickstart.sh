#!/bin/bash

# 斐波那契数列模周期 - 快速启动脚本

echo "======================================"
echo "斐波那契数列模周期可视化工具"
echo "======================================"
echo ""

# 检查C++程序是否存在
if [ ! -f "./fibonacci_mod" ]; then
    echo "C++程序未编译，开始编译..."
    bash compile.sh
    
    if [ $? -ne 0 ]; then
        echo "编译失败！请检查错误信息。"
        exit 1
    fi
    echo ""
fi

# 检查Python依赖
echo "检查Python依赖..."
python3 -c "import matplotlib" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "未找到matplotlib库，正在安装..."
    pip3 install matplotlib numpy
fi
echo "✓ 依赖检查完成"
echo ""

# 启动交互式工具
echo "启动交互式可视化工具..."
echo ""
python3 python/fibonacci_cli_visualizer.py
