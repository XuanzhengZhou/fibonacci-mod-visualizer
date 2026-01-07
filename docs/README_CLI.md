# 斐波那契数列模周期 - 命令行工具

## 快速开始

### 1. 编译C++高性能计算程序

```bash
bash compile.sh
```

或使用g++直接编译：

```bash
g++ -std=c++11 -O3 -o fibonacci_mod fibonacci_mod.cpp
```

### 2. 安装Python依赖

```bash
pip3 install matplotlib numpy
```

### 3. 运行交互式可视化工具

```bash
python3 fibonacci_cli_visualizer.py
```

## 功能特性

### 高性能计算
- 使用优化的C++算法，支持大模数计算（最高1,000,000）
- 自动检测并去重周期
- 输出JSON格式数据

### 交互式命令行界面
- 直观的菜单导航系统
- 支持灵活的范围选择（如: 3-5,6,7-21）
- 实时预览选择的数列

### 可视化功能
- 生成与网页版相同的二维网格可视化
- 支持导出PNG图片
- 自动处理大网格优化

### 数据导出
- 支持导出完整数据为JSON格式
- 包含所有周期信息和选择状态

## 使用示例

### 计算模100的周期
```bash
./fibonacci_mod 100
```

### 运行交互式工具
```bash
python3 fibonacci_cli_visualizer.py
```

然后按照菜单提示：
1. 选择"计算新的模数"
2. 输入100
3. 等待计算完成
4. 选择"选择要可视化的数列"
5. 输入范围，如: 0-3,5,7-9
6. 选择"生成可视化图表"

### 常见输入格式

选择数列时支持以下格式：
- `3-5,6,7-21` - 选择多个范围和单个数列
- `all` - 选择所有数列
- `0-10` - 选择前11个数列
- `clear` - 清空选择

## 性能提示

- **模数 < 1000**: 非常快 (< 1秒)
- **模数 < 10000**: 较快 (几秒)
- **模数 < 100000**: 较慢 (几分钟)
- **模数 > 100000**: 很慢 (可能需要几十分钟)

## 文件说明

- `fibonacci_mod.cpp` - C++高性能计算核心
- `fibonacci_cli_visualizer.py` - Python交互式可视化工具
- `fibonacci-mod-visualizer.html` - 网页版可视化工具
- `compile.sh` - 自动编译脚本

## 系统要求

- C++编译器支持C++11标准
- Python 3.6+
- matplotlib库
- numpy库

## 许可证

MIT License
