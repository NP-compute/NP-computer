# This is a function to check if a given graph is colorable with k colors (will be used for 3 mostly)

import networkx as nx
import matplotlib.pyplot as plt

def is_colorable(graph, k=3, visualize=False):
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
    

if __name__ == "__main__":
    # Test code

    # Create graph
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])

    # Assert that this graph is 3 colorable
    colorable, coloring = is_colorable(G, k=3, visualize=False)
    assert colorable == True

    # Make a non-3-colorable graph
    G.add_edge(2, 4)

    # Assert that this graph is not 3 colorable
    colorable, coloring = is_colorable(G, k=3, visualize=False)
    assert colorable == False

    print("All tests passed.")