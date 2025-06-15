# This maintains a set value for the logic 0, 1, and X
from enum import Enum

class TriBit(Enum):
    ZERO = 0
    ONE = 1
    X = 'X'

ALL_TRI_BITS = {TriBit.ZERO, TriBit.ONE, TriBit.X}