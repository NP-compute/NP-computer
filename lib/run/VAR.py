# This is an abstract class to represent n bit variables

from lib.run.FINALS import TriBit, ALL_TRI_BITS
from lib.run.INIT import NPComputer

class VAR:
    def __init__(self, computer: NPComputer, n: int):
        """ Generate a n bit variable

        Args:
            g (NPComputer): The computer that this variable belongs to
            n (int): The number of bits in the variable
        """

        self.computer = computer
        self.n = n
        self.bits = []

        # Add in the bits as 0 or 1 while saving the node ids
        for _ in range(n):
            bit = self.computer.generate_node(allow={TriBit.ZERO, TriBit.ONE})
            self.bits.append(bit)
