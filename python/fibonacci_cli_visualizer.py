#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
斐波那契数列模周期 - 命令行交互式可视化工具

使用方法:
    python3 fibonacci_cli_visualizer.py
    
功能:
    - 交互式输入模数
    - 选择要可视化的数列范围
    - 生成与网页版相同的可视化图表
    - 支持导出为PNG图片
"""

import json
import subprocess
import sys
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np
from datetime import datetime

# 颜色调色板（与网页版一致）
PALETTE = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728',
    '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
    '#bcbd22', '#17becf', '#393b79', '#637939'
]

class FibonacciVisualizer:
    def __init__(self):
        self.base = None
        self.sequences = []
        self.cycles_pairs = []
        self.selected_sequences = set()
        
    def clear_screen(self):
        """清屏"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """打印欢迎横幅"""
        self.clear_screen()
        print("=" * 70)
        print("  斐波那契数列模周期 - 高性能计算与可视化工具")
        print("=" * 70)
        print()
    
    def check_executable(self):
        """检查C++可执行文件是否存在"""
        if not os.path.exists('./cpp/fibonacci_mod'):
            print("错误: 找不到C++可执行文件 'cpp/fibonacci_mod'")
            print("请先编译C++程序:")
            print("  bash scripts/compile.sh")
            print("或:")
            print("  g++ -std=c++11 -O3 -o cpp/fibonacci_mod src/fibonacci_mod.cpp")
            return False
        return True
    
    def run_cpp_program(self, base):
        """运行C++程序并获取结果"""
        print(f"\n正在计算模 {base} 的斐波那契周期...")
        print("这可能需要一些时间，请耐心等待...\n")
        
        try:
            # 运行C++程序
            result = subprocess.run(
                ['./fibonacci_mod', str(base)],
                capture_output=True,
                text=True,
                timeout=3600  # 1小时超时
            )
            
            if result.returncode != 0:
                print(f"错误: C++程序执行失败")
                print(f"错误信息: {result.stderr}")
                return False
            
            # 解析JSON输出
            data = json.loads(result.stdout)
            
            self.base = data['base']
            self.sequences = data['sequences']
            self.cycles_pairs = data['cycles_pairs']
            
            print(f"✓ 计算完成！")
            print(f"  - 模数: {self.base}")
            print(f"  - 找到 {len(self.sequences)} 个不同的周期")
            print()
            
            return True
            
        except subprocess.TimeoutExpired:
            print("错误: 计算超时（超过1小时）")
            return False
        except json.JSONDecodeError as e:
            print(f"错误: 无法解析JSON数据: {e}")
            return False
        except Exception as e:
            print(f"错误: {e}")
            return False
    
    def parse_range_input(self, input_str):
        """解析用户输入的范围，如 '3-5,6,7-21'"""
        selected = set()
        
        try:
            # 分割逗号
            parts = input_str.strip().split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # 范围格式: 3-5
                    start, end = part.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    if start < 0 or end >= len(self.sequences):
                        print(f"警告: 范围 {start}-{end} 超出有效范围 [0, {len(self.sequences)-1}]")
                        continue
                    
                    selected.update(range(start, end + 1))
                else:
                    # 单个数字: 6
                    idx = int(part)
                    if idx < 0 or idx >= len(self.sequences):
                        print(f"警告: 索引 {idx} 超出有效范围 [0, {len(self.sequences)-1}]")
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
            color = PALETTE[idx % len(PALETTE)]
            selected_mark = "✓" if idx in self.selected_sequences else " "
            
            # 截断长序列显示
            seq_str = str(seq)
            if len(seq_str) > 60:
                seq_str = seq_str[:60] + "..."
            
            print(f"[{selected_mark}] {idx:3d}. 长度={len(seq):3d} | {seq_str}")
        
        print("=" * 70)
    
    def select_sequences_interactive(self):
        """交互式选择数列"""
        if not self.sequences:
            print("错误: 没有可用的数列")
            return
        
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
                # 解析范围输入
                indices = self.parse_range_input(choice)
                if indices is not None:
                    self.selected_sequences.update(indices)
                    print(f"已选择 {len(indices)} 个数列")
            
            input("\n按回车继续...")
    
    def generate_visualization(self):
        """生成可视化图表（两张图：正常版和高清版）"""
        if not self.selected_sequences:
            print("错误: 没有选择任何数列")
            return
        
        if self.base is None or not self.sequences:
            print("错误: 没有可用的数据，请先计算模数")
            return
        
        print("\n正在生成可视化图表...")
        print(f"  - 模数: {self.base}")
        print(f"  - 选择的数列数: {len(self.selected_sequences)}")
        
        # 创建网格数据
        grid_size = self.base
        grid_data = np.zeros((grid_size, grid_size, 3))
        
        # 用于存储每个数列的信息
        sequence_info = []
        
        # 填充网格
        for idx in self.selected_sequences:
            if idx >= len(self.sequences):
                continue
            
            seq = self.sequences[idx]
            color = PALETTE[idx % len(PALETTE)]
            
            # 将颜色从hex转换为RGB
            rgb_color = tuple(int(color[i:i+2], 16) / 255 for i in (1, 3, 5))
            
            # 生成坐标对
            pairs = []
            for i in range(len(seq)):
                a = seq[i]
                b = seq[(i + 1) % len(seq)]
                pairs.append((a, b))
            
            # 在网格中标记
            for x, y in pairs:
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    grid_data[y, x] = rgb_color
            
            # 保存数列信息用于图例
            sequence_info.append({
                'index': idx,
                'length': len(seq),
                'color': color,
                'preview': str(seq[:8])[:-1] + '...]' if len(seq) > 8 else str(seq)
            })
        
        # ========== 第一张图：正常大小 ==========
        print("\n生成图1: 正常尺寸...")
        fig1, (ax_grid1, ax_legend1) = plt.subplots(
            1, 2, 
            figsize=(14, 7),
            gridspec_kw={'width_ratios': [3, 1]}
        )
        
        # 绘制网格
        ax_grid1.imshow(grid_data, interpolation='nearest')
        ax_grid1.set_title(f'斐波那契数列 Mod {self.base} 周期可视化', fontsize=14, fontweight='bold')
        ax_grid1.set_xlabel('X 坐标')
        ax_grid1.set_ylabel('Y 坐标')
        ax_grid1.grid(True, alpha=0.3)
        
        # 添加坐标标签
        if grid_size <= 20:
            ax_grid1.set_xticks(range(grid_size))
            ax_grid1.set_yticks(range(grid_size))
            ax_grid1.set_xticklabels(range(grid_size))
            ax_grid1.set_yticklabels(range(grid_size))
        else:
            step = max(1, grid_size // 10)
            ax_grid1.set_xticks(range(0, grid_size, step))
            ax_grid1.set_yticks(range(0, grid_size, step))
            ax_grid1.set_xticklabels(range(0, grid_size, step))
            ax_grid1.set_yticklabels(range(0, grid_size, step))
        
        # 绘制图例
        ax_legend1.axis('off')
        ax_legend1.set_title('数列信息', fontsize=12, fontweight='bold')
        
        legend_text1 = f"模数: {self.base}\n"
        legend_text1 += f"总数列: {len(self.sequences)}\n"
        legend_text1 += f"已选择: {len(self.selected_sequences)}\n\n"
        
        for i, info in enumerate(sequence_info[:20]):
            legend_text1 += f"[{info['index']}] 长度={info['length']}\n"
            legend_text1 += f"    {info['preview']}\n"
        
        if len(sequence_info) > 20:
            legend_text1 += f"\n... 还有 {len(sequence_info) - 20} 个数列"
        
        legend_text1 += f"\n生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        ax_legend1.text(0.05, 0.95, legend_text1, 
                       transform=ax_legend1.transAxes, 
                       fontsize=9, 
                       verticalalignment='top',
                       fontfamily='monospace',
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.5))
        
        plt.tight_layout()
        
        # ========== 第二张图：高分辨率大图 ==========
        print("生成图2: 高分辨率大图...")
        
        # 大模数警告
        if grid_size > 200:
            print(f"  ⚠️  警告: 模数 {grid_size} 较大，生成高分辨率图可能:")
            print(f"     - 消耗大量内存 (预计 > 2GB)")
            print(f"     - 需要较长时间 (可能 > 30秒)")
            print(f"     - 生成大文件 (可能 > 10MB)")
            
            confirm = input("  是否继续生成? (y/n): ").strip().lower()
            if confirm != 'y':
                print("  已跳过高清图生成")
                # 只显示第一张图
                try:
                    plt.show(block=True)
                except Exception as e:
                    print(f"警告: 显示图表时出现问题: {e}")
                
                # 询问是否保存
                save_choice = input("\n是否保存图表为PNG文件? (y/n): ").strip().lower()
                if save_choice == 'y':
                    try:
                        filename1 = f"output/fibonacci_mod_{self.base}_visualization.png"
                        fig1.savefig(filename1, dpi=150, bbox_inches='tight')
                        print(f"✓ 图1已保存为: {filename1}")
                    except Exception as e:
                        print(f"错误: 保存图片失败: {e}")
                
                try:
                    plt.close('all')
                except:
                    pass
                
                return
        
        # 根据网格大小计算合适的图形尺寸
        # 确保每个格子至少能被清晰看到（最小10x10像素）
        min_pixel_per_cell = 10
        dpi = 300  # 高DPI
        fig_width = max(20, grid_size * min_pixel_per_cell / dpi * 1.2)  # 留20%边距
        fig_height = fig_width  # 正方形
        
        print(f"  - 图形尺寸: {fig_width:.1f}x{fig_height:.1f} 英寸")
        print(f"  - 分辨率: {int(fig_width * dpi)}x{int(fig_height * dpi)} 像素")
        
        fig2 = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
        
        # 主网格区域（占85%宽度）
        ax_grid2 = plt.subplot2grid((1, 20), (0, 0), colspan=17, fig=fig2)
        
        # 图例区域（占15%宽度）
        ax_legend2 = plt.subplot2grid((1, 20), (0, 17), colspan=3, fig=fig2)
        
        # 绘制高分辨率网格
        im = ax_grid2.imshow(grid_data, interpolation='nearest')
        
        # 添加网格线，确保每个格子清晰可见
        ax_grid2.set_xticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax_grid2.set_yticks(np.arange(-0.5, grid_size, 1), minor=True)
        ax_grid2.grid(which='minor', color='gray', linestyle='-', linewidth=0.5, alpha=0.3)
        
        # 设置标题和标签
        ax_grid2.set_title(f'斐波那契数列 Mod {self.base} 周期可视化 (高分辨率)', 
                          fontsize=16, fontweight='bold', pad=20)
        ax_grid2.set_xlabel('X 坐标', fontsize=12)
        ax_grid2.set_ylabel('Y 坐标', fontsize=12)
        
        # 添加坐标标签（小网格时显示所有，大网格时显示主要刻度）
        if grid_size <= 50:
            # 小网格：显示所有坐标
            step = 1
            ax_grid2.set_xticks(range(0, grid_size, step))
            ax_grid2.set_yticks(range(0, grid_size, step))
            ax_grid2.set_xticklabels(range(0, grid_size, step), fontsize=8)
            ax_grid2.set_yticklabels(range(0, grid_size, step), fontsize=8)
        else:
            # 大网格：只显示主要刻度，避免过于密集
            step = max(1, grid_size // 20)
            ax_grid2.set_xticks(range(0, grid_size, step))
            ax_grid2.set_yticks(range(0, grid_size, step))
            ax_grid2.set_xticklabels(range(0, grid_size, step), fontsize=8)
            ax_grid2.set_yticklabels(range(0, grid_size, step), fontsize=8)
        
        # 绘制图例
        ax_legend2.axis('off')
        ax_legend2.set_title('数列信息', fontsize=14, fontweight='bold')
        
        # 图例文本（调整字体大小）
        legend_text2 = f"模数: {self.base}\n"
        legend_text2 += f"总数列: {len(self.sequences)}\n"
        legend_text2 += f"已选择: {len(self.selected_sequences)}\n\n"
        
        for i, info in enumerate(sequence_info[:15]):  # 高分辨率图显示少些，避免溢出
            legend_text2 += f"[{info['index']}] 长度={info['length']}\n"
            preview = info['preview']
            if len(preview) > 25:
                preview = preview[:25] + '...]'
            legend_text2 += f"    {preview}\n"
        
        if len(sequence_info) > 15:
            legend_text2 += f"\n... 还有 {len(sequence_info) - 15} 个数列"
        
        legend_text2 += f"\n分辨率: {grid_size}x{grid_size}\n"
        legend_text2 += f"DPI: {dpi}\n"
        legend_text2 += f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        ax_legend2.text(0.05, 0.95, legend_text2, 
                       transform=ax_legend2.transAxes, 
                       fontsize=10, 
                       verticalalignment='top',
                       fontfamily='monospace',
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.5))
        
        plt.tight_layout()
        
        # ========== 显示和保存 ==========
        print("\n✓ 图表生成完成！")
        print("  - 关闭图表窗口以返回菜单")
        
        try:
            plt.show(block=True)
        except Exception as e:
            print(f"警告: 显示图表时出现问题: {e}")
            print("  但图表文件仍然可以保存。")
        
        # 询问是否保存
        save_choice = input("\n是否保存图表为PNG文件? (y/n): ").strip().lower()
        if save_choice == 'y':
            try:
                # 保存正常尺寸图
                filename1 = f"fibonacci_mod_{self.base}_visualization.png"
                fig1.savefig(filename1, dpi=150, bbox_inches='tight')
                print(f"✓ 图1已保存为: {filename1}")
                
                # 保存高分辨率大图
                filename2 = f"fibonacci_mod_{self.base}_highres.png"
                fig2.savefig(filename2, dpi=dpi, bbox_inches='tight')
                print(f"✓ 图2（高分辨率）已保存为: {filename2}")
                print(f"  - 尺寸: {fig_width:.1f}x{fig_height:.1f} 英寸")
                print(f"  - DPI: {dpi}")
                print(f"  - 像素: {int(fig_width * dpi)}x{int(fig_height * dpi)}")
            except Exception as e:
                print(f"错误: 保存图片失败: {e}")
        
        # 清理内存
        try:
            plt.close('all')
            print("  - 已清理内存")
        except:
            pass
    
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
            print("3. 生成可视化图表")
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
                    self.generate_visualization()
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
                    filename = f"examples/fibonacci_mod_{self.base}_data.json"
                    with open(filename, 'w') as f:
                        json.dump({
                            'base': self.base,
                            'sequences': self.sequences,
                            'cycles_pairs': self.cycles_pairs,
                            'selected_sequences': sorted(list(self.selected_sequences))
                        }, f, indent=2)
                    print(f"✓ 数据已导出到: {filename}")
                    input("\n按回车继续...")
            else:
                print("错误: 无效的选择")
                input("\n按回车继续...")


def main():
    """主函数"""
    # 检查Python版本
    if sys.version_info < (3, 6):
        print("错误: 需要Python 3.6或更高版本")
        sys.exit(1)
    
    # 检查matplotlib
    try:
        import matplotlib
    except ImportError:
        print("错误: 需要matplotlib库")
        print("请安装: pip3 install matplotlib")
        sys.exit(1)
    
    # 创建可视化器并运行
    visualizer = FibonacciVisualizer()
    visualizer.main_menu()


if __name__ == "__main__":
    main()
