# This performs 2 bit AND logic operation
# NOTE: This logic is hard to follow, please consult README.md in this directory for explanation
# NOTE: I am using custom notation for the variables below
    # Ex: x_1t_2f means x input but 1 is now true and 2 (or rather X) is now false

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS
from lib.binary_logic.SWAP import SWAP
from lib.binary_logic.NOT import NOT

def AND(computer: NPComputer, x_id: int, y_id: int) -> int:
    
    ### There are three restrictions for the AND functionality followed by a filter

    ## These are the three restrictions:
    # 1. Dont allow 0 output if both inputs arent 1
    x_1t_2f = SWAP(computer, NOT(computer, x_id), from_poss=[TriBit.ZERO, TriBit.ONE], to_poss=[TriBit.ONE, TriBit.X])
    y_1t_2f = SWAP(computer, NOT(computer, y_id), from_poss=[TriBit.ZERO, TriBit.ONE], to_poss=[TriBit.ONE, TriBit.X])
    first_restriction = computer.generate_node(allow={TriBit.ZERO, TriBit.X})
    computer.add_edge(x_1t_2f, first_restriction)
    computer.add_edge(y_1t_2f, first_restriction)

    # 2. Dont allow 1 output if both inputs are 1
    x_2t_0f = NOT(computer, SWAP(computer, x_id, from_poss=[TriBit.ONE, TriBit.ZERO], to_poss=[TriBit.ZERO, TriBit.X]), between={TriBit.ZERO, TriBit.X})
    y_2t_0f = NOT(computer, SWAP(computer, y_id, from_poss=[TriBit.ONE, TriBit.ZERO], to_poss=[TriBit.ZERO, TriBit.X]), between={TriBit.ZERO, TriBit.X})
    second_restriction = computer.generate_node(allow={TriBit.ONE, TriBit.X})
    computer.add_edge(x_2t_0f, second_restriction)
    computer.add_edge(y_2t_0f, second_restriction)

    # 3. Dont allow X output if both inputs are 1
    x_1t_0f = x_id
    y_0t_1f = NOT(computer, y_id)
    third_restriction = computer.generate_node()
    computer.add_edge(x_1t_0f, third_restriction)
    computer.add_edge(y_0t_1f, third_restriction)

    # Input to the filter
    filter_input = computer.generate_node()
    computer.add_edge(first_restriction, filter_input)
    computer.add_edge(second_restriction, filter_input)
    computer.add_edge(third_restriction, filter_input)

    ### This is the filter to change 1, 2 to 0 and 0 to 1, to thus follow the logic of a AND gate
    temp_flipper = computer.generate_node(allow={TriBit.ONE, TriBit.X})
    output = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    computer.add_edge(filter_input, temp_flipper)
    computer.add_edge(temp_flipper, output)
    computer.add_edge(filter_input, output)

    return output

def test_AND_00():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform NOT operation
    result_node = AND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "AND operation failed for 00 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "AND operation did not return 0 for 00 input"

def test_AND_01():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ZERO})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform NOT operation
    result_node = AND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "AND operation failed for 01 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "AND operation did not return 0 for 01 input"

def test_AND_10():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ZERO})

    # Perform NOT operation
    result_node = AND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "AND operation failed for 10 input"
    assert mapping[result_node] == mapping[TriBit.ZERO], "AND operation did not return 0 for 10 input"

def test_AND_11():
    computer = NPComputer()

    # Create a node that is one
    input_node_0 = computer.generate_node(allow={TriBit.ONE})
    input_node_1 = computer.generate_node(allow={TriBit.ONE})

    # Perform NOT operation
    result_node = AND(computer, input_node_0, input_node_1)

    # Get the mapping of nodes to colors
    result, mapping = computer.get_result_mapping()

    # Make sure the input node is 1 and the result node is 0
    assert result is True, "AND operation failed for 11 input"
    assert mapping[result_node] == mapping[TriBit.ONE], "AND operation did not return 1 for 11 input"

def test_all():
    test_AND_00()
    test_AND_01()
    test_AND_10()
    test_AND_11()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")