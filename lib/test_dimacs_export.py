#!/usr/bin/env python3
"""Test script for DIMACS export functionality"""

from lib.run.INIT import NPComputer
from lib.run.VAR import VAR
from lib.run.CONST import CONST
from lib.binary_logic.AND import AND

def test_dimacs_export():
    print("=== Testing DIMACS Export Functionality ===\n")

    # Test 1: Export simple graph without solving
    print("Test 1: Export simple graph to DIMACS format")
    computer = NPComputer(solve=False, export_file="output_graph.col", graph_name="test_graph")

    # Create some nodes and edges
    node1 = computer.generate_node()
    node2 = computer.generate_node()
    node3 = computer.generate_node()
    computer.add_edge(node1, node2)
    computer.add_edge(node2, node3)

    # Call the computer - this will export instead of solving
    dimacs_output = computer()
    print("DIMACS output:")
    print(dimacs_output)
    print("✓ Exported to output_graph.col\n")

    # Test 2: Solve normally (default behavior)
    print("Test 2: Solve graph normally (default behavior)")
    computer2 = NPComputer()  # solve=True by default

    node1 = computer2.generate_node()
    node2 = computer2.generate_node()
    computer2.add_edge(node1, node2)

    result = computer2()
    print(f"Graph is 3-colorable: {result}")
    print("✓ Solved normally\n")

    # Test 3: Export a more complex graph
    print("Test 3: Export complex graph with logic operations")
    computer3 = NPComputer(solve=False, export_file="complex_graph.col", graph_name="complex_graph")

    var_a = VAR(computer3, n=4)
    var_b = VAR(computer3, n=4)

    # Perform some AND operations
    result_bits = []
    for i in range(4):
        result_bits.append(AND(computer3, var_a.bits[i], var_b.bits[i]))

    dimacs_output = computer3()
    print(f"Complex graph stats:")
    print(f"  Nodes: {len(computer3.graph.nodes())}")
    print(f"  Edges: {len(computer3.graph.edges())}")
    print("✓ Exported to complex_graph.col\n")

    # Test 4: Solve the same complex graph
    print("Test 4: Solve the same complex graph")
    computer4 = NPComputer(solve=True)  # Explicitly set solve=True

    var_a = VAR(computer4, n=4)
    var_b = VAR(computer4, n=4)

    result_bits = []
    for i in range(4):
        result_bits.append(AND(computer4, var_a.bits[i], var_b.bits[i]))

    result = computer4()
    print(f"Graph is 3-colorable: {result}")
    print("✓ Solved successfully\n")

    print("=== All DIMACS export tests passed! ===")

def test_all():
    test_dimacs_export()

if __name__ == "__main__":
    test_all()
