#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
斐波那契数列模周期 - 命令行轻量级可视化工具

无需外部依赖，使用纯Python和ASCII字符进行可视化
"""

import json
import subprocess
import sys
import os

# 颜色代码（终端颜色）
COLORS = [
    '\033[91m',  # 红色
    '\033[92m',  # 绿色
    '\033[93m',  # 黄色
    '\033[94m',  # 蓝色
    '\033[95m',  # 紫色
    '\033[96m',  # 青色
    '\033[31m',  # 深红
    '\033[32m',  # 深绿
    '\033[33m',  # 深黄
    '\033[34m',  # 深蓝
    '\033[35m',  # 深紫
    '\033[36m',  # 深青
]

RESET_COLOR = '\033[0m'
BOLD = '\033[1m'

class FibonacciCLI:
    def __init__(self):
        self.base = None
        self.sequences = []
        self.selected_sequences = set()
    
    def clear_screen(self):
        """清屏"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """打印欢迎横幅"""
        self.clear_screen()
        print("=" * 70)
        print(f"{BOLD}斐波那契数列模周期 - 命令行可视化工具{RESET_COLOR}")
        print("=" * 70)
        print()
    
    def check_executable(self):
        """检查C++可执行文件是否存在"""
        if not os.path.exists('./fibonacci_mod'):
            print("错误: 找不到C++可执行文件 'fibonacci_mod'")
            print("请先编译C++程序:")
            print("  bash compile.sh")
            return False
        return True
    
    def run_cpp_program(self, base):
        """运行C++程序并获取结果"""
        print(f"\n正在计算模 {base} 的斐波那契周期...")
        print("这可能需要一些时间，请耐心等待...\n")
        
        try:
            result = subprocess.run(
                ['./fibonacci_mod', str(base)],
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            if result.returncode != 0:
                print(f"错误: C++程序执行失败")
                print(f"错误信息: {result.stderr}")
                return False
            
            # 解析JSON输出
            lines = result.stdout.strip().split('\n')
            json_start = -1
            for i, line in enumerate(lines):
                if line.strip().startswith('{'):
                    json_start = i
                    break
            
            if json_start == -1:
                print("错误: 无法找到JSON数据")
                return False
            
            json_data = '\n'.join(lines[json_start:])
            data = json.loads(json_data)
            
            self.base = data['base']
            self.sequences = data['sequences']
            
            print(f"✓ 计算完成！")
            print(f"  - 模数: {self.base}")
            print(f"  - 找到 {len(self.sequences)} 个不同的周期")
            print()
            
            return True
            
        except Exception as e:
            print(f"错误: {e}")
            return False
    
    def parse_range_input(self, input_str):
        """解析用户输入的范围"""
        selected = set()
        
        try:
            parts = input_str.strip().split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    start, end = part.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    if start < 0 or end >= len(self.sequences):
                        print(f"警告: 范围 {start}-{end} 超出有效范围 [0, {len(self.sequences)-1}]")
                        continue
                    
                    selected.update(range(start, end + 1))
                else:
                    idx = int(part)
                    if idx < 0 or idx >= len(self.sequences):
                        print(f"警告: 索引 {idx} 超出有效范围")
                        continue
                    selected.add(idx)
            
            return sorted(list(selected))
            
        except ValueError:
            print("错误: 无效的输入格式")
            return None
    
    def display_sequences(self):
        """显示所有数列"""
        print("\n" + "=" * 70)
        print(f"所有数列 (共 {len(self.sequences)} 个):")
        print("=" * 70)
        
        for idx, seq in enumerate(self.sequences):
            color = COLORS[idx % len(COLORS)]
            selected_mark = "✓" if idx in self.selected_sequences else " "
            
            seq_str = str(seq)
            if len(seq_str) > 50:
                seq_str = seq_str[:50] + "..."
            
            print(f"{color}[{selected_mark}] {idx:3d}. 长度={len(seq):3d} | {seq_str}{RESET_COLOR}")
        
        print("=" * 70)
    
    def generate_ascii_visualization(self):
        """生成ASCII字符可视化"""
        if not self.selected_sequences:
            print("错误: 没有选择任何数列")
            return
        
        print("\n" + "=" * 70)
        print(f"{BOLD}可视化图表 (模 {self.base}){RESET_COLOR}")
        print("=" * 70)
        
        # 创建网格
        grid_size = self.base
        grid = [['  ' for _ in range(grid_size)] for _ in range(grid_size)]
        grid_colors = [[-1 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # 填充网格
        for idx in self.selected_sequences:
            if idx >= len(self.sequences):
                continue
            
            seq = self.sequences[idx]
            color_idx = idx % len(COLORS)
            
            # 生成坐标对
            for i in range(len(seq)):
                x = seq[i]
                y = seq[(i + 1) % len(seq)]
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    grid[y][x] = f'{color_idx:2d}'
                    grid_colors[y][x] = color_idx
        
        # 显示网格
        print(f"\n{BOLD}图例:{RESET_COLOR}")
        legend_line = ""
        for idx in sorted(self.selected_sequences):
            if idx >= len(self.sequences):
                continue
            color_idx = idx % len(COLORS)
            seq_len = len(self.sequences[idx])
            legend_line += f"{COLORS[color_idx]}[{idx}]({seq_len}){RESET_COLOR} "
        print(legend_line)
        print()
        
        # 打印网格
        if grid_size <= 20:
            # 小网格：显示完整
            print(f"{BOLD}  ", end="")
            for x in range(grid_size):
                print(f"{x:2d}", end="")
            print(f"{RESET_COLOR}")
            
            for y in range(grid_size-1, -1, -1):
                print(f"{BOLD}{y:2d}{RESET_COLOR}", end="")
                for x in range(grid_size):
                    color_idx = grid_colors[y][x]
                    if color_idx >= 0:
                        print(f"{COLORS[color_idx]}██{RESET_COLOR}", end="")
                    else:
                        print("░░", end="")
                print()
        elif grid_size <= 50:
            # 中等网格：简化显示
            step = max(1, grid_size // 40)
            for y in range(grid_size-1, -1, -step):
                for x in range(0, grid_size, step):
                    color_idx = grid_colors[y][x]
                    if color_idx >= 0:
                        print(f"{COLORS[color_idx]}██{RESET_COLOR}", end="")
                    else:
                        print("░░", end="")
                print()
        else:
            # 大网格：只显示密度
            print(f"网格太大 ({grid_size}x{grid_size})，显示简化版本:")
            step = max(1, grid_size // 40)
            filled = 0
            total = 0
            
            for y in range(grid_size-1, -1, -step):
                for x in range(0, grid_size, step):
                    total += 1
                    color_idx = grid_colors[y][x]
                    if color_idx >= 0:
                        filled += 1
                        print(f"{COLORS[color_idx]}██{RESET_COLOR}", end="")
                    else:
                        print("░░", end="")
                print()
            
            print(f"\n填充率: {filled}/{total} ({filled/total*100:.1f}%)")
        
        print("=" * 70)
        print("提示: ██ 表示有数据，░░ 表示空")
        print("=" * 70)
    
    def select_sequences_interactive(self):
        """交互式选择数列"""
        while True:
            self.display_sequences()
            
            print("\n选择要可视化的数列:")
            print("  - 输入范围，如: 3-5,6,7-21")
            print("  - 输入 'all' 选择所有数列")
            print("  - 输入 'clear' 清空选择")
            print("  - 输入 'done' 完成选择")
            print("  - 输入 'back' 返回主菜单")
            
            choice = input("\n请输入: ").strip().lower()
            
            if choice == 'back':
                return False
            elif choice == 'done':
                if not self.selected_sequences:
                    print("警告: 没有选择任何数列")
                    continue
                return True
            elif choice == 'clear':
                self.selected_sequences.clear()
                print("已清空所有选择")
            elif choice == 'all':
                self.selected_sequences = set(range(len(self.sequences)))
                print(f"已选择所有 {len(self.sequences)} 个数列")
            else:
                indices = self.parse_range_input(choice)
                if indices is not None:
                    self.selected_sequences.update(indices)
                    print(f"已选择 {len(indices)} 个数列")
            
            input("\n按回车继续...")
    
    def main_menu(self):
        """主菜单"""
        while True:
            self.print_banner()
            
            if self.base is None:
                print("当前状态: 未计算")
            else:
                print(f"当前状态: 模数={self.base}, 数列数={len(self.sequences)}")
                print(f"已选择: {len(self.selected_sequences)} 个数列")
            
            print("\n" + "=" * 70)
            print("主菜单:")
            print("=" * 70)
            print("1. 计算新的模数")
            print("2. 选择要可视化的数列")
            print("3. 生成ASCII可视化")
            print("4. 查看数列详情")
            print("5. 导出数据为JSON")
            print("0. 退出")
            print("=" * 70)
            
            choice = input("\n请选择 (0-5): ").strip()
            
            if choice == '0':
                print("\n感谢使用！再见！")
                break
            elif choice == '1':
                try:
                    base = int(input("请输入模数 (1-1000000): ").strip())
                    if base < 1 or base > 1000000:
                        print("错误: 模数必须在1-1000000之间")
                        input("\n按回车继续...")
                        continue
                    
                    if not self.check_executable():
                        input("\n按回车继续...")
                        continue
                    
                    if self.run_cpp_program(base):
                        self.selected_sequences.clear()
                        print("\n✓ 计算成功！")
                    else:
                        print("\n✗ 计算失败！")
                    
                    input("\n按回车继续...")
                except ValueError:
                    print("错误: 请输入有效的整数")
                    input("\n按回车继续...")
            elif choice == '2':
                if self.base is None:
                    print("错误: 请先计算一个模数")
                    input("\n按回车继续...")
                else:
                    self.select_sequences_interactive()
            elif choice == '3':
                if self.base is None:
                    print("错误: 请先计算一个模数")
                    input("\n按回车继续...")
                elif not self.selected_sequences:
                    print("错误: 请先选择要可视化的数列")
                    input("\n按回车继续...")
                else:
                    self.generate_ascii_visualization()
                    input("\n按回车继续...")
            elif choice == '4':
                if self.base is None:
                    print("错误: 请先计算一个模数")
                else:
                    self.display_sequences()
                    input("\n按回车继续...")
            elif choice == '5':
                if self.base is None:
                    print("错误: 请先计算一个模数")
                else:
                    filename = f"fibonacci_mod_{self.base}_data.json"
                    with open(filename, 'w') as f:
                        json.dump({
                            'base': self.base,
                            'sequences': self.sequences,
                            'selected_sequences': sorted(list(self.selected_sequences))
                        }, f, indent=2)
                    print(f"✓ 数据已导出到: {filename}")
                    input("\n按回车继续...")
            else:
                print("错误: 无效的选择")
                input("\n按回车继续...")


def main():
    """主函数"""
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)
    
    cli = FibonacciCLI()
    cli.main_menu()


if __name__ == "__main__":
    main()