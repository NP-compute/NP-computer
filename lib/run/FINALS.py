# This maintains a set value for the logic 0, 1, and X
from enum import Enum

class TriBit(Enum):
    ZERO = 0
    ONE = 1
    X = 'X'

ALL_TRI_BITS = {TriBit.ZERO, TriBit.ONE, TriBit.X}

# This is a mapping for the TriBit values to the gauranteed node values
TRI_BIT_TO_NODE = {
    TriBit.ZERO: 0,
    TriBit.ONE: 1,
    TriBit.X: 2
}

# This is the default length of bit ints
DEFAULT_INT_BIT_LENGTH = 8