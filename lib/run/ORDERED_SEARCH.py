# This is a 3-coloring search that colors the nodes in a caller supplied order
# IS_COLORABLE always colors in sorted node order and starts with an O(n^4) clique check, which is too slow for big graphs
# This version is iterative (no recursion limit), lets the caller choose the order, and reports every step of the search
# The Turing machine converter uses this so the search walks the graph in the same order the machine runs

import networkx as nx
from lib.run.FINALS import TriBit, TRI_BIT_TO_NODE

# Colors are named after the TriBit of the base node that holds them (base node 0 -> color 0 etc.)
TRI_BIT_TO_COLOR = {tri_bit: node for tri_bit, node in TRI_BIT_TO_NODE.items()}
COLOR_TO_TRI_BIT = {color: tri_bit for tri_bit, color in TRI_BIT_TO_COLOR.items()}

# Try ONE first, so asking "is this node 1?" is always the first thing the search does
DEFAULT_COLOR_ORDER = (TRI_BIT_TO_COLOR[TriBit.ONE], TRI_BIT_TO_COLOR[TriBit.ZERO], TRI_BIT_TO_COLOR[TriBit.X])

# Event kinds handed to the listener
ASSIGN = "assign"        # (ASSIGN, node, color) the node was given this color
REJECT = "reject"        # (REJECT, node, color) the color clashed with a colored neighbor
BACKTRACK = "backtrack"  # (BACKTRACK, node, None) no color worked, step back to the previous node

def ordered_search(graph: nx.Graph, order: list = None, color_order: tuple = DEFAULT_COLOR_ORDER, listener=None):
    """ Chronological backtracking that colors the nodes exactly in the given order

    Args:
        graph (nx.Graph): The graph to 3-color
        order (list, optional): The order to color the nodes in, defaults to sorted node order (the order the computer built them)
        color_order (tuple, optional): The order colors are tried in for every node
        listener (callable, optional): Called as listener(event, node, color, index) for every assign, reject and backtrack

    Returns:
        (bool, dict): (is 3 colorable, mapping of nodes to colors)
    """

    order = sorted(graph.nodes()) if order is None else list(order)
    if set(order) != set(graph.nodes()) or len(order) != len(graph.nodes()):
        raise ValueError("The order must contain every node of the graph exactly once")

    coloring = {}

    # The base nodes are pinned to their own colors, any valid coloring can be renamed to match this
    for tri_bit, node in TRI_BIT_TO_NODE.items():
        if node in graph:
            coloring[node] = TRI_BIT_TO_COLOR[tri_bit]
    pinned = set(coloring)
    order = [node for node in order if node not in pinned]

    # next_try[i] is how far through color_order the node at order[i] has gotten
    next_try = [0] * len(order)
    i = 0
    while 0 <= i < len(order):
        node = order[i]
        coloring.pop(node, None)

        placed = False
        while next_try[i] < len(color_order):
            color = color_order[next_try[i]]
            next_try[i] += 1
            if all(coloring.get(neighbor) != color for neighbor in graph.neighbors(node)):
                coloring[node] = color
                placed = True
                break
            if listener:
                listener(REJECT, node, color, i)

        if placed:
            if listener:
                listener(ASSIGN, node, color, i)
            i += 1
            if i < len(order):
                next_try[i] = 0
        else:
            if listener:
                listener(BACKTRACK, node, None, i)
            next_try[i] = 0
            i -= 1

    if i < 0:
        return False, {}
    return True, coloring

# Test functions
def is_proper_coloring(graph, coloring):
    return all(coloring[u] != coloring[v] for u, v in graph.edges()) and all(c in (0, 1, 2) for c in coloring.values())

def test_ordered_search_basic():
    """ Same graphs as the IS_COLORABLE tests """
    G = nx.Graph()
    G.add_edges_from([(1, 2), (2, 3), (3, 4), (4, 1), (1, 3)])
    result, coloring = ordered_search(G)
    assert result is True
    assert is_proper_coloring(G, coloring)

    G.add_edge(2, 4)
    result, coloring = ordered_search(G)
    assert result is False

def test_ordered_search_petersen():
    G = nx.petersen_graph()
    result, coloring = ordered_search(G)
    assert result is True
    assert is_proper_coloring(G, coloring)

def test_ordered_search_respects_order():
    """ The listener sees the nodes assigned in the requested order """
    G = nx.path_graph(6)
    order = [5, 3, 1, 4, 2, 0]
    assigned = []
    ordered_search(G, order=order, listener=lambda event, node, color, index: assigned.append(node) if event == ASSIGN else None)
    # Nodes 0, 1, 2 are the pinned base nodes
    assert assigned == [5, 3, 4]

def test_ordered_search_with_computer():
    """ The base nodes are pinned so the mapping can be read as TriBits """
    from lib.run.INIT import NPComputer
    computer = NPComputer()
    node = computer.generate_node(allow={TriBit.ONE})
    computer.add_edge(node, TRI_BIT_TO_NODE[TriBit.ZERO])
    result, coloring = ordered_search(computer.graph)
    assert result is True
    assert coloring[node] == TRI_BIT_TO_COLOR[TriBit.ONE]

def test_ordered_search_bad_order():
    G = nx.path_graph(3)
    try:
        ordered_search(G, order=[0, 1])
        assert False, "Should reject an order that is missing nodes"
    except ValueError:
        pass

def test_all():
    test_ordered_search_basic()
    test_ordered_search_petersen()
    test_ordered_search_respects_order()
    test_ordered_search_with_computer()
    test_ordered_search_bad_order()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")
