# This is a Turing machine with finite memory (a fixed length tape) and a plain python simulator for it
# The simulator is the reference that the graph coloring search is checked against
#
# Rules (the graph in TM_TO_GRAPH follows the exact same rules):
#   - The input is written from cell 0, the rest of the tape is blank and the head starts on cell 0
#   - Moving left off cell 0 or right off the last cell leaves the head where it is
#   - The accept and reject states halt, and so does any (state, symbol) pair with no transition
#   - A halted machine keeps the same configuration for the rest of the steps

from dataclasses import dataclass

LEFT = "L"
RIGHT = "R"
STAY = "S"
MOVES = (LEFT, RIGHT, STAY)

@dataclass(frozen=True)
class Configuration:
    state: str
    head: int
    tape: tuple

    def __str__(self):
        cells = [f"[{symbol}]" if i == self.head else f" {symbol} " for i, symbol in enumerate(self.tape)]
        return f"{self.state:>8} |{''.join(cells)}|"

class TuringMachine:
    def __init__(self, states: list, alphabet: list, transitions: dict, start: str, accept: str, reject: str = None, blank: str = "_", tape_length: int = 8):
        """ Declare a single tape Turing machine with a finite tape

        Args:
            states (list): Every state name
            alphabet (list): Every tape symbol, must include the blank
            transitions (dict): (state, symbol) -> (new state, symbol to write, move) where move is "L", "R" or "S"
            start (str): The start state
            accept (str): The accepting state, the machine accepts if it is in this state after the last step
            reject (str, optional): A rejecting state, it only halts the machine. Defaults to None.
            blank (str, optional): The blank symbol. Defaults to "_".
            tape_length (int, optional): The number of tape cells (the finite memory). Defaults to 8.
        """
        self.states = list(states)
        self.alphabet = list(alphabet)
        self.transitions = dict(transitions)
        self.start = start
        self.accept = accept
        self.reject = reject
        self.blank = blank
        self.tape_length = tape_length
        self.halting = {state for state in (accept, reject) if state is not None}
        self.validate()

    def validate(self):
        if len(set(self.states)) != len(self.states) or len(set(self.alphabet)) != len(self.alphabet):
            raise ValueError("States and symbols must be unique")
        if self.blank not in self.alphabet:
            raise ValueError(f"The blank symbol {self.blank!r} must be in the alphabet")
        for state in (self.start, *self.halting):
            if state not in self.states:
                raise ValueError(f"Unknown state {state!r}")
        if self.tape_length < 1:
            raise ValueError("The tape needs at least one cell")
        for (state, symbol), (new_state, write, move) in self.transitions.items():
            if state not in self.states or new_state not in self.states:
                raise ValueError(f"Unknown state in transition {(state, symbol)}")
            if symbol not in self.alphabet or write not in self.alphabet:
                raise ValueError(f"Unknown symbol in transition {(state, symbol)}")
            if move not in MOVES:
                raise ValueError(f"Move must be one of {MOVES}, got {move!r}")

    def step_rule(self, state: str, symbol: str):
        """ What the machine does in this state reading this symbol, halted machines stand still

        Returns:
            (str, str, str): (new state, symbol to write, move)
        """
        if state in self.halting or (state, symbol) not in self.transitions:
            return state, symbol, STAY
        return self.transitions[(state, symbol)]

    def initial_configuration(self, tape_input) -> Configuration:
        tape_input = list(tape_input)
        if len(tape_input) > self.tape_length:
            raise ValueError(f"Input of length {len(tape_input)} does not fit on a tape of length {self.tape_length}")
        for symbol in tape_input:
            if symbol not in self.alphabet:
                raise ValueError(f"Unknown input symbol {symbol!r}")
        tape = tuple(tape_input + [self.blank] * (self.tape_length - len(tape_input)))
        return Configuration(self.start, 0, tape)

    def step(self, config: Configuration) -> Configuration:
        new_state, write, move = self.step_rule(config.state, config.tape[config.head])
        tape = list(config.tape)
        tape[config.head] = write
        head = config.head
        if move == LEFT:
            head = max(head - 1, 0)
        elif move == RIGHT:
            head = min(head + 1, self.tape_length - 1)
        return Configuration(new_state, head, tuple(tape))

    def run(self, tape_input, max_steps: int):
        """ Run the machine for exactly max_steps steps

        Returns:
            (bool, list[Configuration]): (accepted, the max_steps + 1 configurations it went through)
        """
        trace = [self.initial_configuration(tape_input)]
        for _ in range(max_steps):
            trace.append(self.step(trace[-1]))
        return trace[-1].state == self.accept, trace

# Example machines used by the tests
def even_ones_machine(tape_length=6):
    """ Accepts binary strings with an even number of 1s """
    return TuringMachine(
        states=["even", "odd", "accept", "reject"],
        alphabet=["_", "0", "1"],
        transitions={
            ("even", "0"): ("even", "0", RIGHT),
            ("even", "1"): ("odd", "1", RIGHT),
            ("even", "_"): ("accept", "_", STAY),
            ("odd", "0"): ("odd", "0", RIGHT),
            ("odd", "1"): ("even", "1", RIGHT),
            ("odd", "_"): ("reject", "_", STAY),
        },
        start="even", accept="accept", reject="reject", tape_length=tape_length)

def increment_machine(tape_length=6):
    """ Adds 1 to a little endian binary number written after a "#" marker (cell 1 is the lowest bit)
        then walks back to the marker and accepts, so it uses both head directions and writes to the tape """
    return TuringMachine(
        states=["start", "carry", "back", "accept"],
        alphabet=["_", "#", "0", "1"],
        transitions={
            ("start", "#"): ("carry", "#", RIGHT),
            ("carry", "1"): ("carry", "0", RIGHT),
            ("carry", "0"): ("back", "1", LEFT),
            ("carry", "_"): ("back", "1", LEFT),
            ("back", "0"): ("back", "0", LEFT),
            ("back", "1"): ("back", "1", LEFT),
            ("back", "#"): ("accept", "#", STAY),
        },
        start="start", accept="accept", tape_length=tape_length)

def palindrome_machine(tape_length=5):
    """ Accepts binary palindromes by crossing off the outer symbols and going back and forth """
    return TuringMachine(
        states=["start", "have0", "have1", "check0", "check1", "return", "accept", "reject"],
        alphabet=["_", "0", "1"],
        transitions={
            ("start", "0"): ("have0", "_", RIGHT),
            ("start", "1"): ("have1", "_", RIGHT),
            ("start", "_"): ("accept", "_", STAY),
            ("have0", "0"): ("have0", "0", RIGHT),
            ("have0", "1"): ("have0", "1", RIGHT),
            ("have0", "_"): ("check0", "_", LEFT),
            ("have1", "0"): ("have1", "0", RIGHT),
            ("have1", "1"): ("have1", "1", RIGHT),
            ("have1", "_"): ("check1", "_", LEFT),
            ("check0", "0"): ("return", "_", LEFT),
            ("check0", "1"): ("reject", "1", STAY),
            ("check0", "_"): ("accept", "_", STAY),
            ("check1", "1"): ("return", "_", LEFT),
            ("check1", "0"): ("reject", "0", STAY),
            ("check1", "_"): ("accept", "_", STAY),
            ("return", "0"): ("return", "0", LEFT),
            ("return", "1"): ("return", "1", LEFT),
            ("return", "_"): ("start", "_", RIGHT),
        },
        start="start", accept="accept", reject="reject", tape_length=tape_length)

# Test functions
def test_even_ones():
    tm = even_ones_machine()
    assert tm.run("0110", 10)[0] is True
    assert tm.run("0100", 10)[0] is False
    assert tm.run("", 10)[0] is True

def test_increment():
    tm = increment_machine()
    accepted, trace = tm.run("#1101", 20)
    assert accepted is True
    assert trace[-1].tape == ("#", "0", "0", "1", "1", "_")
    assert trace[-1].head == 0
    assert tm.run("#111", 20)[-1][-1].tape == ("#", "0", "0", "0", "1", "_")   # carries into a blank cell
    assert tm.run("#1101", 5)[0] is False   # not enough steps to finish
    assert tm.run("0", 20)[0] is False      # no marker, so there is no transition and it halts

def test_palindrome():
    tm = palindrome_machine()
    for word in ["", "0", "1", "00", "11", "010", "0110", "1001"]:
        assert tm.run(word, 40)[0] is True, word
    for word in ["01", "10", "011", "0100", "1101"]:
        assert tm.run(word, 40)[0] is False, word

def test_halting_and_edges():
    tm = TuringMachine(states=["a", "acc"], alphabet=["_", "1"], transitions={("a", "_"): ("a", "1", LEFT)}, start="a", accept="acc", tape_length=2)
    accepted, trace = tm.run("", 3)
    # Moving left off cell 0 keeps the head on cell 0
    assert [config.head for config in trace] == [0, 0, 0, 0]
    # ("a", "1") has no transition so the machine halts and never accepts
    assert trace[-1] == trace[1]
    assert accepted is False

def test_validation():
    for bad in [
        dict(states=["a"], alphabet=["0"], transitions={}, start="a", accept="a"),                                # no blank
        dict(states=["a"], alphabet=["_"], transitions={("a", "_"): ("b", "_", RIGHT)}, start="a", accept="a"),   # unknown state
        dict(states=["a"], alphabet=["_"], transitions={("a", "_"): ("a", "_", "UP")}, start="a", accept="a"),    # bad move
    ]:
        try:
            TuringMachine(**bad)
            assert False, f"Should have rejected {bad}"
        except ValueError:
            pass
    try:
        even_ones_machine(tape_length=2).initial_configuration("010")
        assert False, "Input longer than the tape should be rejected"
    except ValueError:
        pass

def test_all():
    test_even_ones()
    test_increment()
    test_palindrome()
    test_halting_and_edges()
    test_validation()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")
