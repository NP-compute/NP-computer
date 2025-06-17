# This is the basic memory block, only used as a base
from lib.run.FINALS import DEFAULT_INT_BIT_LENGTH
from lib.run.INIT import NPComputer

class MEM:
    def __init__(self, computer, bits: list[int] = [], n: int=DEFAULT_INT_BIT_LENGTH):
        self.computer = computer
        self.n = n
        self.bits = bits[:]

    def __len__(self):
        """ Returns the number of bits in this MEM """
        return self.n
    
    def get_lower_half(self):
        """ Returns the lower half of the MEM """
        bits = self.bits[:self.n // 2]
        return self.__class__(self.computer, bits=bits, n=len(bits))

    def get_upper_half(self):
        """ Returns the upper half of the MEM """
        bits = self.bits[self.n // 2:]
        return self.__class__(self.computer, bits=bits, n=len(bits))
    
    def merge(self, other):
        """ Merges this MEM with another MEM """
        new_bits = self.bits + other.bits
        return self.__class__(self.computer, bits=new_bits, n=len(new_bits))
    
# Test Functions
def test_merge_basic():
    """Test basic merge functionality"""
    computer = NPComputer()
    
    # Create two simple MEMs
    mem1 = MEM(computer, bits=[1, 2, 3], n=3)
    mem2 = MEM(computer, bits=[4, 5], n=2)
    
    # Merge them
    merged = mem1.merge(mem2)
    
    # Check results
    assert merged.bits == [1, 2, 3, 4, 5], "Merged bits should be concatenated"
    assert merged.n == 5, "Merged n should be sum of original n values"
    assert len(merged) == 5, "Length should match n"
    assert merged.computer is computer, "Computer should be preserved"
    assert isinstance(merged, MEM), "Result should be MEM instance"

def test_all():
    """Run all tests"""
    test_merge_basic()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")