# This is an abstract class to represent n bit variables

from lib.run.FINALS import TriBit, ALL_TRI_BITS
from lib.run.INIT import NPComputer
from lib.run.MEM import MEM
from lib.run.FINALS import DEFAULT_INT_BIT_LENGTH

class VAR(MEM):
    def __init__(self, computer: NPComputer, bits: list[int] = None, n: int=DEFAULT_INT_BIT_LENGTH):
        """ Generate a n bit variable

        Args:
            g (NPComputer): The computer that this variable belongs to
            n (int): The number of bits in the variable
        """

        self.computer = computer
        self.n = n
        self.bits = []

        if bits is None:
            # Generate n bits
            for _ in range(n):
                bit = self.computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
                self.bits.append(bit)
        else:
            # Use the provided bits
            self.bits = bits

# Test functions
def test_VAR_basic_initialization():
    """Test basic initialization of VAR with default parameters"""
    computer = NPComputer()
    
    # Test with default bit length
    var = VAR(computer)
    assert var.computer is computer
    assert var.n == DEFAULT_INT_BIT_LENGTH
    assert len(var.bits) == DEFAULT_INT_BIT_LENGTH
    assert isinstance(var, MEM), "VAR should inherit from MEM"
    
    # Test with custom bit length
    var8 = VAR(computer, n=8)
    assert var8.n == 8
    assert len(var8.bits) == 8

def test_VAR_custom_bit_length():
    """Test VAR with various custom bit lengths"""
    computer = NPComputer()
    
    test_lengths = [1, 4, 8, 16, 64]
    
    for n in test_lengths:
        var = VAR(computer, n=n)
        assert var.n == n
        assert len(var.bits) == n
        assert var.computer is computer

def test_VAR_with_provided_bits():
    """Test VAR initialization with pre-existing bit nodes"""
    computer = NPComputer()
    
    # Create some bit nodes manually
    bit1 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    bit2 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    bit3 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    existing_bits = [bit1, bit2, bit3]
    
    # Create VAR with existing bits
    var = VAR(computer, bits=existing_bits, n=3)
    
    assert var.bits == existing_bits
    assert var.n == 3
    assert len(var.bits) == 3
    assert var.computer is computer

def test_VAR_bit_constraints():
    """Test that VAR bits are properly constrained to ZERO or ONE only"""
    computer = NPComputer()
    var = VAR(computer, n=4)
    
    # Check that each bit can only be ZERO or ONE (not X)
    for bit_node in var.bits:
        neighbors = set(computer.graph.neighbors(bit_node))
        
        # Bit should be connected to X (constraint), but not both ZERO and ONE
        assert TriBit.X in neighbors, f"Bit {bit_node} should be connected to X as constraint"
        
        # Should NOT be connected to both ZERO and ONE (that would over-constrain)
        # Actually, for unconstrained bits that can be 0 OR 1, they should only be connected to X
        zero_connected = TriBit.ZERO in neighbors
        one_connected = TriBit.ONE in neighbors
        
        # For a bit that can be either 0 or 1, it should only be connected to X
        assert not (zero_connected and one_connected), f"Bit {bit_node} over-constrained"

def test_VAR_graph_colorability():
    """Test that VAR doesn't break 3-colorability"""
    computer = NPComputer()
    
    # Test various bit lengths
    test_lengths = [1, 4, 8, 16, 32]
    
    for n in test_lengths:
        computer_test = NPComputer()
        var = VAR(computer_test, n=n)
        
        result, mapping = computer_test.get_result_mapping()
        assert result is True, f"Graph became non-3-colorable after creating {n}-bit VAR"

def test_VAR_get_lower_half():
    """Test the get_lower_half method"""
    computer = NPComputer()
    
    # Test with even number of bits
    var8 = VAR(computer, n=8)
    lower_half = var8.get_lower_half()
    
    assert lower_half.n == 4
    assert len(lower_half.bits) == 4
    assert lower_half.bits == var8.bits[:4]
    assert lower_half.computer is computer
    assert isinstance(lower_half, VAR)
    
    # Test with odd number of bits
    var7 = VAR(computer, n=7)
    lower_half_odd = var7.get_lower_half()
    
    assert lower_half_odd.n == 3  # 7 // 2 = 3
    assert len(lower_half_odd.bits) == 3
    assert lower_half_odd.bits == var7.bits[:3]

def test_VAR_get_upper_half():
    """Test the get_upper_half method"""
    computer = NPComputer()
    
    # Test with even number of bits
    var8 = VAR(computer, n=8)
    upper_half = var8.get_upper_half()
    
    assert upper_half.n == 4
    assert len(upper_half.bits) == 4
    assert upper_half.bits == var8.bits[4:]
    assert upper_half.computer is computer
    assert isinstance(upper_half, VAR)
    
    # Test with odd number of bits
    var7 = VAR(computer, n=7)
    upper_half_odd = var7.get_upper_half()
    
    assert upper_half_odd.n == 4  # 7 - (7 // 2) = 7 - 3 = 4
    assert len(upper_half_odd.bits) == 4
    assert upper_half_odd.bits == var7.bits[3:]

def test_VAR_halves_complete_original():
    """Test that lower and upper halves together contain all original bits"""
    computer = NPComputer()
    
    test_lengths = [2, 4, 6, 8, 9, 15, 16]
    
    for n in test_lengths:
        var = VAR(computer, n=n)
        lower = var.get_lower_half()
        upper = var.get_upper_half()
        
        # Combined halves should equal original
        combined_bits = lower.bits + upper.bits
        assert combined_bits == var.bits, f"Halves don't reconstruct original for n={n}"
        
        # No overlap between halves
        assert set(lower.bits).isdisjoint(set(upper.bits)), f"Overlapping bits in halves for n={n}"
        
        # Correct lengths
        assert len(lower.bits) == n // 2, f"Lower half wrong length for n={n}"
        assert len(upper.bits) == n - (n // 2), f"Upper half wrong length for n={n}"

def test_VAR_multiple_variables():
    """Test creating multiple variables in the same computer"""
    computer = NPComputer()
    
    # Create multiple variables
    var1 = VAR(computer, n=4)
    var2 = VAR(computer, n=6)
    var3 = VAR(computer, n=2)
    
    # All should have correct properties
    assert var1.n == 4 and len(var1.bits) == 4
    assert var2.n == 6 and len(var2.bits) == 6
    assert var3.n == 2 and len(var3.bits) == 2
    
    # All bits should be unique
    all_bits = var1.bits + var2.bits + var3.bits
    assert len(all_bits) == len(set(all_bits)), "Duplicate bit nodes found"
    
    # Graph should still be 3-colorable
    result, mapping = computer.get_result_mapping()
    assert result is True, "Graph became non-3-colorable with multiple variables"

def test_VAR_nested_halves():
    """Test getting halves of halves"""
    computer = NPComputer()
    var16 = VAR(computer, n=16)
    
    # Get halves
    lower8 = var16.get_lower_half()    # bits 0-7
    upper8 = var16.get_upper_half()    # bits 8-15
    
    # Get quarters
    quarter1 = lower8.get_lower_half()  # bits 0-3
    quarter2 = lower8.get_upper_half()  # bits 4-7
    quarter3 = upper8.get_lower_half()  # bits 8-11
    quarter4 = upper8.get_upper_half()  # bits 12-15
    
    # Check properties
    assert quarter1.n == 4 and len(quarter1.bits) == 4
    assert quarter2.n == 4 and len(quarter2.bits) == 4
    assert quarter3.n == 4 and len(quarter3.bits) == 4
    assert quarter4.n == 4 and len(quarter4.bits) == 4
    
    # Check bit sequences
    expected_bits = var16.bits
    actual_bits = quarter1.bits + quarter2.bits + quarter3.bits + quarter4.bits
    assert actual_bits == expected_bits, "Nested halves don't reconstruct original"

def test_VAR_edge_cases():
    """Test edge cases for VAR"""
    computer = NPComputer()
    
    # Test 1-bit variable
    var1 = VAR(computer, n=1)
    assert var1.n == 1
    assert len(var1.bits) == 1
    
    # Test halves of 1-bit variable
    lower = var1.get_lower_half()
    upper = var1.get_upper_half()
    
    assert lower.n == 0 and len(lower.bits) == 0  # 1 // 2 = 0
    assert upper.n == 1 and len(upper.bits) == 1  # 1 - 0 = 1
    
    # Test 2-bit variable
    var2 = VAR(computer, n=2)
    lower2 = var2.get_lower_half()
    upper2 = var2.get_upper_half()
    
    assert lower2.n == 1 and len(lower2.bits) == 1
    assert upper2.n == 1 and len(upper2.bits) == 1

def test_VAR_zero_bits():
    """Test VAR with zero bits (edge case)"""
    computer = NPComputer()
    
    # Create VAR with 0 bits using provided bits
    var0 = VAR(computer, bits=[], n=0)
    assert var0.n == 0
    assert len(var0.bits) == 0
    
    # Test halves of 0-bit variable
    lower = var0.get_lower_half()
    upper = var0.get_upper_half()
    
    assert lower.n == 0 and len(lower.bits) == 0
    assert upper.n == 0 and len(upper.bits) == 0

def test_VAR_inheritance():
    """Test that VAR properly inherits from MEM"""
    computer = NPComputer()
    var = VAR(computer, n=4)
    
    assert isinstance(var, MEM), "VAR should inherit from MEM"
    assert isinstance(var, VAR), "VAR should be instance of VAR"

def test_VAR_provided_bits_length_mismatch():
    """Test behavior when provided bits length doesn't match n parameter"""
    computer = NPComputer()
    
    # Create 3 bits but specify n=5
    bit1 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    bit2 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    bit3 = computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
    existing_bits = [bit1, bit2, bit3]
    
    # This should use the provided bits regardless of n parameter
    var = VAR(computer, bits=existing_bits, n=5)
    
    assert var.bits == existing_bits
    assert len(var.bits) == 3  # Actual bits length
    assert var.n == 5  # But n is still what was specified
    
    # This might cause issues in get_lower_half/get_upper_half
    # Let's test that too
    try:
        lower = var.get_lower_half()  # Should use first n//2 = 5//2 = 2 bits
        upper = var.get_upper_half()  # Should use remaining bits from index 2
        
        assert len(lower.bits) == 2
        assert len(upper.bits) == 1  # Only 1 bit left from index 2
    except IndexError:
        # This is expected behavior when n doesn't match actual bits length
        pass

def test_VAR_bit_node_uniqueness():
    """Test that each VAR gets unique bit nodes"""
    computer = NPComputer()
    
    var1 = VAR(computer, n=4)
    var2 = VAR(computer, n=4)
    
    # All bit nodes should be unique
    all_bits = var1.bits + var2.bits
    unique_bits = set(all_bits)
    
    assert len(all_bits) == len(unique_bits), "VAR instances share bit nodes"
    assert set(var1.bits).isdisjoint(set(var2.bits)), "VAR instances have overlapping bits"

def test_all():
    
    test_VAR_basic_initialization()
    test_VAR_custom_bit_length()
    test_VAR_with_provided_bits()
    test_VAR_bit_constraints()
    test_VAR_graph_colorability()
    test_VAR_get_lower_half()
    test_VAR_get_upper_half()
    test_VAR_halves_complete_original()
    test_VAR_multiple_variables()
    test_VAR_nested_halves()
    test_VAR_edge_cases()
    test_VAR_zero_bits()
    test_VAR_inheritance()
    test_VAR_provided_bits_length_mismatch()
    test_VAR_bit_node_uniqueness()

if __name__ == "__main__":
    test_all()
    print("All VAR tests passed!")