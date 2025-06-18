# This has the IF operation for the NP computer
# Since this NP computer is very similar to hardware we cant choose to just use branching
# We have to create a gate at the input and output.
# The blocking at the input is to prevent BREAK logic from being used within the code
# The blocking at the output is to act as if the graph had never been colored (or rather executed)
# To allow more manual control this function should be used before the input and after the output

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS, TRI_BIT_TO_NODE
from lib.binary_logic.NOT import NOT
from lib.binary_logic.SWAP import SWAP
from lib.binary_logic.NAND import NAND
from lib.binary_logic.NOR import NOR
from lib.binary_logic.OR import OR
from lib.binary_logic.AND import AND
from lib.binary_logic.XOR import XOR
from lib.run.CONST import CONST
from lib.run.VAR import VAR
from lib.run.MEM import MEM

def generate_IF_layer(computer: NPComputer, nodes: list[int], toggle_node: int) -> list[int]:
    """ Generate the IF layer for the NP computer

    Args:
        computer (NPComputer): The NP computer to generate the IF layer for
        nodes (list[int]): The nodes to connect to the IF layer
        toggle_node (int): The node that will toggle the IF layer to allow output (1 allows output, 0 blocks output)

    Returns:
        list[int]: The corresponding nodes for the output layer
    """

    # There are two branches that control this logic
    # The end goal is
    # 1. To have the open as cant be 2 so that it must be 0 or 1, be the negation of the input, to then negate the output
    # 2. To have the closed as cant be 0 or 1 so that it must be 2, that way the input doesnt effect the output and vice versa

    # These branches control the main logic
    branch1 = NOT(computer, SWAP(computer, NOT(computer, toggle_node), from_poss=[TriBit.ZERO, TriBit.ONE], to_poss=[TriBit.ONE, TriBit.X]), between={TriBit.ONE, TriBit.X})
    branch2 = NOT(computer, SWAP(computer, toggle_node, from_poss=[TriBit.ONE, TriBit.ZERO], to_poss=[TriBit.ZERO, TriBit.X]), between={TriBit.ZERO, TriBit.X})
    # branch1 = NOT(computer, SWAP(computer, toggle_node), between={TriBit.ONE, TriBit.X})
    # branch2 = NOT(computer, SWAP(computer, NOT(computer, toggle_node), from_poss=[TriBit.ONE, TriBit.ZERO], to_poss=[TriBit.ZERO, TriBit.X]), between={TriBit.ZERO, TriBit.X})

    # Apply them to the layered output
    output_nodes = []
    for node in nodes:
        output_node = computer.generate_node()
        computer.add_edge(output_node, branch1)
        computer.add_edge(output_node, branch2)
        output_nodes.append(output_node)
    
    return output_nodes

def IF_toggle0():
    computer = NPComputer()

    zero, one = computer.generate_node(allow={TriBit.ZERO}), computer.generate_node(allow={TriBit.ONE})
    input_nodes = [zero, one]

    # Test with constant 0 toggle
    toggle_0 = CONST(computer, value=0, n=1).bits[0]
    output_nodes_0 = generate_IF_layer(computer, input_nodes, toggle_0)
    
    assert len(output_nodes_0) == 2, "Should work with constant 0 toggle"

    # Check graph validity
    is_valid, mapping = computer.get_result_mapping()
    print(f'the mapping is {mapping} and the valid is {is_valid}')
    assert is_valid, "Graph should remain valid with different toggle types"

def IF_toggle1():
    computer = NPComputer()

    zero, one = computer.generate_node(allow={TriBit.ZERO}), computer.generate_node(allow={TriBit.ONE})
    input_nodes = [zero, one]

    # Test with constant 1 toggle
    toggle_1 = CONST(computer, value=1, n=1).bits[0]
    output_nodes_1 = generate_IF_layer(computer, input_nodes, toggle_1)
    
    assert len(output_nodes_1) == 2, "Should work with constant 1 toggle"

    # Check graph validity
    is_valid, mapping = computer.get_result_mapping()
    print(f'the mapping is {mapping} and the valid is {is_valid}')
    assert is_valid, "Graph should remain valid with different toggle types"

# Test Functions
def test_IF_layer_graph_colorability():
    """Test that IF layer maintains 3-colorability"""
    computer = NPComputer()
    
    # Create input nodes
    input_nodes = []
    for i in range(5):
        node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
        input_nodes.append(node)
    
    # Create toggle node
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, input_nodes, toggle_node)
    
    # Check graph is still 3-colorable
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain 3-colorable after adding IF layer"
    
    print("✓ IF layer maintains 3-colorability")

def test_IF_layer_empty_input():
    """Test IF layer with empty input list"""
    computer = NPComputer()
    
    # Create toggle node
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # Generate IF layer with empty input
    output_nodes = generate_IF_layer(computer, [], toggle_node)
    
    assert output_nodes == [], "Empty input should produce empty output"
    
    # Graph should still be valid
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with empty IF layer"
    
    print("✓ IF layer handles empty input correctly")

def test_IF_layer_single_node():
    """Test IF layer with single input node"""
    computer = NPComputer()
    
    # Create single input node
    input_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, [input_node], toggle_node)
    
    assert len(output_nodes) == 1, "Single input should produce single output"
    assert output_nodes[0] != input_node, "Output node should be different from input"
    
    # Check graph validity
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with single-node IF layer"
    
    print("✓ IF layer handles single node correctly")

def test_IF_layer_with_constants():
    """Test IF layer with constant inputs"""
    computer = NPComputer()
    
    # Create constant nodes
    const_0 = CONST(computer, value=0, n=1)
    const_1 = CONST(computer, value=1, n=1)
    
    input_nodes = [const_0.bits[0], const_1.bits[0]]
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, input_nodes, toggle_node)
    
    assert len(output_nodes) == 2, "Should handle constant inputs"
    
    # Check graph validity
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with constant inputs"
    
    print("✓ IF layer works with constant inputs")

def test_IF_layer_with_variable_inputs():
    """Test IF layer with variable inputs"""
    computer = NPComputer()
    
    # Create variable
    var = VAR(computer, n=3)
    
    # Use variable bits as input
    input_nodes = var.bits
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, input_nodes, toggle_node)
    
    assert len(output_nodes) == 3, "Should handle variable inputs"
    
    # Check graph validity
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with variable inputs"
    
    print("✓ IF layer works with variable inputs")

def test_IF_layer_toggle_node_types():
    """Test IF layer with different toggle node types"""
    computer = NPComputer()
    
    # Test with constant toggle nodes
    input_nodes = [computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})]
    
    # Test with constant 0 toggle
    toggle_0 = CONST(computer, value=0, n=1).bits[0]
    output_nodes_0 = generate_IF_layer(computer, input_nodes, toggle_0)
    
    assert len(output_nodes_0) == 1, "Should work with constant 0 toggle"
    
    # Test with constant 1 toggle
    toggle_1 = CONST(computer, value=1, n=1).bits[0]
    output_nodes_1 = generate_IF_layer(computer, input_nodes, toggle_1)
    
    assert len(output_nodes_1) == 1, "Should work with constant 1 toggle"
    
    # Check graph validity
    is_valid, mapping = computer.get_result_mapping()
    print(f'the mapping is {mapping} and the valid is {is_valid}')
    assert is_valid, "Graph should remain valid with different toggle types"
    
    print("✓ IF layer works with different toggle node types")

def test_IF_layer_branch_creation():
    """Test that IF layer creates the expected branch nodes"""
    computer = NPComputer()
    
    initial_node_count = len(computer.graph.nodes())
    
    # Create input
    input_nodes = [computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})]
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    intermediate_count = len(computer.graph.nodes())
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, input_nodes, toggle_node)
    
    final_count = len(computer.graph.nodes())
    
    # Should create: branch1, branch2, and output nodes
    # branch1 = NOT(SWAP(NOT(toggle)))
    # branch2 = NOT(SWAP(toggle))
    # Plus output nodes
    nodes_created = final_count - intermediate_count
    
    print(f"Initial nodes: {initial_node_count}")
    print(f"After inputs: {intermediate_count}")
    print(f"After IF layer: {final_count}")
    print(f"Nodes created by IF layer: {nodes_created}")
    
    assert nodes_created >= len(input_nodes), "Should create at least as many nodes as outputs"

def test_IF_layer_multiple_calls():
    """Test multiple IF layer calls in same computer"""
    computer = NPComputer()
    
    # First IF layer
    input1 = [computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})]
    toggle1 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    output1 = generate_IF_layer(computer, input1, toggle1)
    
    # Second IF layer
    input2 = [computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})]
    toggle2 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    output2 = generate_IF_layer(computer, input2, toggle2)
    
    # All outputs should be unique
    assert set(output1).isdisjoint(set(output2)), "Different IF layers should have unique outputs"
    
    # Graph should remain valid
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with multiple IF layers"
    
    print("✓ Multiple IF layers work correctly")

def test_IF_layer_chaining():
    """Test chaining IF layers (output of one as input to another)"""
    computer = NPComputer()
    
    # Create initial input
    initial_input = [computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})]
    toggle1 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # First IF layer
    intermediate_output = generate_IF_layer(computer, initial_input, toggle1)
    
    # Second IF layer using first's output
    toggle2 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    final_output = generate_IF_layer(computer, intermediate_output, toggle2)
    
    assert len(final_output) == len(initial_input), "Chained IF layers should preserve node count"
    
    # Graph should remain valid
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with chained IF layers"
    
    print("✓ IF layer chaining works correctly")

def test_IF_layer_large_input():
    """Test IF layer with larger input sets"""
    computer = NPComputer()
    
    # Create larger input set
    input_nodes = []
    for i in range(20):
        node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
        input_nodes.append(node)
    
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, input_nodes, toggle_node)
    
    assert len(output_nodes) == 20, "Should handle large input sets"
    assert len(set(output_nodes)) == 20, "All output nodes should be unique"
    
    # Graph should remain valid (might be slow)
    is_valid, mapping = computer.get_result_mapping()
    assert is_valid, "Graph should remain valid with large IF layer"
    
    print("✓ IF layer handles large inputs correctly")

def test_IF_layer_edge_connections():
    """Test that IF layer creates expected edge connections"""
    computer = NPComputer()
    
    input_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    toggle_node = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    
    initial_edges = len(computer.graph.edges())
    
    # Generate IF layer
    output_nodes = generate_IF_layer(computer, [input_node], toggle_node)
    
    final_edges = len(computer.graph.edges())
    
    # Should have added edges for branch logic and connections
    assert final_edges > initial_edges, "Should add edges for IF layer logic"
    
    print(f"Edges added by IF layer: {final_edges - initial_edges}")

def test_all():
    """Run all IF layer tests"""
    IF_toggle0()
    IF_toggle1()
    test_IF_layer_graph_colorability()
    test_IF_layer_empty_input()
    test_IF_layer_single_node()
    test_IF_layer_with_constants()
    test_IF_layer_with_variable_inputs()
    test_IF_layer_toggle_node_types()
    test_IF_layer_branch_creation()
    test_IF_layer_multiple_calls()
    test_IF_layer_chaining()
    test_IF_layer_large_input()
    test_IF_layer_edge_connections()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")