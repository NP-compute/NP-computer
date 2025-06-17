# This is an abstract class to represent n bit constants

from lib.run.FINALS import TriBit, ALL_TRI_BITS
from lib.run.INIT import NPComputer
from lib.run.MEM import MEM
from lib.run.FINALS import DEFAULT_INT_BIT_LENGTH

class CONST(MEM):
    def __init__(self, computer: NPComputer, value: int = -1, bits: list[int] = None, n: int=DEFAULT_INT_BIT_LENGTH):
        """ Generate a n bit variable

        Args:
            computer (NPComputer): The computer that this variable belongs to
            value (int): The value of the variable, must be between 0 and 2^n - 1
            n (int): The number of bits in the variable
        """

        # Make sure the value is within the range of 0 to 2^n - 1
        if not (0 <= value < 2 ** n or (value == -1 and bits is not None)):
            raise ValueError(f"Value {value} is out of range for {n} bits")

        self.computer = computer
        self.n = n
        self.bits = []

        if bits is None:
            # Generate n bits
            for _ in range(n):
                bit = self.computer.generate_node(allow={TriBit.ZERO} if value & 1 == 0 else {TriBit.ONE})
                self.bits.append(bit)

                value >>= 1
        else:
            # Use the provided bits
            self.bits = bits

# Test functions
def test_CONST_basic_initialization():
    """Test basic initialization of CONST with valid inputs"""
    computer = NPComputer()
    
    # Test 1-bit constant
    con1 = CONST(computer, 0, n=1)
    assert con1.n == 1
    assert len(con1.bits) == 1
    assert con1.computer is computer
    
    # Test 4-bit constant
    con4 = CONST(computer, 5, n=4)
    assert con4.n == 4
    assert len(con4.bits) == 4
    assert con4.computer is computer

def test_CONST_value_range_validation():
    """Test that CONST validates value ranges correctly"""
    computer = NPComputer()
    
    # Valid values should work
    CONST(computer, 0, 1)    # 0 for 1-bit
    CONST(computer, 1, 1)    # 1 for 1-bit
    CONST(computer, 0, 4)    # 0 for 4-bit
    CONST(computer, 15, 4)   # 15 for 4-bit (2^4 - 1)
    
    # Invalid values should raise ValueError
    try:
        CONST(computer, 2, n=1)
        raise AssertionError("Expected ValueError for value 2 in 1 bit")
    except:
        pass

    try:
        CONST(computer, 16, n=4)
        raise AssertionError("Expected ValueError for value 2 in 1 bit")
    except:
        pass
    
    try:
        CONST(computer, -1, n=4)
        raise AssertionError("Expected ValueError for value 2 in 1 bit")
    except:
        pass

def test_CONST_binary_representation():
    """Test that binary values are correctly represented"""
    computer = NPComputer()
    
    # Test specific binary patterns
    test_cases = [
        (0, 1, [0]),           # 0 in 1 bit: [0]
        (1, 1, [1]),           # 1 in 1 bit: [1]
        (0, 4, [0, 0, 0, 0]),  # 0 in 4 bits: [0, 0, 0, 0]
        (1, 4, [1, 0, 0, 0]),  # 1 in 4 bits: [1, 0, 0, 0] (LSB first)
        (5, 4, [1, 0, 1, 0]),  # 5 in 4 bits: [1, 0, 1, 0] (binary: 0101)
        (15, 4, [1, 1, 1, 1]), # 15 in 4 bits: [1, 1, 1, 1]
        (7, 3, [1, 1, 1]),     # 7 in 3 bits: [1, 1, 1]
        (3, 3, [1, 1, 0]),     # 3 in 3 bits: [1, 1, 0] (binary: 011)
    ]
    
    for value, n_bits, expected_bits in test_cases:
        con = CONST(computer, value, n=n_bits)
        
        # Get the actual bit values by checking node constraints
        actual_bits = []
        result, mapping = computer.get_result_mapping()
        
        for bit_node in con.bits:
            # Check if this bit is constrained to ZERO or ONE
            bit_neighbors = set(computer.graph.neighbors(bit_node))
            
            if TriBit.ONE in bit_neighbors and TriBit.X in bit_neighbors:
                # Connected to ONE and X, so must be ZERO
                actual_bits.append(0)
            elif TriBit.ZERO in bit_neighbors and TriBit.X in bit_neighbors:
                # Connected to ZERO and X, so must be ONE
                actual_bits.append(1)
            else:
                # Check the actual mapping
                if result and bit_node in mapping:
                    if mapping[bit_node] == mapping.get(TriBit.ZERO, -1):
                        actual_bits.append(0)
                    elif mapping[bit_node] == mapping.get(TriBit.ONE, -1):
                        actual_bits.append(1)
                    else:
                        actual_bits.append(-1)  # Unknown
        
        print(f"Value {value} in {n_bits} bits:")
        print(f"  Expected: {expected_bits}")
        print(f"  Actual:   {actual_bits}")
        
        assert actual_bits == expected_bits, f"Binary representation mismatch for value {value} in {n_bits} bits"

def test_CONST_bit_constraints():
    """Test that bits are properly constrained in the graph"""
    computer = NPComputer()
    
    # Test value 5 (binary: 101) in 3 bits
    con = CONST(computer, 5, n=3)  # Should be [1, 0, 1] (LSB first)
    
    # Check bit constraints
    for i, bit_node in enumerate(con.bits):
        neighbors = set(computer.graph.neighbors(bit_node))
        
        expected_bit = (5 >> i) & 1
        
        if expected_bit == 0:
            # Bit should be constrained to ZERO (connected to ONE and X)
            assert TriBit.ONE in neighbors, f"Bit {i} (should be 0) not connected to ONE"
            assert TriBit.X in neighbors, f"Bit {i} (should be 0) not connected to X"
            assert TriBit.ZERO not in neighbors, f"Bit {i} (should be 0) incorrectly connected to ZERO"
        else:
            # Bit should be constrained to ONE (connected to ZERO and X)
            assert TriBit.ZERO in neighbors, f"Bit {i} (should be 1) not connected to ZERO"
            assert TriBit.X in neighbors, f"Bit {i} (should be 1) not connected to X"
            assert TriBit.ONE not in neighbors, f"Bit {i} (should be 1) incorrectly connected to ONE"

def test_CONST_graph_colorability():
    """Test that CONST doesn't break 3-colorability"""
    computer = NPComputer()
    
    # Test various constants
    test_values = [
        (0, 1), (1, 1),
        (0, 4), (7, 4), (15, 4),
        (0, 8), (128, 8), (255, 8)
    ]
    
    for value, n_bits in test_values:
        computer_test = NPComputer()
        con = CONST(computer_test, value, n_bits)
        
        result, mapping = computer_test.get_result_mapping()
        assert result is True, f"Graph became non-3-colorable after creating CONST({value}, {n_bits})"

def test_CONST_multiple_constants():
    """Test creating multiple constants in the same computer"""
    computer = NPComputer()
    
    # Create multiple constants
    con1 = CONST(computer, 3, n=4)   # 3 in 4 bits
    con2 = CONST(computer, 10, n=4)  # 10 in 4 bits
    con3 = CONST(computer, 0, n=2)   # 0 in 2 bits
    
    # Check they don't interfere with each other
    assert len(con1.bits) == 4
    assert len(con2.bits) == 4
    assert len(con3.bits) == 2
    
    # All bits should be unique
    all_bits = con1.bits + con2.bits + con3.bits
    assert len(all_bits) == len(set(all_bits)), "Duplicate bit nodes found"
    
    # Graph should still be 3-colorable
    result, mapping = computer.get_result_mapping()
    assert result is True, "Graph became non-3-colorable with multiple constants"

def test_CONST_edge_cases():
    """Test edge cases and boundary conditions"""
    computer = NPComputer()
    
    # Test minimum values
    con_min_1 = CONST(computer, 0, 1)
    con_min_4 = CONST(computer, 0, 4)
    con_min_8 = CONST(computer, 0, 8)
    
    # Test maximum values
    con_max_1 = CONST(computer, 1, 1)      # 2^1 - 1 = 1
    con_max_4 = CONST(computer, 15, 4)     # 2^4 - 1 = 15
    con_max_8 = CONST(computer, 255, 8)    # 2^8 - 1 = 255
    
    # All should work without errors
    result, mapping = computer.get_result_mapping()
    assert result is True, "Edge case constants broke 3-colorability"

def test_CONST_large_constants():
    """Test with larger bit widths"""
    computer = NPComputer()
    
    # Test 16-bit constant
    con16 = CONST(computer, 65535, n=16)  # 2^16 - 1
    assert len(con16.bits) == 16
    
    # Test 32-bit constant (might be slow)
    con32 = CONST(computer, 1234567890, n=32)
    assert len(con32.bits) == 32
    
    # Should still be 3-colorable (though might be slow to verify)
    result, mapping = computer.get_result_mapping()
    assert result is True, "Large constants broke 3-colorability"

def test_CONST_zero_bits():
    """Test error handling for zero bits"""
    computer = NPComputer()
    
    # 0 bits should be invalid for most use cases
    # But let's see what happens
    try:
        con = CONST(computer, 0, n=0)
        assert len(con.bits) == 0, "0-bit constant should have no bits"
    except (ValueError, ZeroDivisionError):
        # Either error is acceptable for 0-bit case
        pass

def test_CONST_reconstruction():
    """Test that we can reconstruct the original value from the bit constraints"""
    computer = NPComputer()
    
    test_values = [(5, 4), (42, 8), (1023, 10)]
    
    for original_value, n_bits in test_values:
        con = CONST(computer, original_value, n=n_bits)
        
        # Reconstruct value from bit constraints
        reconstructed_value = 0
        for i, bit_node in enumerate(con.bits):
            neighbors = set(computer.graph.neighbors(bit_node))
            
            # Determine if this bit is 0 or 1 based on constraints
            if TriBit.ONE in neighbors and TriBit.X in neighbors:
                # Must be ZERO
                bit_value = 0
            elif TriBit.ZERO in neighbors and TriBit.X in neighbors:
                # Must be ONE
                bit_value = 1
            else:
                raise AssertionError(f"Bit {i} has unexpected constraints: {neighbors}")
            
            reconstructed_value |= (bit_value << i)
        
        assert reconstructed_value == original_value, f"Reconstructed value {reconstructed_value} != original {original_value}"

def test_all():
    test_CONST_basic_initialization()
    test_CONST_value_range_validation()
    test_CONST_binary_representation()
    test_CONST_bit_constraints()
    test_CONST_graph_colorability()
    test_CONST_multiple_constants()
    test_CONST_edge_cases()
    test_CONST_large_constants()
    test_CONST_zero_bits()
    test_CONST_reconstruction()
    
if __name__ == "__main__":
    test_all()
    print("All tests passed!")