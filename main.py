#!/usr/bin/env python3
"""
Main script to generate graph training data for addition operations.
Generates DIMACS format graphs for 1-bit, 2-bit, 3-bit, and 4-bit additions.
"""

import os
from lib.run.INIT import NPComputer
from lib.run.CONST import CONST
from lib.calculator_logic.ADD import ADD

def ensure_output_dir(directory="training_graphs"):
    """Create output directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory

def generate_1bit_additions(output_dir):
    """Generate all possible 1-bit addition graphs."""
    print("=== Generating 1-bit Addition Graphs ===")

    combinations = [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1)
    ]

    for a_val, b_val in combinations:
        filename = f"{output_dir}/add_1bit_{a_val}_{b_val}.col"
        graph_name = f"add_1bit_{a_val}_{b_val}"

        computer = NPComputer(solve=False, export_file=filename, graph_name=graph_name)

        a = CONST(computer, value=a_val, n=1)
        b = CONST(computer, value=b_val, n=1)

        result, carry = ADD(computer, a, b)

        # Export the graph
        computer()

        print(f"  Generated: {filename} ({len(computer.graph.nodes())} nodes, {len(computer.graph.edges())} edges)")

    print()

def generate_2bit_additions(output_dir, num_samples=16):
    """Generate 2-bit addition graphs."""
    print("=== Generating 2-bit Addition Graphs ===")

    # Generate all combinations (0-3 + 0-3)
    for a_val in range(4):
        for b_val in range(4):
            filename = f"{output_dir}/add_2bit_{a_val}_{b_val}.col"
            graph_name = f"add_2bit_{a_val}_{b_val}"

            computer = NPComputer(solve=False, export_file=filename, graph_name=graph_name)

            a = CONST(computer, value=a_val, n=2)
            b = CONST(computer, value=b_val, n=2)

            result, carry = ADD(computer, a, b)

            # Export the graph
            computer()

            print(f"  Generated: {filename} ({len(computer.graph.nodes())} nodes, {len(computer.graph.edges())} edges)")

    print()

def generate_3bit_additions(output_dir):
    """Generate 3-bit addition graphs."""
    print("=== Generating 3-bit Addition Graphs ===")

    # Generate all combinations (0-7 + 0-7)
    for a_val in range(8):
        for b_val in range(8):
            filename = f"{output_dir}/add_3bit_{a_val}_{b_val}.col"
            graph_name = f"add_3bit_{a_val}_{b_val}"

            computer = NPComputer(solve=False, export_file=filename, graph_name=graph_name)

            a = CONST(computer, value=a_val, n=3)
            b = CONST(computer, value=b_val, n=3)

            result, carry = ADD(computer, a, b)

            # Export the graph
            computer()

            print(f"  Generated: {filename} ({len(computer.graph.nodes())} nodes, {len(computer.graph.edges())} edges)")

    print()

def generate_4bit_additions(output_dir):
    """Generate 4-bit addition graphs."""
    print("=== Generating 4-bit Addition Graphs ===")

    # Generate all combinations (0-15 + 0-15)
    for a_val in range(16):
        for b_val in range(16):
            filename = f"{output_dir}/add_4bit_{a_val}_{b_val}.col"
            graph_name = f"add_4bit_{a_val}_{b_val}"

            computer = NPComputer(solve=False, export_file=filename, graph_name=graph_name)

            a = CONST(computer, value=a_val, n=4)
            b = CONST(computer, value=b_val, n=4)

            result, carry = ADD(computer, a, b)

            # Export the graph
            computer()

            print(f"  Generated: {filename} ({len(computer.graph.nodes())} nodes, {len(computer.graph.edges())} edges)")

    print()

def main():
    """Main function to generate all training graphs."""
    print("=" * 60)
    print("Graph Training Data Generator for Addition Operations")
    print("=" * 60)
    print()

    # Create output directory
    output_dir = ensure_output_dir("training_graphs")
    print(f"Output directory: {output_dir}\n")

    # Generate graphs for each bit size
    generate_1bit_additions(output_dir)
    generate_2bit_additions(output_dir)
    generate_3bit_additions(output_dir)
    generate_4bit_additions(output_dir)

    print("=" * 60)
    print("All training graphs generated successfully!")
    print("=" * 60)

    # Print summary
    num_files = len([f for f in os.listdir(output_dir) if f.endswith('.col')])
    print(f"\nTotal graphs generated: {num_files}")
    print(f"  - 1-bit additions: 4 graphs")
    print(f"  - 2-bit additions: 16 graphs")
    print(f"  - 3-bit additions: 64 graphs")
    print(f"  - 4-bit additions: 256 graphs")
    print(f"\nAll files saved to: {output_dir}/")

if __name__ == "__main__":
    main()
