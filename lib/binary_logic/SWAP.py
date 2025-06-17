# This is not a typical logic gate, but it is a better way to do tri-bit operations
# This performs 2 bit SWAP logic operation
# It takes in a node that can be one of 2 tri-bit values (like it is either 0 or 1), then switches to another 2 tri-bit values (in this example 2 or 0)
# This should only be used at a logic gate level to help generate the NAND logic gate

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS, TRI_BIT_TO_NODE

def SWAP(computer: NPComputer, input_id: int, from_poss: list[TriBit]=[TriBit.ZERO, TriBit.ONE], to_poss: list[TriBit]=[TriBit.ONE, TriBit.X]) -> int:
    """ See docstring at top of file for explanation
    Also important to note that the first value in from_poss maps to the first value in to_poss, and the second value in from_poss maps to the second value in to_poss
    Another important note is that there must be all three tri-bit values in the from_poss and to_poss sets combined (otherwise this there are better operations to use)
    Another important note is that the first from value and to value cannot be the same (to acomplish this use the SWAP then the NOT operation)
        Same with the second from value and to value
    Another important note that may be able to be relaxed in the future is that the first from value must be the same as the second to value
    Args:
        computer (NPComputer): This is the NPComputer that is being used to generate the graph
        input_id (int): This is the node id of the input node
        from_poss (list, optional): This is the possibility mapping start. Defaults to {TriBit.ZERO, TriBit.ONE}. 
        to_poss (list, optional): This is the possibility mapping end. Defaults to {TriBit.ONE, TriBit.X}.

    Returns:
        int: _description_
    """
    
    assert len(from_poss) == len(to_poss), "from_set and to_set must be the same size"
    assert len(from_poss) == 2, "from_set and to_set must be size 2"
    assert from_poss[0] != to_poss[0], "from_set and to_set cannot have the same value in the same position"
    assert from_poss[1] != to_poss[1], "from_set and to_set cannot have the same value in the same position"
    assert from_poss[1] == to_poss[0], "Current circuit needs this swapping logic to work"

    # Getting the terms to make it easier to read
    term_to_remove: TriBit = from_poss[0]
    term_to_keep: TriBit = from_poss[1]
    term_to_add: TriBit = to_poss[1]

    # NOTE: For the logic below check the README.md for a diagram of how this works

    # Make the output node
    output_id = computer.generate_node(allow={term_to_keep, term_to_add})

    # Make the top branch that connects the input to the output
    top_branch_id = computer.generate_node(allow={term_to_remove, term_to_add})
    computer.add_edge(input_id, top_branch_id)
    computer.add_edge(top_branch_id, output_id)

    # Make the bottom branch that connects the input to the output
    bottom_branch_id = computer.generate_node(allow={term_to_keep, term_to_add})
    bottom_branch_custom_not_id = computer.generate_node(allow={term_to_keep, term_to_add})
    computer.add_edge(input_id, bottom_branch_id)
    computer.add_edge(bottom_branch_id, bottom_branch_custom_not_id)
    computer.add_edge(bottom_branch_custom_not_id, output_id)

    return output_id

def test_SWAP_default_zero_to_one():
    computer = NPComputer()

    # Make the input and output nodes
    zero_input_id = computer.generate_node(allow={TriBit.ZERO})
    SWAP_output_id = SWAP(computer, zero_input_id, from_poss=[TriBit.ZERO, TriBit.ONE], to_poss=[TriBit.ONE, TriBit.X])

    # Check outputs
    result, mapping = computer.get_result_mapping()
    assert result == True
    assert mapping[SWAP_output_id] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]]

def test_SWAP_default_one_to_two():
    computer = NPComputer()

    # Make the input and output nodes
    one_input_id = computer.generate_node(allow={TriBit.ONE})
    SWAP_output_id = SWAP(computer, one_input_id, from_poss=[TriBit.ZERO, TriBit.ONE], to_poss=[TriBit.ONE, TriBit.X])

    # Check outputs
    result, mapping = computer.get_result_mapping()

    assert result == True
    assert mapping[SWAP_output_id] == mapping[TRI_BIT_TO_NODE[TriBit.X]]

def test_SWAP_not_default_one_to_two():
    computer = NPComputer()

    # Make the input and output nodes
    zero_input_id = computer.generate_node(allow={TriBit.ONE})
    SWAP_output_id = SWAP(computer, zero_input_id, from_poss=[TriBit.ONE, TriBit.X], to_poss=[TriBit.X, TriBit.ZERO])

    # Check outputs
    result, mapping = computer.get_result_mapping()
    assert result == True
    assert mapping[SWAP_output_id] == mapping[TRI_BIT_TO_NODE[TriBit.X]]

def test_SWAP_not_default_two_to_zero():
    computer = NPComputer()

    # Make the input and output nodes
    one_input_id = computer.generate_node(allow={TriBit.X})
    SWAP_output_id = SWAP(computer, one_input_id, from_poss=[TriBit.ONE, TriBit.X], to_poss=[TriBit.X, TriBit.ZERO])

    # Check outputs
    result, mapping = computer.get_result_mapping()

    assert result == True
    assert mapping[SWAP_output_id] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]]

def test_all():
    test_SWAP_default_zero_to_one()
    test_SWAP_default_one_to_two()
    test_SWAP_not_default_one_to_two()
    test_SWAP_not_default_two_to_zero()

if __name__ == "__main__":
    test_all()
    print("All tests passed")