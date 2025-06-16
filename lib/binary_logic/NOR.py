# This performs 2 bit NOR logic operation

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS
from lib.binary_logic.NOT import NOT
from lib.binary_logic.AND import AND

def NOR(computer: NPComputer, x_id: int, y_id: int) -> int:
    
    return AND(computer, NOT(computer, x_id), NOT(computer, y_id))

def test_NOR_00():
    computer = NPComputer()

    # Create two nodes that are zero
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform OR operation
    result_node = NOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    assert result is True, "NOR operation failed for 00 input"
    assert mapping[result_node] == mapping[TriBit.ONE], "NOR operation did not return 1 for 00 input"

def test_NOR_01():
    computer = NPComputer()

    # Create nodes: first zero, second one
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform OR operation
    result_node = NOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    assert result is True, "NOR operation failed for 01 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "NOR operation did not return 0 for 01 input"

def test_NOR_10():
    computer = NPComputer()

    # Create nodes: first one, second zero
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform OR operation
    result_node = NOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    assert result is True, "NOR operation failed for 10 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "NOR operation did not return 0 for 10 input"

def test_NOR_11():
    computer = NPComputer()

    # Create two nodes that are one
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform OR operation
    result_node = NOR(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    assert result is True, "NOR operation failed for 11 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "NOR operation did not return 0 for 11 input"

def test_all():
    test_NOR_00()
    test_NOR_01()
    test_NOR_10()
    test_NOR_11()

if __name__ == "__main__":
    test_all()
    print("All OR tests passed!")