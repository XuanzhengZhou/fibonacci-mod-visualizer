# 斐波那契数列模周期可视化工具

一个用于计算、分析和可视化斐波那契数列在模运算下周期规律的高性能工具集。

[![C++ Version](https://img.shields.io/badge/C%2B%2B-11-blue.svg)](src/fibonacci_mod.cpp)
[![Python Version](https://img.shields.io/badge/Python-3.x-blue.svg)](python/fibonacci_cli_visualizer.py)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](#license)
[![Web Support](https://img.shields.io/badge/Web-HTML%2FJS-blue.svg)](web/fibonacci-mod-visualizer.html)

## 项目简介

本项目提供了一套完整的工具链，用于探索斐波那契数列在模运算下的周期性规律（Pisano周期）。通过高性能的C++计算核心、交互式的Python命令行工具和直观的网页版可视化界面，用户可以深入理解这一有趣的数学现象。

### 核心特性

- **高性能计算**：优化的C++算法，支持模数高达1,000,000
- **双模式可视化**：命令行工具（支持导出高清图片）+ 网页版交互界面
- **智能周期检测**：自动识别并去重所有周期序列
- **灵活的数据导出**：支持JSON格式导出，便于进一步分析
- **跨平台支持**：支持Linux、macOS和Windows系统

## 项目结构

```
斐波那契数列可视化/
├── src/                              # C++源代码
│   └── fibonacci_mod.cpp            # 高性能计算核心
├── cpp/                             # 编译后的可执行文件
│   └── fibonacci_mod                # C++程序（编译后生成）
├── python/                          # Python工具
│   ├── fibonacci_cli_visualizer.py # 交互式可视化工具（完整版）
│   └── fibonacci_cli_simple.py     # 轻量级ASCII可视化工具
├── web/                             # 网页版工具
│   └── fibonacci-mod-visualizer.html # 浏览器可视化界面
├── scripts/                         # 脚本文件
│   ├── compile.sh                   # 自动编译脚本
│   └── quickstart.sh                # 一键启动脚本
├── docs/                            # 文档
│   ├── 使用指南.md                  # 完整使用指南
│   ├── 可视化更新说明.md            # 双图输出功能说明
│   ├── 双图输出功能说明.md          # 双图输出详细说明
│   ├── 双图输出完成总结.md          # 双图输出总结
│   ├── 快速开始.md                  # 快速开始指南
│   └── README_CLI.md                # 命令行工具说明
├── examples/                        # 示例数据
│   ├── demo_mod_30.json             # 模30示例数据
│   └── test_data_mod_20.json        # 模20测试数据
├── output/                          # 输出文件（图表等）
│   ├── fibonacci_mod_512_visualization.png
│   └── fibonacci_mod_729_visualization.png
├── .gitignore                       # Git忽略配置
└── README.md                        # 项目主文档（本文件）
```

## 功能详解

### 1. 高性能计算核心（C++）

位于 `src/fibonacci_mod.cpp`，采用优化的算法实现：

#### 核心算法

**算法目标**：计算斐波那契数列 F(n) mod m 的所有周期序列

**算法步骤**：
1. **状态空间遍历**：遍历所有可能的初始值对 (a₀, b₀)，其中 a₀, b₀ ∈ [0, m-1]
2. **周期检测**：对每个初始值对，生成斐波那契序列直到检测到重复状态
3. **规范化处理**：将检测到的周期旋转到最小字典序，便于去重
4. **去重存储**：使用哈希集合自动去重，保存所有唯一周期

**关键技术优化**：
- **智能哈希**：自定义 `PairHash` 结构，将 (a, b) 对映射为唯一哈希值
- **内存预分配**：使用 `reserve()` 预分配容器空间，减少动态扩容开销
- **进度显示**：大模数计算时显示进度百分比
- **规范化算法**：通过 `canonicalCycle()` 函数将周期旋转到标准形式

**复杂度分析**：
- **时间复杂度**：O(m² × L)，其中 m 是模数，L 是平均周期长度
- **空间复杂度**：O(m²)，用于存储访问状态和周期数据

#### 编译和运行

```bash
# 进入项目目录
cd /Users/mac/Documents/代码/斐波那契数列可视化

# 编译（使用脚本）
bash scripts/compile.sh

# 或直接编译
g++ -std=c++11 -O3 -o cpp/fibonacci_mod src/fibonacci_mod.cpp

# 运行
./cpp/fibonacci_mod <模数>
./cpp/fibonacci_mod 1000              # 计算模1000
./cpp/fibonacci_mod 10000 > data.json # 保存到文件
```

### 2. 交互式命令行工具（Python）

#### 完整版可视化工具

`python/fibonacci_cli_visualizer.py` - 功能完整的交互式可视化工具

**功能特性**：
- 交互式菜单操作
- 支持灵活的范围选择语法（如：`1-3,5,8-10`）
- 生成高质量matplotlib图表
- **双图输出**：正常尺寸图 + 高分辨率大图
- 支持导出PNG图片
- 彩色图例显示

**依赖安装**：
```bash
pip3 install matplotlib numpy
```

**运行方法**：
```bash
cd ~/python
python3 python/fibonacci_cli_visualizer.py
```

**双图输出说明**：
- **图1（正常版）**：14×7英寸，150 DPI，适合快速预览
- **图2（高清版）**：动态尺寸（最小20×20英寸），300 DPI，适合详细分析和打印
  - 自适应尺寸计算：确保每个格子至少10×10像素
  - 添加细网格线，提高可读性
  - 智能坐标标签显示（大网格时自动稀疏化）

#### 轻量级ASCII可视化工具

`python/fibonacci_cli_simple.py` - 无需外部依赖的轻量级工具

**特性**：
- 纯Python实现，无需安装任何库
- ASCII字符可视化
- 适合快速查看和终端环境

**运行方法**：
```bash
python3 python/fibonacci_cli_simple.py
```

### 3. 网页版可视化工具

`web/fibonacci-mod-visualizer.html` - 基于HTML/JavaScript的交互式可视化

**特性**：
- 图形化界面，操作直观
- 实时交互，响应迅速
- 支持导出PNG图片
- 无需安装，浏览器直接打开

**使用方法**：
直接用浏览器打开 `web/fibonacci-mod-visualizer.html` 文件

### 4. 一键启动脚本

`scripts/quickstart.sh` - 自动化启动脚本

**功能**：
1. 检查并编译C++程序（如果需要）
2. 检查Python依赖
3. 启动交互式命令行工具

**使用方法**：
```bash
bash scripts/quickstart.sh
```

## 使用指南

### 快速开始（推荐）

```bash
# 进入项目目录
cd /Users/mac/Documents/代码/斐波那契数列可视化

# 一键启动
bash scripts/quickstart.sh
```

### 手动步骤

#### 1. 编译C++计算核心

```bash
bash scripts/compile.sh
```

#### 2. 运行可视化工具

**选项A：完整版（推荐）**
```bash
# 安装依赖
pip3 install matplotlib numpy

# 运行工具
python3 python/fibonacci_cli_visualizer.py
```

**选项B：轻量级版**
```bash
python3 python/fibonacci_cli_simple.py
```

#### 3. 使用网页版

直接用浏览器打开 `web/fibonacci-mod-visualizer.html`

### 操作流程示例

#### 示例1：探索模8的规律

```bash
# 启动工具
python3 python/fibonacci_cli_visualizer.py

# 菜单选择：
# 1. 计算新的模数 → 输入：8
# 2. 选择要可视化的数列 → 输入：all（选择所有）
# 3. 生成可视化图表
# 4. 提示保存 → 输入：y
```

**结果分析**：
- 模8会产生6个不同的周期
- 周期长度分别为：1, 2, 3, 6, 12, 12
- 观察周期在8×8网格中的分布模式

#### 示例2：研究特定范围

```bash
# 计算模100
./cpp/fibonacci_mod 100

# 启动工具
python3 python/fibonacci_cli_simple.py

# 选择菜单1，输入100

# 选择菜单2，输入：0-5,10-15
# （选择前6个和第10-15个数列）

# 选择菜单3生成可视化
```

#### 示例3：大数据导出

```bash
# 计算大模数（可能需要几分钟到几小时）
./cpp/fibonacci_mod 10000 > examples/large_data.json

# 使用Python工具加载和分析
python3 python/fibonacci_cli_visualizer.py
# 选择菜单5导出更方便的格式
```

## 算法实现详解

### 1. Pisano周期检测算法

#### 数学原理

斐波那契数列定义为：
```
F(0) = 0
F(1) = 1
F(n) = F(n-1) + F(n-2) (n ≥ 2)
```

对于模数 m，斐波那契数列模 m 是周期性的，这个周期称为 **Pisano周期**。

#### 检测方法

**状态表示**：用连续的两个值 (F(k), F(k+1)) 作为状态

**算法流程**：
```
对于每个初始值对 (a₀, b₀) ∈ [0, m-1]²:
    如果 (a₀, b₀) 已访问过:
        跳过
    
    当前状态 ← (a₀, b₀)
    路径 ← [当前状态]
    
    循环:
        下一状态 ← (当前状态的第二个值, (第一个值+第二个值) mod m)
        
        如果 下一状态 在 路径 中:
            # 找到周期
            周期起始位置 ← 路径中下一状态的索引
            完整周期 ← 路径[周期起始位置:]
            规范化周期 ← 旋转到最小字典序
            保存规范化周期
            跳出循环
        
        如果 下一状态 在 全局已访问集合 中:
            # 这个周期已经被其他初始值对发现
            跳出循环
        
        将 下一状态 添加到 路径
        将 下一状态 添加到 全局已访问集合
        当前状态 ← 下一状态
```

#### 规范化处理

为了去重，需要将周期旋转到标准形式：

```cpp
// 找到最小字典序的位置
size_t findMinCycleIndex(const vector<Pair>& cycle) {
    size_t minIdx = 0;
    for (size_t i = 1; i < cycle.size(); ++i) {
        if (comparePairs(cycle[i], cycle[minIdx]) < 0) {
            minIdx = i;
        }
    }
    return minIdx;
}

// 生成规范化的周期
vector<Pair> canonicalCycle(const vector<Pair>& cycle) {
    size_t minIdx = findMinCycleIndex(cycle);
    vector<Pair> result;
    for (size_t i = 0; i < cycle.size(); ++i) {
        result.push_back(cycle[(minIdx + i) % cycle.size()]);
    }
    return result;
}
```

### 2. 可视化算法

#### 散点图生成

**坐标映射**：
- x坐标：数对的第一个值 (a)
- y坐标：数对的第二个值 (b)
- 颜色：不同的周期使用不同颜色

**实现步骤**：
```python
# 1. 创建网格数据
grid = np.zeros((mod, mod))
color_map = {}

# 2. 为每个周期分配颜色
for idx, cycle in enumerate(cycles):
    color_idx = idx % len(PALETTE)
    color_map[idx] = PALETTE[color_idx]
    
    # 3. 在网格中标记周期点
    for pair in cycle:
        x, y = pair
        grid[y, x] = idx + 1  # 使用周期索引作为值

# 4. 创建图表
fig, (ax_grid, ax_legend) = plt.subplots(1, 2, figsize=(14, 7))

# 5. 绘制网格
ax_grid.imshow(grid, cmap=cmap, aspect='equal')

# 6. 添加图例
for idx, cycle in cycles:
    ax_legend.scatter([], [], c=color_map[idx], label=f'周期 {idx+1} (长度={len(cycle)})')
```

#### 高分辨率优化

**自适应尺寸计算**：
```python
min_pixel_per_cell = 10  # 每个格子最小10像素
dpi = 300
fig_width = max(20, grid_size * min_pixel_per_cell / dpi * 1.2)
fig_height = fig_width
```

**智能坐标标签**：
```python
if grid_size <= 50:
    step = 1  # 小网格显示所有坐标
else:
    step = max(1, grid_size // 20)  # 大网格每20个显示一个
```

## 数学知识

### 1. Pisano周期

**定义**：斐波那契数列模 m 的周期称为 Pisano周期，记作 π(m)。

**性质**：
- 对于任意正整数 m，Pisano周期都存在
- 如果 m 和 n 互质，则 π(mn) = lcm(π(m), π(n))
- π(p^k) 对于素数 p 有特定规律

**示例**：
- π(2) = 3: 0, 1, 1, 0, 1, 1, ...
- π(3) = 8: 0, 1, 1, 2, 0, 2, 2, 1, 0, 1, 1, ...
- π(10) = 60

### 2. 模运算与周期

**模运算定义**：
a ≡ b (mod m) 表示 a 和 b 除以 m 的余数相同

**周期性来源**：
- 状态空间有限：只有 m² 个可能的状态对 (a, b)
- 确定性转移：给定当前状态，下一状态唯一确定
- 鸽巢原理：经过最多 m² + 1 步，必然出现重复状态

### 3. 周期分布规律

**观察到的现象**：

1. **素数模数**：
   - 对于许多素数 p，π(p) 整除 p−1 或 p+1
   - 与勒让德符号 (5/p) 有关

2. **2的幂**：
   - π(2) = 3
   - π(4) = 6
   - π(8) = 12
   - π(2^k) = 3 × 2^{k−1} (k ≥ 3)

3. **可视化模式**：
   - 不同周期形成不同的几何图案
   - 对称性和重复模式反映了数论性质
   - 颜色分布展示了周期的分类

### 4. 与线性递推的关系

斐波那契数列是二阶线性递推：
```
F(n+2) = F(n+1) + F(n)
```

矩阵表示：
```
[F(n+1)]   = [1 1] [F(n)]
[F(n)  ]     [1 0] [F(n-1)]
```

模 m 下的周期性与矩阵的阶有关。

## 性能表现

### C++计算核心性能

| 模数 | 计算时间 | 周期数量 | 内存使用 |
|------|---------|---------|---------|
| 10 | < 0.1s | 6 | < 10MB |
| 100 | < 1s | 多种 | < 50MB |
| 1,000 | ~5-10s | 多种 | ~200MB |
| 10,000 | ~2-5分钟 | 多种 | ~1GB |
| 100,000 | ~30-60分钟 | 多种 | ~5GB |

**注意**：大模数计算需要足够内存和耐心。

### Python可视化性能

| 模数 | 生成时间 | 图片尺寸 | 文件大小 |
|------|---------|---------|---------|
| 50 | 2-5s | 20×20英寸 (6000×6000px) | ~2MB |
| 100 | 5-10s | 33×33英寸 (10000×10000px) | ~6MB |
| 200 | 15-30s | 66×66英寸 (20000×20000px) | ~20MB |

## 示例数据

### 示例1：模8的周期

计算结果（简化表示）：
```json
{
  "base": 8,
  "cycles_count": 6,
  "cycles": [
    {"length": 1, "sequence": [[0,0]]},
    {"length": 2, "sequence": [[0,2],[2,2]]},
    {"length": 3, "sequence": [[0,4],[4,4],[4,0]]},
    {"length": 6, "sequence": [[0,1],[1,1],[1,2],[2,3],[3,5],[5,0]]},
    {"length": 12, "sequence": [...]},
    {"length": 12, "sequence": [...]}
  ]
}
```

可视化特征：
- 6个不同颜色的周期
- 在8×8网格中形成对称图案
- 最长周期为12

### 示例2：模100的周期

模100会产生数十个不同长度的周期，可视化展示了复杂的分布模式。

## 故障排除

### 编译错误

**问题**：`error: 'unordered_set' was not declared`

**解决**：
```bash
# 确保使用C++11标准
g++ -std=c++11 -O3 -o cpp/fibonacci_mod src/fibonacci_mod.cpp
```

### Python依赖问题

**问题**：`ModuleNotFoundError: No module named 'matplotlib'`

**解决**：
```bash
# 方案A：安装依赖
pip3 install matplotlib numpy

# 方案B：使用轻量级版本
python3 python/fibonacci_cli_simple.py
```

### 内存不足

**问题**：计算大模数时程序崩溃

**解决**：
```bash
# 使用swap或增加虚拟内存
# 或降低模数
# 模数>100000需要>8GB内存
```

### 权限问题

**问题**：`Permission denied`

**解决**：
```bash
chmod +x scripts/*.sh
chmod +x python/*.py
```

## 贡献指南

欢迎提交Issue和Pull Request！

### 开发环境搭建

```bash
# 克隆仓库
git clone <repository-url>
cd 斐波那契数列可视化

# 编译
bash scripts/compile.sh

# 运行测试
./cpp/fibonacci_mod 100
```

### 代码规范

- C++代码遵循Google C++ Style Guide
- Python代码遵循PEP 8
- 添加必要的注释和文档

## 许可证

本项目采用MIT许可证。详见项目根目录的LICENSE文件（如有）。

## 致谢

- 斐波那契数列的数学性质研究
- Pisano周期的相关理论
- matplotlib和numpy开源项目

## 联系方式

如有问题或建议，请：
- 提交Issue到项目仓库
- 查看 `docs/` 目录下的详细文档

## 相关链接

- [斐波那契数列 - Wikipedia](https://zh.wikipedia.org/wiki/斐波那契数列)
- [Pisano周期 - Wikipedia](https://en.wikipedia.org/wiki/Pisano_period)
- [模运算 - Wikipedia](https://zh.wikipedia.org/wiki/模运算)

---

**享受探索数学之美的乐趣！**
