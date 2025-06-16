# This performs 1 bit NOT operation

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS

def NOT(computer: NPComputer, node_id: int, between={TriBit.ZERO, TriBit.ONE}) -> int:
    """ Perform NOT operation on a node in the NPComputer graph

    Args:
        computer (NPComputer): The NPComputer instance to operate on
        node_id (int): The node ID to perform NOT operation on, this has to be a node that can only be 0 or 1
        between (set, optional): The set of TriBits that the result can be, defaults to {TriBit.ZERO, TriBit.ONE}. This should almost always be {TriBit.ZERO, TriBit.ONE} unless you are swapping logic levels

    Returns:
        int: The node ID of the result of the NOT operation
    """
    
    # Create a new node that can be 0 or 1, but not X
    result_node = computer.generate_node(allow=between)

    # Connect the input node to the result node so they can't be the same value
    computer.add_edge(node_id, result_node)

    return result_node

def test_NOT_ZERO_to_ONE():
    """ Test NOT operation from 0 to 1 """

    computer = NPComputer()

    # Create a node that is zero
    input_node = computer.generate_node(allow={TriBit.ZERO})

    # Perform NOT operation
    result_node = NOT(computer, input_node)

    # Get the mapping of nodes to colors
    mapping = computer.get_mapping()

    # Make sure the input node is 0 and the result node is 1
    assert mapping[input_node] == mapping[TriBit.ZERO]
    assert mapping[result_node] == mapping[TriBit.ONE]

def test_NOT_ONE_to_ZERO():
    """ Test NOT operation from 1 to 0 """

    computer = NPComputer()

    # Create a node that is one
    input_node = computer.generate_node(allow={TriBit.ONE})

    # Perform NOT operation
    result_node = NOT(computer, input_node)

    # Get the mapping of nodes to colors
    mapping = computer.get_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert mapping[input_node] == mapping[TriBit.ONE]
    assert mapping[result_node] == mapping[TriBit.ZERO]

def test_NOT_ONE_to_X():
    """ Test NOT operation from 1 to 0 """

    computer = NPComputer()

    # Create a node that is one
    input_node = computer.generate_node(allow={TriBit.ONE})

    # Perform NOT operation
    result_node = NOT(computer, input_node, between={TriBit.ONE, TriBit.X})

    # Get the mapping of nodes to colors
    mapping = computer.get_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert mapping[result_node] == mapping[TriBit.X]

def test_all():
    test_NOT_ZERO_to_ONE()
    test_NOT_ONE_to_ZERO()
    test_NOT_ONE_to_X()

if __name__ == "__main__":
    test_all()
    print("All tests passed")