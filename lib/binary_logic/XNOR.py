# This performs 2 bit XNOR logic operation

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS, TRI_BIT_TO_NODE
from lib.binary_logic.NAND import NAND
from lib.binary_logic.OR import OR

def XNOR(computer: NPComputer, x_id: int, y_id: int) -> int:
    
    return NAND(computer, OR(computer, x_id, y_id), NAND(computer, x_id, y_id))

def test_XNOR_00():
    computer = NPComputer()

    # Create two nodes that are zero
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform XNOR operation
    result_node = XNOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the operation succeeded and result is 1 (XNOR(0,0) = 1)
    assert result is True, "XNOR operation failed for 00 input"
    assert mapping[result_node] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "XNOR operation did not return 1 for 00 input"

def test_XNOR_01():
    computer = NPComputer()

    # Create nodes: first zero, second one
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform XNOR operation
    result_node = XNOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the operation succeeded and result is 0 (XNOR(0,1) = 0)
    assert result is True, "XNOR operation failed for 01 input"
    assert mapping[result_node] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "XNOR operation did not return 0 for 01 input"

def test_XNOR_10():
    computer = NPComputer()

    # Create nodes: first one, second zero
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform XNOR operation
    result_node = XNOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the operation succeeded and result is 0 (XNOR(1,0) = 0)
    assert result is True, "XNOR operation failed for 10 input"
    assert mapping[result_node] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "XNOR operation did not return 0 for 10 input"

def test_XNOR_11():
    computer = NPComputer()

    # Create two nodes that are one
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform XNOR operation
    result_node = XNOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the operation succeeded and result is 1 (XNOR(1,1) = 1)
    assert result is True, "XNOR operation failed for 11 input"
    assert mapping[result_node] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "XNOR operation did not return 1 for 11 input"

def test_all():
    test_XNOR_00()
    test_XNOR_01()
    test_XNOR_10()
    test_XNOR_11()

if __name__ == "__main__":
    test_all()
    print("All XNOR tests passed!")