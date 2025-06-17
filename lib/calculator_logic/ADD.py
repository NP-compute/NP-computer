# This performs addition of two n bit variables

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit, ALL_TRI_BITS, TRI_BIT_TO_NODE
from lib.binary_logic.NOT import NOT
from lib.binary_logic.NAND import NAND
from lib.binary_logic.NOR import NOR
from lib.binary_logic.OR import OR
from lib.binary_logic.AND import AND
from lib.binary_logic.XOR import XOR
from lib.run.CONST import CONST
from lib.run.VAR import VAR
from lib.run.MEM import MEM

def ADD(computer: NPComputer, a: MEM, b: MEM, carry: int = -1) -> tuple[MEM, int]:
    """ Adds two n bit variables together

    Args:
        computer (NPComputer): The computer that this variable belongs to
        a (MEM): The first variable to add
        b (MEM): The second variable to add

    Returns:
        MEM, int: The result of the addition in the MEM and the carry bit node int
    """
    
    # Make sure the MEM has the same number of bits
    # TODO: Modify this to allow for different sized MEMs
    assert len(a) == len(b), "Both MEMs must have the same number of bits"

    # Get the number of bits we are adding
    n = len(a)

    # Check if it is a base case
    if n == 1:
        # Check if we have a carry bit to add in
        if carry == -1:
            a_bit, b_bit = a.bits[0], b.bits[0]
            return MEM(computer, bits=[XOR(computer, a_bit, b_bit)], n=1), AND(computer, a_bit, b_bit)
        else:
            a_bit, b_bit = a.bits[0], b.bits[0]
            new_carry: int = OR(computer, OR(computer, AND(computer, a_bit, b_bit), AND(computer, a_bit, carry)), AND(computer, carry, b_bit))
            return MEM(computer, bits=[XOR(computer, XOR(computer, a_bit, b_bit), carry)], n=1), new_carry
    
    # IMPORTANT NOTE: The 2 bit addition is untested due to the increase in complexity of the graph coloring algorithm
    # We need to use recursion to add the two MEMs together
    a_upper, a_lower = a.get_upper_half(), a.get_lower_half()
    b_upper, b_lower = b.get_upper_half(), b.get_lower_half()

    add_lower, carry_lower = ADD(computer, a_lower, b_lower, carry=-1)
    add_upper, carry_upper = ADD(computer, a_upper, b_upper, carry_lower)

    sum_result = add_upper.merge(add_lower)
    return sum_result, carry_upper

def test_ADD00():
    """ Test the ADD function with two 0 bit MEMs """
    computer = NPComputer()
    a = CONST(computer, value=0, n=1)
    b = CONST(computer, value=0, n=1)

    result, carry = ADD(computer, a, b)

    # Run the computer to get the result
    is_solvable, mapping = computer.get_result_mapping()

    assert is_solvable is True, "ADD(0, 0) should be colorable"
    assert mapping[result.bits[0]] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(0, 0) should return 0"
    assert mapping[carry] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(0, 0) should return carry 0"

def test_ADD01():
    """ Test the ADD function with 0 + 1 """
    computer = NPComputer()
    a = CONST(computer, value=0, n=1)
    b = CONST(computer, value=1, n=1)

    result, carry = ADD(computer, a, b)

    # Run the computer to get the result
    is_solvable, mapping = computer.get_result_mapping()

    assert is_solvable is True, "ADD(0, 1) should be colorable"
    assert mapping[result.bits[0]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(0, 1) should return 1"
    assert mapping[carry] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(0, 1) should return carry 0"

def test_ADD10():
    """ Test the ADD function with 1 + 0 """
    computer = NPComputer()
    a = CONST(computer, value=1, n=1)
    b = CONST(computer, value=0, n=1)

    result, carry = ADD(computer, a, b)

    # Run the computer to get the result
    is_solvable, mapping = computer.get_result_mapping()

    assert is_solvable is True, "ADD(1, 0) should be colorable"
    assert mapping[result.bits[0]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(1, 0) should return 1"
    assert mapping[carry] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(1, 0) should return carry 0"

def test_ADD11():
    """ Test the ADD function with 1 + 1 """
    computer = NPComputer()
    a = CONST(computer, value=1, n=1)
    b = CONST(computer, value=1, n=1)

    result, carry = ADD(computer, a, b)

    # Run the computer to get the result
    is_solvable, mapping = computer.get_result_mapping()

    assert is_solvable is True, "ADD(1, 1) should be colorable"
    assert mapping[result.bits[0]] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(1, 1) should return 0"
    assert mapping[carry] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(1, 1) should return carry 1"

def test_ADD_small():
    """ Test the ADD function with two 0 bit MEMs """
    computer = NPComputer()
    a = CONST(computer, value=2, n=2)
    b = CONST(computer, value=1, n=2)

    result, carry = ADD(computer, a, b)

    # Run the computer to get the result
    is_solvable, mapping = computer.get_result_mapping()

    assert is_solvable is True, "ADD(1, 2) should be colorable"
    assert mapping[result.bits[0]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(1, 2) first bit should return 1"
    assert mapping[result.bits[1]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(1, 2) second bit should return 1"
    assert mapping[carry] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(1, 2) should return carry 0"

def test_ADD_big():
    """ Test the ADD function with two 0 bit MEMs """
    computer = NPComputer()
    a = CONST(computer, value=3, n=4)
    b = CONST(computer, value=4, n=4)

    result, carry = ADD(computer, a, b)

    # Run the computer to get the result
    is_solvable, mapping = computer.get_result_mapping()

    assert is_solvable is True, "ADD(3, 4) should be colorable"
    assert mapping[result.bits[0]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(3, 4) first bit should return 1"
    assert mapping[result.bits[1]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(3, 4) second bit should return 1"
    assert mapping[result.bits[2]] == mapping[TRI_BIT_TO_NODE[TriBit.ONE]], "ADD(3, 4) third bit should return 0"
    assert mapping[result.bits[3]] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(3, 4) fourth bit should return 0"
    assert mapping[carry] == mapping[TRI_BIT_TO_NODE[TriBit.ZERO]], "ADD(3, 4) should return carry 0"

def test_all():
    """ Run all tests for the ADD function """
    test_ADD00()
    test_ADD01()
    test_ADD10()
    test_ADD11()
    test_ADD_small()
    # test_ADD_big()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")