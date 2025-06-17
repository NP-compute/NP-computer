# This is a function to check if a given graph is colorable with k colors (will be used for 3 mostly)

import networkx as nx
import matplotlib.pyplot as plt

def is_colorable_greedy(graph, k=3, visualize=False):
    """Check if a graph is k-colorable and return the coloring if it is.

    Args:
        graph (_type_): 
        k (_type_): _description_
        visualize (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    try:
        coloring = nx.coloring.greedy_color(graph, strategy='largest_first')
        num_colors = len(set(coloring.values()))

        if visualize:
            colors = ['red', 'blue', 'green', 'yellow', 'purple']
            node_colors = [colors[coloring[node]] for node in graph.nodes()]
            nx.draw(graph, with_labels=True, node_color=node_colors, node_size=500)
            plt.show()

        return num_colors <= k, coloring
    except:
        return False, {}
    
def visualize_coloring(graph, coloring):
    """Visualize the 3-coloring of the graph."""
    try:
        import matplotlib.pyplot as plt
        
        colors = ['red', 'blue', 'green']
        node_colors = [colors[coloring[node]] for node in graph.nodes()]
        
        plt.figure(figsize=(10, 8))
        pos = nx.spring_layout(graph)
        nx.draw(graph, pos, with_labels=True, node_color=node_colors, 
                node_size=500, font_size=16, font_weight='bold')
        
        # Add legend
        legend_elements = [plt.Line2D([0], [0], marker='o', color='w', 
                                     markerfacecolor=colors[i], markersize=15, 
                                     label=f'Color {i}') for i in range(3)]
        plt.legend(handles=legend_elements, loc='upper right')
        plt.title('3-Coloring of Graph')
        plt.show()
    except ImportError:
        print("Matplotlib not available for visualization")

def has_clique_4_or_larger(graph):
    """
    Quick check if graph has a clique of size 4 or larger.
    Such graphs cannot be 3-colored.
    
    Args:
        graph: NetworkX graph
        
    Returns:
        bool: True if graph has K4 or larger clique
    """
    nodes = list(graph.nodes())
    n = len(nodes)
    
    # Check all combinations of 4 nodes
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                for l in range(k + 1, n):
                    # Check if these 4 nodes form a clique
                    if (graph.has_edge(nodes[i], nodes[j]) and
                        graph.has_edge(nodes[i], nodes[k]) and
                        graph.has_edge(nodes[i], nodes[l]) and
                        graph.has_edge(nodes[j], nodes[k]) and
                        graph.has_edge(nodes[j], nodes[l]) and
                        graph.has_edge(nodes[k], nodes[l])):
                        return True
    return False

def is_color_safe(graph, node, color, coloring):
    """
    Check if assigning a color to a node is safe (doesn't conflict with neighbors).
    
    Args:
        graph: NetworkX graph
        node: Node to check
        color: Color to assign (0, 1, or 2)
        coloring: Current partial coloring
        
    Returns:
        bool: True if color assignment is safe
    """
    for neighbor in graph.neighbors(node):
        if neighbor in coloring and coloring[neighbor] == color:
            return False
    return True
    
def is_colorable(graph, visualize=False):
    """
    Version with constraint propagation - eliminates impossible colors early.
    """
    if len(graph.nodes()) == 0:
        return True, {}
    
    if len(graph.nodes()) <= 3:
        nodes = list(graph.nodes())
        coloring = {node: i for i, node in enumerate(nodes)}
        if visualize:
            visualize_coloring(graph, coloring)
        return True, coloring
    
    if has_clique_4_or_larger(graph):
        return False, {}
    
    # Initialize domains for each node (possible colors)
    domains = {node: {0, 1, 2} for node in graph.nodes()}
    
    # NOTE: This sort is the one that is typically used in greedy coloring
    # nodes = sorted(graph.nodes(), key=lambda x: graph.degree(x), reverse=True)

    # NOTE: This is a specialized version that uses the order of nodes in the computer to have faster time complexity (if done right it should be linear, we should know what to change with a correct backtracking algorithm)
    nodes = sorted(graph.nodes())

    coloring = {}
    
    if backtrack_with_propagation(graph, nodes, coloring, domains, 0):
        if visualize:
            visualize_coloring(graph, coloring)
        return True, coloring
    else:
        return False, {}


def backtrack_with_propagation(graph, nodes, coloring, domains, node_index):
    """
    Backtracking with constraint propagation.
    """
    if node_index == len(nodes):
        return True
    
    current_node = nodes[node_index]
    
    # Try colors in order of the current domain
    for color in list(domains[current_node]):
        if is_color_safe(graph, current_node, color, coloring):
            # Make assignment
            coloring[current_node] = color
            
            # Save domains before propagation
            old_domains = {node: domain.copy() for node, domain in domains.items()}
            
            # Propagate constraints (remove this color from neighbors' domains)
            valid = True
            for neighbor in graph.neighbors(current_node):
                if neighbor not in coloring and color in domains[neighbor]:
                    domains[neighbor].remove(color)
                    if len(domains[neighbor]) == 0:
                        valid = False
                        break
            
            if valid and backtrack_with_propagation(graph, nodes, coloring, domains, node_index + 1):
                return True
            
            # Backtrack: restore domains and remove assignment
            domains.update(old_domains)
            del coloring[current_node]
    
    return False

def test_is_colorable():
    # Test code

    # Create graph
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])

    # Assert that this graph is 3 colorable
    colorable, coloring = is_colorable(G)
    assert colorable == True

    # Make a non-3-colorable graph
    G.add_edge(2, 4)

    # Assert that this graph is not 3 colorable
    colorable, coloring = is_colorable(G)
    assert colorable == False

    print("All tests passed.")

def test_is_colorable_default():
    print("\nPerformance comparison on larger graph:")
    G4 = nx.petersen_graph()
    
    result3 = is_colorable(G4)
    
    print(f"With propagation: {result3[0]}")

def test_all():
    test_is_colorable()
    test_is_colorable_default()

if __name__ == "__main__":
    test_all()
    print("All tests passed.")