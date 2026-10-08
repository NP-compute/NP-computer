# These are AND / OR gates where every node has exactly one valid color once the inputs are colored
# The gates in lib/binary_logic give the right output, but some of their inner nodes can take more than one color
# That is fine for "is it 3 colorable", but a backtracking search that hits a BREAK later on would retry every one of those
# inner choices, which grows exponentially with the number of gates
# With these gates a failure late in the graph unwinds straight back through every gate, so the ordered search stays linear
#
# AND(a, b) uses 3 helpers (h0 can be 0/X, h1 can be 1/X, h2 can be anything) and the output z (0/1)
#   edges: b-h0, b-h1, h0-h1, a-h2, h1-h2, h1-z, h2-z
#   b = 0 -> h0 = X, h1 = 1, so z = 0 and h2 = X
#   b = 1 -> h1 = X, h0 = 0, so h2 = NOT a and z = a
#
# OR(a, b) uses the same helpers with different edges
#   edges: b-h0, b-h1, h0-h1, a-h2, h0-h2, h0-z, h2-z
#   b = 1 -> h1 = X, h0 = 0, so z = 1 and h2 = X
#   b = 0 -> h0 = X, h1 = 1, so h2 = NOT a and z = a

import itertools
from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, TRI_BIT_TO_NODE
from lib.binary_logic.NOT import NOT

def _helpers(computer: NPComputer, b_id: int):
    """ Build the h0, h1 pair that both gates share (h0 = X when b is 0, 0 when b is 1) """
    h0 = computer.generate_node(allow={TriBit.ZERO, TriBit.X})
    h1 = computer.generate_node(allow={TriBit.ONE, TriBit.X})
    computer.add_edge(b_id, h0)
    computer.add_edge(b_id, h1)
    computer.add_edge(h0, h1)
    return h0, h1

def RIGID_AND(computer: NPComputer, x_id: int, y_id: int) -> int:
    """ 2 bit AND where the coloring of the gate is unique for every input

    Args:
        computer (NPComputer): The computer to build the gate in
        x_id (int): First input, must be a 0/1 node
        y_id (int): Second input, must be a 0/1 node

    Returns:
        int: The output node
    """
    h0, h1 = _helpers(computer, y_id)
    h2 = computer.generate_node()
    output = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    computer.add_edge(x_id, h2)
    computer.add_edge(h1, h2)
    computer.add_edge(h1, output)
    computer.add_edge(h2, output)
    return output

def RIGID_OR(computer: NPComputer, x_id: int, y_id: int) -> int:
    """ 2 bit OR where the coloring of the gate is unique for every input

    Args:
        computer (NPComputer): The computer to build the gate in
        x_id (int): First input, must be a 0/1 node
        y_id (int): Second input, must be a 0/1 node

    Returns:
        int: The output node
    """
    h0, h1 = _helpers(computer, y_id)
    h2 = computer.generate_node()
    output = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    computer.add_edge(x_id, h2)
    computer.add_edge(h0, h2)
    computer.add_edge(h0, output)
    computer.add_edge(h2, output)
    return output

def RIGID_FALSE(computer: NPComputer) -> int:
    """ A node that can only be 0 """
    return computer.generate_node(allow={TriBit.ZERO})

def RIGID_TRUE(computer: NPComputer) -> int:
    """ A node that can only be 1 """
    return computer.generate_node(allow={TriBit.ONE})

def RIGID_OR_MANY(computer: NPComputer, ids: list[int]) -> int:
    """ OR together any number of 0/1 nodes (0 inputs gives a constant 0) """
    if len(ids) == 0:
        return RIGID_FALSE(computer)
    result = ids[0]
    for node in ids[1:]:
        result = RIGID_OR(computer, result, node)
    return result

def RIGID_AND_MANY(computer: NPComputer, ids: list[int]) -> int:
    """ AND together any number of 0/1 nodes (0 inputs gives a constant 1) """
    if len(ids) == 0:
        return RIGID_TRUE(computer)
    result = ids[0]
    for node in ids[1:]:
        result = RIGID_AND(computer, result, node)
    return result

def RIGID_NOT(computer: NPComputer, x_id: int) -> int:
    """ The repo NOT is already rigid (one edge to a 0/1 node) """
    return NOT(computer, x_id)

# Test functions
def all_colorings(computer: NPComputer, fixed: dict):
    """ Brute force every 3-coloring of the computer graph with the base nodes and the fixed nodes pinned """
    graph = computer.graph
    color_of = {TriBit.ZERO: 0, TriBit.ONE: 1, TriBit.X: 2}
    pinned = {node: color_of[tri_bit] for tri_bit, node in TRI_BIT_TO_NODE.items()}
    pinned.update({node: color_of[tri_bit] for node, tri_bit in fixed.items()})
    free = [node for node in sorted(graph.nodes()) if node not in pinned]
    found = []
    for colors in itertools.product((0, 1, 2), repeat=len(free)):
        coloring = dict(pinned)
        coloring.update(zip(free, colors))
        if all(coloring[u] != coloring[v] for u, v in graph.edges()):
            found.append(coloring)
    return found

def check_gate_is_rigid(gate, truth):
    tri = {0: TriBit.ZERO, 1: TriBit.ONE}
    for a, b in itertools.product((0, 1), repeat=2):
        computer = NPComputer()
        x = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
        y = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
        out = gate(computer, x, y)
        colorings = all_colorings(computer, {x: tri[a], y: tri[b]})
        assert len(colorings) == 1, f"{gate.__name__}({a}, {b}) has {len(colorings)} colorings, expected exactly 1"
        assert colorings[0][out] == truth(a, b), f"{gate.__name__}({a}, {b}) gave {colorings[0][out]}"

def test_RIGID_AND():
    check_gate_is_rigid(RIGID_AND, lambda a, b: a & b)

def test_RIGID_OR():
    check_gate_is_rigid(RIGID_OR, lambda a, b: a | b)

def test_RIGID_MANY():
    from lib.run.ORDERED_SEARCH import ordered_search
    for bits in itertools.product((0, 1), repeat=4):
        computer = NPComputer()
        ids = [computer.generate_node(allow={TriBit.ONE} if bit else {TriBit.ZERO}) for bit in bits]
        any_out = RIGID_OR_MANY(computer, ids)
        all_out = RIGID_AND_MANY(computer, ids)
        result, coloring = ordered_search(computer.graph)
        assert result is True
        assert coloring[any_out] == int(any(bits))
        assert coloring[all_out] == int(all(bits))

    computer = NPComputer()
    none_out = RIGID_OR_MANY(computer, [])
    every_out = RIGID_AND_MANY(computer, [])
    result, coloring = ordered_search(computer.graph)
    assert coloring[none_out] == 0 and coloring[every_out] == 1

def test_all():
    test_RIGID_AND()
    test_RIGID_OR()
    test_RIGID_MANY()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")
