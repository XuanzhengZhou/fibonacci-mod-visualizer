#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fibonacci Sequence Modulo Period - Command Line Interactive Visualization Tool

Usage:
    python3 fibonacci_cli_visualizer.py
    
Features:
    - Interactive input of modulo
    - Select sequence ranges to visualize
    - Generate visualization charts same as the web version
    - Support export to PNG images
"""

import json
import subprocess
import sys
import os
import colorsys
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np
from datetime import datetime

# Color palette (consistent with web version)
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
        """Clear screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_banner(self):
        """Print welcome banner"""
        self.clear_screen()
        print("=" * 70)
        print("  Fibonacci Sequence Modulo Period - High Performance Calculation and Visualization Tool")
        print("=" * 70)
        print()
    
    def check_executable(self):
        """Check if C++ executable exists"""
        if not os.path.exists('../cpp/fibonacci_mod'):
            print("Error: Cannot find C++ executable 'cpp/fibonacci_mod'")
            print("Please compile the C++ program first:")
            print("  bash scripts/compile.sh")
            print("or:")
            print("  g++ -std=c++11 -O3 -o cpp/fibonacci_mod src/fibonacci_mod.cpp")
            return False
        return True
    
    def run_cpp_program(self, base):
        """Run C++ program and get results"""
        print(f"\nCalculating Fibonacci periods for modulo {base}...")
        print("This may take some time, please wait...\n")
        
        try:
            # Run C++ program
            result = subprocess.run(
                ['../cpp/fibonacci_mod', str(base)],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode != 0:
                print(f"Error: C++ program execution failed")
                print(f"Error message: {result.stderr}")
                return False
            
            # Parse JSON output
            data = json.loads(result.stdout)
            
            self.base = data['base']
            self.sequences = data['sequences']
            self.cycles_pairs = data['cycles_pairs']
            
            print(f"✓ Calculation completed!")
            print(f"  - Modulo: {self.base}")
            print(f"  - Found {len(self.sequences)} different periods")
            print()
            
            return True
            
        except subprocess.TimeoutExpired:
            print("Error: Calculation timed out (over 1 hour)")
            return False
        except json.JSONDecodeError as e:
            print(f"Error: Cannot parse JSON data: {e}")
            return False
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    def parse_range_input(self, input_str):
        """Parse user input range, such as '3-5,6,7-21'"""
        selected = set()
        
        try:
            # Split by commas
            parts = input_str.strip().split(',')
            
            for part in parts:
                part = part.strip()
                if '-' in part:
                    # Range format: 3-5
                    start, end = part.split('-')
                    start = int(start.strip())
                    end = int(end.strip())
                    
                    if start < 0 or end >= len(self.sequences):
                        print(f"Warning: Range {start}-{end} exceeds valid range [0, {len(self.sequences)-1}]")
                        continue
                    
                    selected.update(range(start, end + 1))
                else:
                    # Single number: 6
                    idx = int(part)
                    if idx < 0 or idx >= len(self.sequences):
                        print(f"Warning: Index {idx} exceeds valid range [0, {len(self.sequences)-1}]")
                        continue
                    selected.add(idx)
            
            return sorted(list(selected))
            
        except ValueError:
            print("Error: Invalid input format")
            return None
    
    def display_sequences(self):
        """Display all sequences"""
        print("\n" + "=" * 70)
        print(f"All Sequences (Total {len(self.sequences)}):")
        print("=" * 70)
        
        for idx, seq in enumerate(self.sequences):
            color = PALETTE[idx % len(PALETTE)]
            selected_mark = "✓" if idx in self.selected_sequences else " "
            
            # Truncate long sequence display
            seq_str = str(seq)
            if len(seq_str) > 60:
                seq_str = seq_str[:60] + "..."
            
            print(f"[{selected_mark}] {idx:3d}. Length={len(seq):3d} | {seq_str}")
        
        print("=" * 70)
    
    def select_sequences_interactive(self):
        """Interactively select sequences"""
        if not self.sequences:
            print("Error: No available sequences")
            return
        
        while True:
            self.display_sequences()
            
            print("\nSelect sequences to visualize:")
            print("  - Enter range, e.g.: 3-5,6,7-21")
            print("  - Enter 'all' to select all sequences")
            print("  - Enter 'clear' to clear selection")
            print("  - Enter 'done' to finish selection")
            print("  - Enter 'back' to return to main menu")
            
            choice = input("\nPlease enter: ").strip().lower()
            
            if choice == 'back':
                return False
            elif choice == 'done':
                if not self.selected_sequences:
                    print("Warning: No sequences selected")
                    continue
                return True
            elif choice == 'clear':
                self.selected_sequences.clear()
                print("Cleared all selections")
            elif choice == 'all':
                self.selected_sequences = set(range(len(self.sequences)))
                print(f"Selected all {len(self.sequences)} sequences")
            else:
                # Parse range input
                indices = self.parse_range_input(choice)
                if indices is not None:
                    self.selected_sequences.update(indices)
                    print(f"Selected {len(indices)} sequences")
            
            input("\nPress Enter to continue...")
    
    def generate_visualization(self):
        """Generate visualization charts (two charts: normal and high definition)"""
        if not self.selected_sequences:
            print("Error: No sequences selected")
            return
        
        if self.base is None or not self.sequences:
            print("Error: No available data, please calculate modulo first")
            return
        
        print("\nGenerating visualization charts...")
        print(f"  - Modulo: {self.base}")
        print(f"  - Number of selected sequences: {len(self.selected_sequences)}")
        
        # Create grid data
        grid_size = self.base
        grid_data = np.zeros((grid_size, grid_size, 3))
        
        # Information for storing each sequence
        sequence_info = []
        
        # Find the maximum sequence length to normalize color intensity
        max_length = max(len(self.sequences[idx]) for idx in self.selected_sequences if idx < len(self.sequences))
        min_length = min(len(self.sequences[idx]) for idx in self.selected_sequences if idx < len(self.sequences))
        
        # Fill the grid
        for idx in self.selected_sequences:
            if idx >= len(self.sequences):
                continue
            
            seq = self.sequences[idx]
            # Calculate color intensity based on sequence length (shorter = more vivid)
            seq_length = len(seq)
            # Normalize the length to a 0-1 range where shorter sequences have higher intensity
            if max_length == min_length:
                intensity = 1.0  # If all selected sequences have the same length, use max intensity
            else:
                # Invert the ratio so shorter sequences get higher intensity values
                intensity = 1.0 - ((seq_length - min_length) / (max_length - min_length))
            
            # Apply a power function to adjust contrast - using a value closer to 1 for smoother transition
            intensity = intensity ** 0.95  # Very close to linear for very smooth transition
            
            # Get base color from palette
            base_color = PALETTE[idx % len(PALETTE)]
            base_rgb = tuple(int(base_color[i:i+2], 16) / 255 for i in (1, 3, 5))
            
            # Adjust the color based on intensity to make shorter sequences more vivid
            # For vividness, we'll increase saturation for shorter sequences and decrease for longer ones
            # Convert RGB to HSV to manipulate saturation
            import colorsys
            h, s, v = colorsys.rgb_to_hsv(*base_rgb)
            # Adjust saturation and value (brightness) based on intensity
            # Higher intensity (shorter sequences) = higher saturation and brightness
            adjusted_s = s * (0.8 + 0.2 * intensity)  # Very subtle change in saturation
            adjusted_v = v * (0.85 + 0.15 * intensity)  # Very subtle change in brightness
            # Convert back to RGB
            r, g, b = colorsys.hsv_to_rgb(h, adjusted_s, adjusted_v)
            rgb_color = (r, g, b)
            
            # Generate coordinate pairs
            pairs = []
            for i in range(len(seq)):
                a = seq[i]
                b = seq[(i + 1) % len(seq)]
                pairs.append((a, b))
            
            # Mark in the grid
            for x, y in pairs:
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    grid_data[y, x] = rgb_color
            
            # Convert RGB color back to hex for the legend
            hex_color = '#{:02x}{:02x}{:02x}'.format(
                int(rgb_color[0] * 255), 
                int(rgb_color[1] * 255), 
                int(rgb_color[2] * 255)
            )
            
            # Save sequence information for legend
            sequence_info.append({
                'index': idx,
                'length': len(seq),
                'color': hex_color,
                'preview': str(seq[:8])[:-1] + '...]' if len(seq) > 8 else str(seq)
            })
        
        # ========== First chart: Normal size ==========
        print("\nGenerating Chart 1: Normal size...")
        fig1, (ax_grid1, ax_legend1) = plt.subplots(
            1, 2, 
            figsize=(14, 7),
            gridspec_kw={'width_ratios': [3, 1]}
        )
        
        # Draw grid
        ax_grid1.imshow(grid_data, interpolation='nearest')
        ax_grid1.set_title(f'Fibonacci Sequence Mod {self.base} Period Visualization', fontsize=14, fontweight='bold')
        ax_grid1.set_xlabel('X Coordinate')
        ax_grid1.set_ylabel('Y Coordinate')
        ax_grid1.grid(True, alpha=0.3)
        
        # Add coordinate labels
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
        
        # Draw legend
        ax_legend1.axis('off')
        ax_legend1.set_title('Sequence Information', fontsize=12, fontweight='bold')
        
        legend_text1 = f"Modulo: {self.base}\n"
        legend_text1 += f"Total Sequences: {len(self.sequences)}\n"
        legend_text1 += f"Selected: {len(self.selected_sequences)}\n\n"
        
        for i, info in enumerate(sequence_info[:20]):
            legend_text1 += f"[{info['index']}] Length={info['length']}\n"
            legend_text1 += f"    {info['preview']}\n"
        
        if len(sequence_info) > 20:
            legend_text1 += f"\n... {len(sequence_info) - 20} more sequences"
        
        legend_text1 += f"\nGeneration Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        ax_legend1.text(0.05, 0.95, legend_text1, 
                       transform=ax_legend1.transAxes, 
                       fontsize=9, 
                       verticalalignment='top',
                       fontfamily='monospace',
                       bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.5))
        
        plt.tight_layout()
        
        # ========== Second chart: High resolution grid only ==========
        print("Generating Chart 2: High resolution grid only...")
        
        # Large modulo warning
        if grid_size > 200:
            print(f"  ⚠️  Warning: Modulo {grid_size} is large, generating high resolution grid may:")
            print(f"     - Consume large amount of memory (expected > 2GB)")
            print(f"     - Take a long time (may > 30 seconds)")
            print(f"     - Generate large file (may > 10MB)")
            
            confirm = input("  Continue generating? (y/n): ").strip().lower()
            if confirm != 'y':
                print("  Skipped high resolution grid generation")
                # Only show first chart
                try:
                    plt.show(block=True)
                except Exception as e:
                    print(f"Warning: Problem displaying chart: {e}")
                
                # Ask if save
                save_choice = input("\nSave charts as PNG files? (y/n): ").strip().lower()
                if save_choice == 'y':
                    try:
                        filename1 = f"fibonacci_mod_{self.base}_visualization.png"
                        fig1.savefig(filename1, dpi=150, bbox_inches='tight')
                        print(f"✓ Chart 1 saved as: {filename1}")
                    except Exception as e:
                        print(f"Error: Failed to save image: {e}")
                
                try:
                    plt.close('all')
                except:
                    pass
                
                return
        
        # Calculate appropriate chart size based on grid size
        # Each cell is exactly 10x10 pixels
        pixel_per_cell = 10
        dpi = 300  # High DPI
        fig_width = grid_size * pixel_per_cell / dpi
        fig_height = grid_size * pixel_per_cell / dpi
        
        print(f"  - Grid size: {grid_size}x{grid_size} cells")
        print(f"  - Pixel size per cell: {pixel_per_cell}x{pixel_per_cell}")
        print(f"  - Chart size: {fig_width:.1f}x{fig_height:.1f} inches")
        print(f"  - Total resolution: {int(fig_width * dpi)}x{int(fig_height * dpi)} pixels")
        
        # Create a figure with exactly the grid dimensions
        fig2 = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
        ax2 = fig2.add_subplot(111)
        
        # Draw high resolution grid only
        ax2.imshow(grid_data, interpolation='nearest')
        
        # Remove axes, ticks, and labels for a clean grid view
        ax2.set_xticks([])
        ax2.set_yticks([])
        ax2.axis('off')
        
        plt.tight_layout(pad=0)
        
        # ========== Display and save ==========
        print("\n✓ Charts generation completed!")
        print("  - Close chart windows to return to menu")
        
        try:
            plt.show(block=True)
        except Exception as e:
            print(f"Warning: Problem displaying chart: {e}")
            print("  But chart files can still be saved.")
        
        # Ask if save
        save_choice = input("\nSave charts as PNG files? (y/n): ").strip().lower()
        if save_choice == 'y':
            try:
                # Save normal size chart
                filename1 = f"fibonacci_mod_{self.base}_visualization.png"
                fig1.savefig(filename1, dpi=150, bbox_inches='tight')
                print(f"✓ Chart 1 saved as: {filename1}")
                
                # Save high resolution grid-only chart with 10x10 pixel cells
                filename2 = f"fibonacci_mod_{self.base}_highres_grid.png"
                fig2.savefig(filename2, dpi=dpi, bbox_inches='tight', pad_inches=0)
                print(f"✓ Chart 2 (high resolution grid) saved as: {filename2}")
                print(f"  - Grid size: {grid_size}x{grid_size} cells")
                print(f"  - Pixel size per cell: {pixel_per_cell}x{pixel_per_cell}")
                print(f"  - Total pixels: {int(fig_width * dpi)}x{int(fig_height * dpi)}")
            except Exception as e:
                print(f"Error: Failed to save image: {e}")
        
        # Clean memory
        try:
            plt.close('all')
            print("  - Memory cleaned")
        except:
            pass
    
    def main_menu(self):
        """Main menu"""
        while True:
            self.print_banner()
            
            if self.base is None:
                print("Current status: Not calculated")
            else:
                print(f"Current status: Modulo={self.base}, Number of sequences={len(self.sequences)}")
                print(f"Selected: {len(self.selected_sequences)} sequences")
            
            print("\n" + "=" * 70)
            print("Main Menu:")
            print("=" * 70)
            print("1. Calculate new modulo")
            print("2. Select sequences to visualize")
            print("3. Generate visualization charts")
            print("4. View sequence details")
            print("5. Export data as JSON")
            print("0. Exit")
            print("=" * 70)
            
            choice = input("\nPlease select (0-5): ").strip()
            
            if choice == '0':
                print("\nThank you for using! Goodbye!")
                break
            elif choice == '1':
                try:
                    base = int(input("Please enter modulo (1-1000000): ").strip())
                    if base < 1 or base > 1000000:
                        print("Error: Modulo must be between 1-1000000")
                        input("\nPress Enter to continue...")
                        continue
                    
                    if not self.check_executable():
                        input("\nPress Enter to continue...")
                        continue
                    
                    if self.run_cpp_program(base):
                        self.selected_sequences.clear()
                        print("\n✓ Calculation successful!")
                    else:
                        print("\n✗ Calculation failed!")
                    
                    input("\nPress Enter to continue...")
                except ValueError:
                    print("Error: Please enter a valid integer")
                    input("\nPress Enter to continue...")
            elif choice == '2':
                if self.base is None:
                    print("Error: Please calculate a modulo first")
                    input("\nPress Enter to continue...")
                else:
                    self.select_sequences_interactive()
            elif choice == '3':
                if self.base is None:
                    print("Error: Please calculate a modulo first")
                    input("\nPress Enter to continue...")
                elif not self.selected_sequences:
                    print("Error: Please select sequences to visualize first")
                    input("\nPress Enter to continue...")
                else:
                    self.generate_visualization()
                    input("\nPress Enter to continue...")
            elif choice == '4':
                if self.base is None:
                    print("Error: Please calculate a modulo first")
                else:
                    self.display_sequences()
                    input("\nPress Enter to continue...")
            elif choice == '5':
                if self.base is None:
                    print("Error: Please calculate a modulo first")
                else:
                    filename = f"examples/fibonacci_mod_{self.base}_data.json"
                    with open(filename, 'w') as f:
                        json.dump({
                            'base': self.base,
                            'sequences': self.sequences,
                            'cycles_pairs': self.cycles_pairs,
                            'selected_sequences': sorted(list(self.selected_sequences))
                        }, f, indent=2)
                    print(f"✓ Data exported to: {filename}")
                    input("\nPress Enter to continue...")
            else:
                print("Error: Invalid selection")
                input("\nPress Enter to continue...")


def main():
    """Main function"""
    # Check Python version
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required")
        sys.exit(1)
    
    # Check matplotlib
    try:
        import matplotlib
    except ImportError:
        print("Error: matplotlib library is required")
        print("Please install: pip3 install matplotlib")
        sys.exit(1)
    
    # Create visualizer and run
    visualizer = FibonacciVisualizer()
    visualizer.main_menu()


if __name__ == "__main__":
    main()
