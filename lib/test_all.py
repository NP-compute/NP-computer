# This is a script to test all the components of the library
def test_all():

    from lib.run import IS_COLORABLE
    IS_COLORABLE.test_all()

    from lib.run import INIT
    INIT.test_all()

    from lib.binary_logic import NOT
    NOT.test_all()

    from lib.binary_logic import SWAP
    SWAP.test_all()

    from lib.binary_logic import AND
    AND.test_all()

    from lib.binary_logic import NAND
    NAND.test_all()

    from lib.binary_logic import OR
    OR.test_all()

    from lib.binary_logic import NOR
    NOR.test_all()

    from lib.binary_logic import XOR
    XOR.test_all()

    from lib.binary_logic import XNOR
    XNOR.test_all()

    from lib.run.CONST import test_all
    test_all()

    from lib.run.VAR import test_all
    test_all()

    from lib.run.MEM import test_all
    test_all()

    from lib.calculator_logic.ADD import test_all
    test_all()

    from lib.execution_control.IF import test_all
    test_all()

    from lib.execution_control.BREAK import test_all
    test_all()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")

    