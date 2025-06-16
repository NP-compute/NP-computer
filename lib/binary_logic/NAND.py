# This performs 2 bit NAND logic operation

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS
from lib.binary_logic.NOT import NOT
from lib.binary_logic.AND import AND

def NAND(computer: NPComputer, x_id: int, y_id: int) -> int:
    
    return NOT(computer, AND(computer, x_id, y_id))

def test_NAND_00():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform NOT operation
    result_node = NAND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "NAND operation failed for 00 input"
    assert mapping[result_node] == mapping[TriBit.ONE], "NAND operation did not return 1 for 00 input"

def test_NAND_01():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform NOT operation
    result_node = NAND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "NAND operation failed for 01 input"
    assert mapping[result_node] == mapping[TriBit.ONE], "NAND operation did not return 1 for 01 input"

def test_NAND_10():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform NOT operation
    result_node = NAND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "NAND operation failed for 10 input"
    assert mapping[result_node] == mapping[TriBit.ONE], "NAND operation did not return 1 for 10 input"

def test_NAND_11():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform NOT operation
    result_node = NAND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "NAND operation failed for 11 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "NAND operation did not return 0 for 11 input"

def test_all():
    test_NAND_00()
    test_NAND_01()
    test_NAND_10()
    test_NAND_11()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")