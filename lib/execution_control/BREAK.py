# This is the core functionality that makes this special
# Up until now we have been coding linearly where one thing happens after another (even if conditionals dont control the flow, just wether it is used)
# This BREAK logic allows us to do something I call FIND
# We can generate a VAR that has no values and can represent any value 0 <= value < 2^n
# We can then build off of this logic that controls if we BREAK (make the graph not 3 colorable) or not
# This allows us to do what would take mass looping in coding landuages
# This is the reasoning behind the name FIND, and also proves why the coloring problem cant be solved in polynomial time

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS, TRI_BIT_TO_NODE
from lib.binary_logic.SWAP import SWAP
from lib.binary_logic.NOT import NOT
from lib.run.CONST import CONST

def BREAK(computer: NPComputer, x_id: int):
    """ If a 1 is inputed into this then BREAK the computer (make it not 3 colorable), otherwise do nothing

    Args:
        computer (NPComputer): This is the computer that is being built
        x_id (int): This is the id of the node that is being used to control the BREAK logic
    """
    
    # For how important this is it is quite simple
    # We connect it to a node that has to be 1

    one = computer.generate_node(allow={TriBit.ONE})
    computer.add_edge(x_id, one)

def test_BREAK_with_input_1():
    """ Test BREAK function with input 1 - should make graph not 3-colorable """
    computer = NPComputer()
    
    # Create a constant node with value 1
    const_1 = CONST(computer, value=1, n=1)
    input_node = const_1.bits[0]  # This node is constrained to be 1
    
    # Verify graph is 3-colorable before BREAK
    is_valid_before, mapping_before = computer.get_result_mapping()
    assert is_valid_before is True, "Graph should be 3-colorable before BREAK"
    
    # Apply BREAK with input 1
    BREAK(computer, input_node)
    
    # Verify graph is NOT 3-colorable after BREAK
    is_valid_after, mapping_after = computer.get_result_mapping()
    assert is_valid_after is False, "Graph should NOT be 3-colorable after BREAK with input 1"
    
    print("✓ BREAK with input 1 successfully breaks the graph (makes it not 3-colorable)")

def test_BREAK_with_input_0():
    """ Test BREAK function with input 0 - should keep graph 3-colorable """
    computer = NPComputer()
    
    # Create a constant node with value 0
    const_0 = CONST(computer, value=0, n=1)
    input_node = const_0.bits[0]  # This node is constrained to be 0
    
    # Verify graph is 3-colorable before BREAK
    is_valid_before, mapping_before = computer.get_result_mapping()
    assert is_valid_before is True, "Graph should be 3-colorable before BREAK"
    
    # Apply BREAK with input 0
    BREAK(computer, input_node)
    
    # Verify graph is still 3-colorable after BREAK
    is_valid_after, mapping_after = computer.get_result_mapping()
    assert is_valid_after is True, "Graph should remain 3-colorable after BREAK with input 0"
    
    print("✓ BREAK with input 0 preserves graph 3-colorability")

def test_all():
    """Run both BREAK test cases"""
    
    test_BREAK_with_input_1()
    test_BREAK_with_input_0()
    
if __name__ == "__main__":
    test_all()
    print("All BREAK tests passed successfully!")