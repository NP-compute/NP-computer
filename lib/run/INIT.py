# This is used to initialize the NP computer, and will be used to add nodes and edges to the graph
import networkx as nx
from lib.run.IS_COLORABLE import is_colorable
from lib.run.FINALS import TriBit, ALL_TRI_BITS, TRI_BIT_TO_NODE

class NPComputer:
    def __init__(self):
        self.graph = nx.Graph()

        # Add in 3 nodes that are fully connected to each other to get 0, 1, and X
        tribit_zero, tribit_one, tribit_x = TRI_BIT_TO_NODE[TriBit.ZERO], TRI_BIT_TO_NODE[TriBit.ONE], TRI_BIT_TO_NODE[TriBit.X]
        self.graph.add_edges_from([(tribit_zero, tribit_one), (tribit_one, tribit_x), (tribit_x, tribit_zero)])

    def generate_node(self, allow={TriBit.ZERO, TriBit.ONE, TriBit.X}) -> int:
        """ Add a node to the graph, with optional constraints on what values it can take

        Args:
            allow (dict, optional): Defines what TriBits this node can take, defaults to allow all values. Defaults to {TriBit.ZERO, TriBit.ONE, TriBit.X}.
        """

        node_id = len(self.graph.nodes) + 1
        self.graph.add_node(node_id)

        # Connect this node to all TriBits that it is NOT allowed to be so the coloring algorithm can't assign it that value
        for tri_bit in ALL_TRI_BITS - allow:
            self.graph.add_edge(node_id, TRI_BIT_TO_NODE[tri_bit])

        return node_id

    def add_edge(self, u, v):
        self.graph.add_edge(u, v)

    def __call__(self):
        
        # Run the graph coloring algorithm to see if the graph if it is 3 colorable
        # Essentially this computer returns true or false based off of if the graph is 3 colorable
        return self.get_result_mapping()[0]
    
    def get_mapping(self):
        """ Get the mapping of nodes to colors of the graph regardless of if it is 3 colorable

        Returns:
            dict: Mapping of nodes to colors
        """
        return self.get_result_mapping()[1]
    
    def get_result_mapping(self):
        """ Gets the result and mapping of the graph

        Returns:
            (bool, dict): (result, mapping)
        """
        
        return is_colorable(self.graph)

# Test code
def test_np_computer():
    """Comprehensive test suite for NPComputer"""
    
    print("=== NPComputer Test Suite ===\n")
    
    # Test 1: Basic initialization
    print("Test 1: Basic Initialization")
    np_comp = NPComputer()
    print(f"Initial nodes: {list(np_comp.graph.nodes())}")
    print(f"Initial edges: {list(np_comp.graph.edges())}")
    print(f"Initial graph is 3-colorable: {np_comp()}")
    assert np_comp() == True, "Initial graph should be 3-colorable"
    print("✓ PASSED\n")
    
    # Test 2: Generate node with all constraints allowed
    print("Test 2: Generate Node (All Values Allowed)")
    np_comp = NPComputer()
    node1 = np_comp.generate_node()
    print(f"Generated node: {node1}")
    print(f"Graph nodes after generation: {list(np_comp.graph.nodes())}")
    print(f"Graph edges after generation: {list(np_comp.graph.edges())}")
    print(f"Graph is still 3-colorable: {np_comp()}")
    assert np_comp() == True, "Graph should still be 3-colorable"
    print("✓ PASSED\n")
    
    # Test 3: Generate node with specific constraints
    print("Test 3: Generate Node (Only ZERO and ONE allowed)")
    np_comp = NPComputer()
    node1 = np_comp.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    print(f"Generated node: {node1}")
    print(f"Node {node1} is connected to: {list(np_comp.graph.neighbors(node1))}")
    print(f"Graph is still 3-colorable: {np_comp()}")
    assert np_comp() == True, "Graph should still be 3-colorable"
    print("✓ PASSED\n")
    
    # Test 4: Generate node with single constraint
    print("Test 4: Generate Node (Only ZERO allowed)")
    np_comp = NPComputer()
    node1 = np_comp.generate_node(allow={TriBit.ZERO})
    print(f"Generated node: {node1}")
    print(f"Node {node1} is connected to: {list(np_comp.graph.neighbors(node1))}")
    print(f"Graph is still 3-colorable: {np_comp()}")
    assert np_comp() == True, "Graph should still be 3-colorable"
    print("✓ PASSED\n")
    
    # Test 5: Multiple nodes with different constraints
    print("Test 5: Multiple Nodes with Different Constraints")
    np_comp = NPComputer()
    node1 = np_comp.generate_node(allow={TriBit.ZERO})
    node2 = np_comp.generate_node(allow={TriBit.ONE})
    node3 = np_comp.generate_node(allow={TriBit.X})
    print(f"Generated nodes: {node1}, {node2}, {node3}")
    print(f"Total nodes: {len(np_comp.graph.nodes())}")
    print(f"Graph is still 3-colorable: {np_comp()}")
    assert np_comp() == True, "Graph should still be 3-colorable"
    print("✓ PASSED\n")
    
    # Test 6: Add edge between generated nodes
    print("Test 6: Add Edge Between Generated Nodes")
    np_comp = NPComputer()
    node1 = np_comp.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    node2 = np_comp.generate_node(allow={TriBit.ONE, TriBit.X})
    np_comp.add_edge(node1, node2)
    print(f"Added edge between {node1} and {node2}")
    print(f"Graph is still 3-colorable: {np_comp()}")
    assert np_comp() == True, "Graph should still be 3-colorable"
    print("✓ PASSED\n")
    
    # Test 7: Create a scenario that should make the graph non-3-colorable
    print("Test 7: Create Non-3-Colorable Scenario")
    np_comp = NPComputer()
    # Create nodes that can only be specific values and connect them in a way that conflicts
    node1 = np_comp.generate_node(allow={TriBit.ZERO})  # Must be ZERO
    node2 = np_comp.generate_node(allow={TriBit.ZERO})  # Must be ZERO
    node3 = np_comp.generate_node(allow={TriBit.ZERO})  # Must be ZERO
    node4 = np_comp.generate_node(allow={TriBit.ONE})   # Must be ONE
    
    # Connect all the ZERO nodes to each other - this should still work
    np_comp.add_edge(node1, node2)
    np_comp.add_edge(node2, node3)
    np_comp.add_edge(node1, node3)
    
    # Connect one of the ZERO nodes to the ONE node - this should still work
    np_comp.add_edge(node1, node4)
    
    print(f"Created constrained scenario with nodes: {node1}, {node2}, {node3}, {node4}")
    result = np_comp()
    print(f"Graph is 3-colorable: {result}")
    assert result == False, "Graph should not be 3 colorable"
    # This might still be 3-colorable depending on the constraints
    print("✓ PASSED\n")
    
    # Test 8: Test node ID generation
    print("Test 8: Node ID Generation")
    np_comp = NPComputer()
    nodes = []
    for i in range(5):
        node = np_comp.generate_node()
        nodes.append(node)
    print(f"Generated node IDs: {nodes}")
    assert nodes == [4, 5, 6, 7, 8], f"Expected [4, 5, 6, 7, 8], got {nodes}"
    print("✓ PASSED\n")
    
    # Test 9: Complex constraint scenario
    print("Test 9: Complex Constraint Scenario")
    np_comp = NPComputer()
    
    # Create a scenario where we have nodes with overlapping but different constraints
    node_a = np_comp.generate_node(allow={TriBit.ZERO, TriBit.ONE})      # Can be 0 or 1
    node_b = np_comp.generate_node(allow={TriBit.ONE, TriBit.X})         # Can be 1 or X
    node_c = np_comp.generate_node(allow={TriBit.ZERO, TriBit.X})        # Can be 0 or X
    
    # Connect them in a triangle
    np_comp.add_edge(node_a, node_b)
    np_comp.add_edge(node_b, node_c)
    np_comp.add_edge(node_c, node_a)
    
    print(f"Created triangle with constrained nodes: {node_a}, {node_b}, {node_c}")
    print(f"Graph is 3-colorable: {np_comp()}")
    
    # Get the actual coloring to see what happened
    colorable, coloring = is_colorable(np_comp.graph)
    if colorable:
        print(f"Coloring: {coloring}")
        print(f"Node {node_a} colored as: {coloring.get(node_a, 'Unknown')}")
        print(f"Node {node_b} colored as: {coloring.get(node_b, 'Unknown')}")
        print(f"Node {node_c} colored as: {coloring.get(node_c, 'Unknown')}")
    
    print("✓ PASSED\n")
    
    # Test 10: Visualize final graph structure
    print("Test 10: Graph Structure Analysis")
    np_comp = NPComputer()
    node1 = np_comp.generate_node(allow={TriBit.ZERO})
    node2 = np_comp.generate_node(allow={TriBit.ONE, TriBit.X})
    np_comp.add_edge(node1, node2)
    
    print(f"Final graph has {len(np_comp.graph.nodes())} nodes and {len(np_comp.graph.edges())} edges")
    print(f"Nodes: {list(np_comp.graph.nodes())}")
    print(f"Edges: {list(np_comp.graph.edges())}")
    
    # Show degree of each node
    for node in np_comp.graph.nodes():
        degree = np_comp.graph.degree(node)
        neighbors = list(np_comp.graph.neighbors(node))
        print(f"Node {node}: degree={degree}, neighbors={neighbors}")
    
    print("✓ PASSED\n")
    
def test_all():
    test_np_computer()

if __name__ == "__main__":
    test_all()
    print("All tests completed.")