# This converts a finite memory Turing machine into a graph coloring problem
# The graph is 3 colorable if and only if the machine is in its accept state after max_steps steps
#
# Every step t of the run gets its own copy of the machine:
#   state[t][q]     1 if the machine is in state q
#   head[t][i]      1 if the head is on cell i
#   cells[t][i][s]  1 if cell i holds symbol s
# Step t + 1 is wired from step t in the order the machine runs, and the nodes are created in that order so the
# ordered search (lib/run/ORDERED_SEARCH.py) colors the graph the same way the machine would run:
#   1. READ   every cell is connected to the head: read[s] = OR over i of (head[i] AND cells[i][s])
#   2. DECIDE fire[q, s] = state[q] AND read[s], then the new state, the symbol to write and the move are ORs of the fires
#   3. MOVE   the search walks the tape left to right asking "is the head here?" (it tries ONE first on head[t + 1][i])
#             every cell the head did not move to rejects ONE, so the search fails there and moves on to the cell on the right
#   4. WRITE  cells[t + 1][i][s] = (head[i] AND write[s]) OR (NOT head[i] AND cells[i][s])
# At the end BREAK is used if the machine is not in the accept state, so the coloring is only valid when the machine accepts
#
# All the gates are rigid (see RIGID_GATES.py) so the search never has to guess, a rejecting run fails at the BREAK and
# unwinds straight back to the start without retrying anything

from lib.run.INIT import NPComputer
from lib.run.FINALS import TriBit
from lib.run.ORDERED_SEARCH import ordered_search, ASSIGN, REJECT, TRI_BIT_TO_COLOR
from lib.execution_control.BREAK import BREAK
from lib.binary_logic.NOT import NOT
from lib.turing_machine.RIGID_GATES import RIGID_AND, RIGID_OR, RIGID_OR_MANY, RIGID_TRUE, RIGID_FALSE
from lib.turing_machine.TM import TuringMachine, Configuration, LEFT, RIGHT, STAY

ONE_COLOR = TRI_BIT_TO_COLOR[TriBit.ONE]

class TM_TO_GRAPH:
    def __init__(self, tm: TuringMachine, tape_input, max_steps: int, computer: NPComputer = None):
        """ Build the graph for running tm on tape_input for max_steps steps

        Args:
            tm (TuringMachine): The machine to convert
            tape_input (str | list): The input written from cell 0
            max_steps (int): How many steps to run, the machine has to accept within this many steps
            computer (NPComputer, optional): The computer to build in (pass one with solve=False to export DIMACS). Defaults to a new one.
        """
        self.tm = tm
        self.tape_input = tape_input
        self.max_steps = max_steps
        self.computer = computer or NPComputer()

        # steps[t] = {"state": {q: node}, "head": [node per cell], "cells": [{symbol: node} per cell]}
        self.steps = [self.build_initial(tm.initial_configuration(tape_input))]
        for _ in range(max_steps):
            self.steps.append(self.build_step(self.steps[-1]))

        # The machine has to be in the accept state at the end, otherwise BREAK the graph
        self.accept_node = self.steps[-1]["state"][tm.accept]
        BREAK(self.computer, NOT(self.computer, self.accept_node))

    def build_initial(self, config: Configuration) -> dict:
        """ The first configuration is all constants """
        tm = self.tm
        bit = lambda value: RIGID_TRUE(self.computer) if value else RIGID_FALSE(self.computer)
        return {
            "state": {q: bit(q == config.state) for q in tm.states},
            "head": [bit(i == config.head) for i in range(tm.tape_length)],
            "cells": [{s: bit(s == config.tape[i]) for s in tm.alphabet} for i in range(tm.tape_length)],
        }

    def build_step(self, prev: dict) -> dict:
        """ Wire up the configuration after one more step of the machine """
        tm, computer = self.tm, self.computer
        L = tm.tape_length

        # 1. READ: the head is connected to every cell, only the cell under the head gets through
        read = {s: RIGID_OR_MANY(computer, [RIGID_AND(computer, prev["head"][i], prev["cells"][i][s]) for i in range(L)]) for s in tm.alphabet}

        # 2. DECIDE: exactly one (state, symbol) pair fires
        new_state_inputs = {q: [] for q in tm.states}
        write_inputs = {s: [] for s in tm.alphabet}
        move_inputs = {move: [] for move in (LEFT, RIGHT, STAY)}
        for q in tm.states:
            for s in tm.alphabet:
                fire = RIGID_AND(computer, prev["state"][q], read[s])
                new_q, write, move = tm.step_rule(q, s)
                new_state_inputs[new_q].append(fire)
                write_inputs[write].append(fire)
                move_inputs[move].append(fire)
        state = {q: RIGID_OR_MANY(computer, new_state_inputs[q]) for q in tm.states}
        write = {s: RIGID_OR_MANY(computer, write_inputs[s]) for s in tm.alphabet}
        move = {m: RIGID_OR_MANY(computer, move_inputs[m]) for m in move_inputs}

        # Moving off either end of the tape leaves the head where it is
        stay_at = []
        for i in range(L):
            stays = [move[STAY]] + ([move[LEFT]] if i == 0 else []) + ([move[RIGHT]] if i == L - 1 else [])
            stay_at.append(RIGID_OR_MANY(computer, stays))

        # 3. MOVE: built cell by cell from the left, so the search probes each cell for the head in turn
        head = []
        for i in range(L):
            arrive = [RIGID_AND(computer, prev["head"][i], stay_at[i])]
            if i > 0:
                arrive.append(RIGID_AND(computer, prev["head"][i - 1], move[RIGHT]))
            if i < L - 1:
                arrive.append(RIGID_AND(computer, prev["head"][i + 1], move[LEFT]))
            # The head node is a copy of the OR (through two NOTs), so it hangs off one already colored node
            # That way the search asks "is the head here?" exactly once per cell, even if the OR gate had to retry inside
            head.append(NOT(computer, NOT(computer, RIGID_OR_MANY(computer, arrive))))

        # 4. WRITE: the cell under the old head takes the written symbol, every other cell keeps its symbol
        cells = []
        for i in range(L):
            away = NOT(computer, prev["head"][i])
            cells.append({s: RIGID_OR(computer, RIGID_AND(computer, prev["head"][i], write[s]), RIGID_AND(computer, away, prev["cells"][i][s])) for s in tm.alphabet})

        return {"state": state, "head": head, "cells": cells}

    def config_nodes(self, t: int) -> list[int]:
        step = self.steps[t]
        return list(step["state"].values()) + step["head"] + [node for cell in step["cells"] for node in cell.values()]

    def decode(self, coloring: dict, t: int) -> Configuration:
        """ Read the configuration at step t back out of a coloring """
        step = self.steps[t]
        is_one = lambda node: coloring[node] == ONE_COLOR
        states = [q for q, node in step["state"].items() if is_one(node)]
        heads = [i for i, node in enumerate(step["head"]) if is_one(node)]
        tape = []
        for cell in step["cells"]:
            symbols = [s for s, node in cell.items() if is_one(node)]
            if len(symbols) != 1:
                raise ValueError(f"Step {t} has a cell holding {symbols}")
            tape.append(symbols[0])
        if len(states) != 1 or len(heads) != 1:
            raise ValueError(f"Step {t} has states {states} and heads {heads}")
        return Configuration(states[0], heads[0], tuple(tape))

    def search_order(self) -> list[int]:
        """ The nodes in the order the machine runs, which is the order they were built in """
        return sorted(self.computer.graph.nodes())

    def solve(self):
        """ Run the ordered search and record what it did

        Returns:
            (bool, dict, SearchRecorder): (the machine accepts, the coloring, what the search did)
        """
        recorder = SearchRecorder(self)
        result, coloring = ordered_search(self.computer.graph, order=self.search_order(), listener=recorder)
        return result, coloring, recorder

    def __call__(self) -> bool:
        """ True if the graph is 3 colorable, which means the machine accepts """
        return self.solve()[0]

class SearchRecorder:
    """ Listens to the ordered search and writes down the machine run it is following """

    def __init__(self, tm_graph: TM_TO_GRAPH):
        self.tm_graph = tm_graph
        self.colors = {}
        # The configuration at step t is known once its last node has been colored
        self.last_node = {max(tm_graph.config_nodes(t)): t for t in range(len(tm_graph.steps))}
        self.head_node = {node: (t, i) for t, step in enumerate(tm_graph.steps) for i, node in enumerate(step["head"])}
        self.trace = []           # [Configuration] in the order the search finished them
        self.head_probes = {}     # t -> [(cell, True if the head is there)] in the order the search asked
        self.events = 0
        self.backtracks = 0

    def __call__(self, event, node, color, index):
        self.events += 1
        if event == ASSIGN:
            self.colors[node] = color
        elif event != REJECT:
            self.backtracks += 1

        # Asking "is the head on this cell?" is the search trying ONE on a head node
        if node in self.head_node and color == ONE_COLOR and event in (ASSIGN, REJECT):
            t, i = self.head_node[node]
            self.head_probes.setdefault(t, []).append((i, event == ASSIGN))

        if event == ASSIGN and node in self.last_node:
            t = self.last_node[node]
            self.trace.append(self.tm_graph.decode(self.colors, t))

# Test functions
from lib.turing_machine.TM import even_ones_machine, increment_machine, palindrome_machine

def is_proper_coloring(graph, coloring):
    return all(coloring[u] != coloring[v] for u, v in graph.edges())

def check_search_follows_machine(tm: TuringMachine, tape_input, max_steps: int):
    """ The search has to accept exactly when the machine does, and walk through the same configurations """
    accepted, trace = tm.run(tape_input, max_steps)
    tm_graph = TM_TO_GRAPH(tm, tape_input, max_steps)
    result, coloring, recorder = tm_graph.solve()

    assert result is accepted, f"{tape_input!r}: machine accepted={accepted} but the graph colorable={result}"

    # The search finishes the configurations in the same order the machine runs, and they match step for step
    assert recorder.trace == trace, f"{tape_input!r}: the search did not follow the machine"

    # Each step the search probes the head from the left and the only cell that takes ONE is where the machine moved
    for t in range(1, max_steps + 1):
        probes = recorder.head_probes[t]
        assert [cell for cell, _ in probes] == list(range(tm.tape_length)), f"step {t}: probes {probes}"
        assert [cell for cell, here in probes if here] == [trace[t].head], f"step {t}: probes {probes}"

    # The only real backtracking is unwinding after the BREAK on a rejecting run, so the work is linear in the graph
    nodes = len(tm_graph.computer.graph.nodes())
    assert recorder.events < 6 * nodes, f"{recorder.events} search events for {nodes} nodes"

    if result:
        assert is_proper_coloring(tm_graph.computer.graph, coloring)
        assert [tm_graph.decode(coloring, t) for t in range(max_steps + 1)] == trace
        assert coloring[tm_graph.accept_node] == ONE_COLOR
    else:
        assert coloring == {}
    return result

def test_even_ones_graph():
    tm = even_ones_machine(tape_length=5)
    for word in ["", "0", "1", "11", "101", "0110", "1011"]:
        assert check_search_follows_machine(tm, word, 6) == (word.count("1") % 2 == 0), word

def test_increment_graph():
    tm = increment_machine(tape_length=5)
    assert check_search_follows_machine(tm, "#101", 8) is True
    assert check_search_follows_machine(tm, "#11", 8) is True
    # Not enough steps to walk back to the marker
    assert check_search_follows_machine(tm, "#111", 4) is False
    # No marker so the machine halts straight away
    assert check_search_follows_machine(tm, "1", 3) is False

def test_palindrome_graph():
    tm = palindrome_machine(tape_length=4)
    for word, expected in [("", True), ("0", True), ("11", True), ("010", True), ("01", False), ("011", False), ("110", False)]:
        assert check_search_follows_machine(tm, word, 16) is expected, word

def test_head_walks_both_ways():
    """ The increment machine moves right then left, the probes have to follow it both ways """
    tm = increment_machine(tape_length=5)
    accepted, trace = tm.run("#11", 8)
    heads = [config.head for config in trace]
    assert heads == [0, 1, 2, 3, 2, 1, 0, 0, 0]
    tm_graph = TM_TO_GRAPH(tm, "#11", 8)
    _, _, recorder = tm_graph.solve()
    assert [next(cell for cell, here in recorder.head_probes[t] if here) for t in range(1, 9)] == heads[1:]

def test_dimacs_export():
    """ The machine can be built in an exporting computer and written out as DIMACS """
    tm = even_ones_machine(tape_length=3)
    tm_graph = TM_TO_GRAPH(tm, "11", 3, computer=NPComputer(solve=False))
    dimacs = tm_graph.computer()
    header = [line for line in dimacs.splitlines() if line.startswith("p ")][0]
    assert header == f"p edge {len(tm_graph.computer.graph.nodes())} {len(tm_graph.computer.graph.edges())}"

def test_all():
    test_even_ones_graph()
    test_increment_graph()
    test_palindrome_graph()
    test_head_walks_both_ways()
    test_dimacs_export()

if __name__ == "__main__":
    test_all()
    print("All tests passed!")
