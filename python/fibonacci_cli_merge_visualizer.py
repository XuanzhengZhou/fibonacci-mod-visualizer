#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fibonacci Sequence Modulo Period - Command Line Interactive 2D/3D Visualization Tool

Usage:
    python3 fibonacci_cli_merge_visualizer.py
    
Features:
    - Interactive input of modulo
    - Select sequence ranges to visualize
    - Generate both 2D and 3D visualizations 
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

class FibonacciMergeVisualizer:
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
        print("  Fibonacci Sequence Modulo Period - 2D/3D Visualization Tool")
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
        """Generate both 2D and 3D visualizations"""
        if not self.selected_sequences:
            print("Error: No sequences selected")
            return
        
        if self.base is None or not self.sequences:
            print("Error: No available data, please calculate modulo first")
            return
        
        print("\nGenerating 2D and 3D visualizations...")
        print(f"  - Modulo: {self.base}")
        print(f"  - Number of selected sequences: {len(self.selected_sequences)}")
        
        # Import 3D plotting tools
        from mpl_toolkits.mplot3d import Axes3D
        from mpl_toolkits.mplot3d.art3d import Poly3DCollection
        import matplotlib.pyplot as plt
        
        # Information for storing each sequence
        sequence_info = []
        
        # Find the maximum sequence length to normalize color intensity
        max_length = max(len(self.sequences[idx]) for idx in self.selected_sequences if idx < len(self.sequences))
        min_length = min(len(self.sequences[idx]) for idx in self.selected_sequences if idx < len(self.sequences))
        
        # Create 2D grid data
        grid_size = self.base
        grid_data = np.zeros((grid_size, grid_size, 3))
        
        # Prepare data for 3D visualization
        x_data = []
        y_data = []
        z_data = []  # z position (bottom of the cube)
        height_data = []  # height of each sequence (for positioning the top cube)
        colors = []
        
        # Fill both 2D and 3D data
        for idx in self.selected_sequences:
            if idx >= len(self.sequences):
                continue
            
            seq = self.sequences[idx]
            # Calculate color intensity based on sequence length (shorter = more vivid)
            seq_length = len(seq)
            # Use sequence length as the height reference for top cube position
            height = seq_length
            
            # Normalize the length to a 0-1 range where shorter sequences have higher intensity
            if max_length == min_length:
                intensity = 1.0  # If all selected sequences have the same length, use max intensity
            else:
                # Invert the ratio so shorter sequences get higher intensity values
                intensity = 1.0 - ((seq_length - min_length) / (max_length - min_length))
            
            # Get base color from palette
            base_color = PALETTE[idx % len(PALETTE)]
            base_rgb = tuple(int(base_color[i:i+2], 16) / 255 for i in (1, 3, 5))
            
            # Adjust the color based on intensity to make shorter sequences more vivid
            # For vividness, we'll increase saturation for shorter sequences and decrease for longer ones
            # Convert RGB to HSV to manipulate saturation
            h, s, v = colorsys.rgb_to_hsv(*base_rgb)
            # Adjust saturation and value (brightness) based on intensity
            # Higher intensity (shorter sequences) = higher saturation and brightness
            adjusted_s = s * (0.8 + 0.2 * intensity)  # Very subtle change in saturation
            adjusted_v = v * (0.85 + 0.15 * intensity)  # Very subtle change in brightness
            # Convert back to RGB
            r, g, b = colorsys.hsv_to_rgb(h, adjusted_s, adjusted_v)
            rgb_color = (r, g, b)
            rgba_color = (r, g, b, 0.8)  # Add alpha for transparency in 3D
            
            # Generate coordinate pairs
            pairs = []
            for i in range(len(seq)):
                a = seq[i]
                b = seq[(i + 1) % len(seq)]
                pairs.append((a, b))
            
            # Fill 2D grid data
            for x, y in pairs:
                if 0 <= x < grid_size and 0 <= y < grid_size:
                    grid_data[y, x] = rgb_color
            
            # Add each coordinate pair as a top cube in 3D space
            for x, y in pairs:
                x_data.append(x)
                y_data.append(y)
                z_data.append(height - 0.5)  # Position cube at the top of the sequence height
                height_data.append(height)  # Store the height for visualization
                colors.append(rgba_color)
            
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
                'preview': str(seq[:8])[:-1] + '...' if len(seq) > 8 else str(seq)
            })
        
        # Create 2D visualization
        print("Generating 2D chart...")
        fig2d, (ax_grid2d, ax_legend2d) = plt.subplots(
            1, 2,
            figsize=(14, 7),
            gridspec_kw={'width_ratios': [3, 1]}
        )
        
        # Draw 2D grid
        ax_grid2d.imshow(grid_data, interpolation='nearest')
        ax_grid2d.set_title(f'2D Fibonacci Sequence Mod {self.base} Period Visualization', fontsize=14, fontweight='bold')
        ax_grid2d.set_xlabel('X Coordinate')
        ax_grid2d.set_ylabel('Y Coordinate')
        ax_grid2d.grid(True, alpha=0.3)
        
        # Add coordinate labels
        if grid_size <= 20:
            ax_grid2d.set_xticks(range(grid_size))
            ax_grid2d.set_yticks(range(grid_size))
            ax_grid2d.set_xticklabels(range(grid_size))
            ax_grid2d.set_yticklabels(range(grid_size))
        else:
            step = max(1, grid_size // 10)
            ax_grid2d.set_xticks(range(0, grid_size, step))
            ax_grid2d.set_yticks(range(0, grid_size, step))
            ax_grid2d.set_xticklabels(range(0, grid_size, step))
            ax_grid2d.set_yticklabels(range(0, grid_size, step))
        
        # Draw legend for 2D
        ax_legend2d.axis('off')
        ax_legend2d.set_title('Sequence Information', fontsize=12, fontweight='bold')
        
        legend_text2d = f"Modulo: {self.base}\n"
        legend_text2d += f"Total Sequences: {len(self.sequences)}\n"
        legend_text2d += f"Selected: {len(self.selected_sequences)}\n\n"
        
        for i, info in enumerate(sequence_info[:20]):
            legend_text2d += f"[{info['index']}] Length={info['length']}\n"
            legend_text2d += f"    {info['preview']}\n"
        
        if len(sequence_info) > 20:
            legend_text2d += f"\n... {len(sequence_info) - 20} more sequences"
        
        legend_text2d += f"\nGeneration Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        ax_legend2d.text(0.05, 0.95, legend_text2d,
                        transform=ax_legend2d.transAxes,
                        fontsize=9,
                        verticalalignment='top',
                        fontfamily='monospace',
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.5))
        
        plt.tight_layout()
        
        # Create high-resolution 2D grid-only visualization
        print("Generating high-resolution 2D grid-only chart...")
        
        # Large modulo warning
        if grid_size > 200:
            print(f"  ⚠️  Warning: Modulo {grid_size} is large, generating high resolution grid may:")
            print(f"     - Consume large amount of memory (expected > 2GB)")
            print(f"     - Take a long time (may > 30 seconds)")
            print(f"     - Generate large file (may > 10MB)")
            
            confirm = input("  Continue generating? (y/n): ").strip().lower()
            if confirm != 'y':
                print("  Skipped high resolution grid generation")
                # Continue with 3D visualization
            else:
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
                fig2d_highres = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
                ax2d_highres = fig2d_highres.add_subplot(111)
                
                # Draw high resolution grid only
                ax2d_highres.imshow(grid_data, interpolation='nearest')
                
                # Remove axes, ticks, and labels for a clean grid view
                ax2d_highres.set_xticks([])
                ax2d_highres.set_yticks([])
                ax2d_highres.axis('off')
                
                plt.tight_layout(pad=0)
        else:
            # For smaller grids, still create the high-res version
            pixel_per_cell = 10
            dpi = 300  # High DPI
            fig_width = grid_size * pixel_per_cell / dpi
            fig_height = grid_size * pixel_per_cell / dpi
            
            # Create a figure with exactly the grid dimensions
            fig2d_highres = plt.figure(figsize=(fig_width, fig_height), dpi=dpi)
            ax2d_highres = fig2d_highres.add_subplot(111)
            
            # Draw high resolution grid only
            ax2d_highres.imshow(grid_data, interpolation='nearest')
            
            # Remove axes, ticks, and labels for a clean grid view
            ax2d_highres.set_xticks([])
            ax2d_highres.set_yticks([])
            ax2d_highres.axis('off')
            
            plt.tight_layout(pad=0)
        
        # Create 3D visualization
        print("Generating 3D chart...")
        fig3d = plt.figure(figsize=(14, 10))
        ax3d = fig3d.add_subplot(111, projection='3d')
        
        # Create top cubes only
        if x_data and y_data and z_data:
            dx = dy = 0.8  # Width and depth of each cube
            dz = 1.0  # Fixed height of each top cube
            
            # Draw top cubes only
            for i in range(len(x_data)):
                x = x_data[i]
                y = y_data[i]
                z = z_data[i]  # Position the cube at the height corresponding to sequence length
                
                # Create a cube at (x, y, z) with dimensions (dx, dy, dz)
                xx = [x, x+dx, x+dx, x, x, x+dx, x+dx, x]
                yy = [y, y, y+dy, y+dy, y, y, y+dy, y+dy]
                zz = [z, z, z, z, z+dz, z+dz, z+dz, z+dz]
                
                # Define the 6 faces of the cube
                faces = [
                    [xx[0], yy[0], zz[0]], [xx[1], yy[1], zz[1]], [xx[2], yy[2], zz[2]], [xx[3], yy[3], zz[3]],  # Bottom
                    [xx[4], yy[4], zz[4]], [xx[5], yy[5], zz[5]], [xx[6], yy[6], zz[6]], [xx[7], yy[7], zz[7]],  # Top
                    [xx[0], yy[0], zz[0]], [xx[1], yy[1], zz[1]], [xx[5], yy[5], zz[5]], [xx[4], yy[4], zz[4]],  # Front
                    [xx[2], yy[2], zz[2]], [xx[3], yy[3], zz[3]], [xx[7], yy[7], zz[7]], [xx[6], yy[6], zz[6]],  # Back
                    [xx[1], yy[1], zz[1]], [xx[2], yy[2], zz[2]], [xx[6], yy[6], zz[6]], [xx[5], yy[5], zz[5]],  # Right
                    [xx[4], yy[4], zz[4]], [xx[7], yy[7], zz[7]], [xx[3], yy[3], zz[3]], [xx[0], yy[0], zz[0]]   # Left
                ]
                
                # Create a Poly3DCollection for each face
                face_vertices = [
                    [faces[0], faces[1], faces[2], faces[3]],  # Bottom
                    [faces[4], faces[5], faces[6], faces[7]],  # Top
                    [faces[8], faces[9], faces[10], faces[11]],  # Front
                    [faces[12], faces[13], faces[14], faces[15]], # Back
                    [faces[16], faces[17], faces[18], faces[19]], # Right
                    [faces[20], faces[21], faces[22], faces[23]]  # Left
                ]
                
                # Create Poly3DCollection for the cube faces
                cube_faces = Poly3DCollection(face_vertices, facecolors=colors[i], edgecolors='black', linewidths=0.2)
                ax3d.add_collection3d(cube_faces)
        
        # Set labels and title for 3D
        ax3d.set_xlabel('X Coordinate')
        ax3d.set_ylabel('Y Coordinate')
        ax3d.set_zlabel('Sequence Period Height')
        ax3d.set_title(f'3D Fibonacci Sequence Mod {self.base} Period Visualization\nTop cubes represent sequence period length', fontsize=14, fontweight='bold')
        
        # Set axis limits for 3D
        ax3d.set_xlim(0, grid_size)
        ax3d.set_ylim(0, grid_size)
        max_height = max(height_data) if height_data else 1
        ax3d.set_zlim(0, max_height * 1.2)  # Add some space above for better visualization
        
        # Add legend for 3D sequence information
        legend_text3d = f"Modulo: {self.base}\n"
        legend_text3d += f"Total Sequences: {len(self.sequences)}\n"
        legend_text3d += f"Selected: {len(self.selected_sequences)}\n\n"
        
        for i, info in enumerate(sequence_info[:20]):
            legend_text3d += f"[{info['index']}] Length={info['length']}\n"
            legend_text3d += f"    {info['preview']}\n"
        
        if len(sequence_info) > 20:
            legend_text3d += f"\n... {len(sequence_info) - 20} more sequences"
        
        legend_text3d += f"\nGeneration Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Add text box for legend
        ax3d.text2D(0.02, 0.98, legend_text3d,
                  transform=ax3d.transAxes,
                  fontsize=9,
                  verticalalignment='top',
                  fontfamily='monospace',
                  bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        # Adjust the viewing angle for better visualization
        ax3d.view_init(elev=20, azim=45)
        
        plt.tight_layout()
        
        # ========== Display and save ==========
        print("\n✓ 2D and 3D visualizations generation completed!")
        print("  - Close chart windows to return to menu")
        
        try:
            plt.show(block=True)
        except Exception as e:
            print(f"Warning: Problem displaying chart: {e}")
            print("  But chart files can still be saved.")
        
        # Ask if save
        save_choice = input("\nSave both 2D and 3D charts as PNG files? (y/n): ").strip().lower()
        if save_choice == 'y':
            try:
                # Save 2D visualization (normal size)
                filename2d = f"fibonacci_mod_{self.base}_2d_visualization.png"
                fig2d.savefig(filename2d, dpi=150, bbox_inches='tight')
                print(f"✓ 2D chart saved as: {filename2d}")
                
                # Save high-resolution 2D grid-only visualization
                filename2d_highres = f"fibonacci_mod_{self.base}_2d_highres_grid.png"
                fig2d_highres.savefig(filename2d_highres, dpi=300, bbox_inches='tight', pad_inches=0)
                print(f"✓ High-resolution 2D grid-only chart saved as: {filename2d_highres}")
                print(f"  - Grid size: {grid_size}x{grid_size} cells")
                print(f"  - Pixel size per cell: 10x10")
                print(f"  - Total pixels: {int(fig_width * 300)}x{int(fig_height * 300)}")
                
                # Define different viewing angles for 3D
                angles = [
                    {'elev': 20, 'azim': 45, 'name': 'main'},
                    {'elev': 20, 'azim': 135, 'name': 'side_1'},
                    {'elev': 20, 'azim': 225, 'name': 'side_2'},
                    {'elev': 20, 'azim': 315, 'name': 'side_3'},
                    {'elev': 90, 'azim': 0, 'name': 'top'},
                    {'elev': 0, 'azim': 0, 'name': 'front'},
                    {'elev': 0, 'azim': 90, 'name': 'side'},
                ]
                
                # Save 3D visualizations from different angles
                for angle in angles:
                    ax3d.view_init(elev=angle['elev'], azim=angle['azim'])
                    filename3d = f"fibonacci_mod_{self.base}_3d_visualization_{angle['name']}.png"
                    fig3d.savefig(filename3d, dpi=150, bbox_inches='tight')
                    print(f"✓ 3D chart ({angle['name']} view) saved as: {filename3d}")
                
                # Reset to original view
                ax3d.view_init(elev=20, azim=45)
                
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
            print("3. Generate 2D/3D visualization charts")
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
    visualizer = FibonacciMergeVisualizer()
    visualizer.main_menu()


if __name__ == "__main__":
    main()
