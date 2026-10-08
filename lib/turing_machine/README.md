# lib/turing_machine

This directory turns a Turing machine with finite memory (a fixed length tape) into a graph coloring problem.
The graph is 3-colorable if and only if the machine is in its accept state after `max_steps` steps, and the
ordered search colors the graph in the same order the machine runs, so you can watch the search follow the machine.

## Files

### TM.py
Declares a machine and runs it in plain python (this is the reference the graph is tested against):

```python
from lib.turing_machine.TM import TuringMachine, LEFT, RIGHT, STAY

tm = TuringMachine(
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
    start="even", accept="accept", reject="reject", tape_length=6)

accepted, trace = tm.run("0110", max_steps=10)
```

Rules (the graph follows the same ones):
- The input is written from cell 0, the rest of the tape is blank and the head starts on cell 0
- Moving off either end of the tape leaves the head where it is
- The accept and reject states halt, and so does any (state, symbol) pair with no transition
- A halted machine keeps the same configuration for the rest of the steps, so "accepts within `max_steps`" is the same as "is in the accept state at step `max_steps`"

### TM_TO_GRAPH.py
Builds the graph. Every step `t` gets one-hot 0/1 nodes for the state, the head position and the symbol in every cell.
Step `t + 1` is wired from step `t` in the order the machine runs:

1. **READ**: every cell is connected to the head, `read[s] = OR_i (head[i] AND cell[i][s])`, so only the cell under the head gets through
2. **DECIDE**: `fire[q, s] = state[q] AND read[s]`, then the new state, the symbol to write and the move are ORs of the fires
3. **MOVE**: the head nodes are built from cell 0 to the right. The search tries ONE first on each one, asking "is the head here?".
   Every cell the head did not move to rejects ONE, so the search fails there and moves on to the cell on the right until one accepts
4. **WRITE**: `cell'[i][s] = (head[i] AND write[s]) OR (NOT head[i] AND cell[i][s])`

At the end `BREAK(NOT(state[max_steps][accept]))` makes the graph impossible to color unless the machine accepted.

```python
from lib.turing_machine.TM_TO_GRAPH import TM_TO_GRAPH

tm_graph = TM_TO_GRAPH(tm, "0110", max_steps=10)
tm_graph()                                   # True, the graph is 3-colorable so the machine accepts

result, coloring, recorder = tm_graph.solve()
recorder.trace                               # the configurations, in the order the search finished them
recorder.head_probes[3]                      # [(cell, head is here?), ...] for step 3, left to right
tm_graph.decode(coloring, 3)                 # read the configuration at step 3 back out of the coloring
```

To export the graph instead, build it in a computer that doesn't solve: `TM_TO_GRAPH(tm, "0110", 10, computer=NPComputer(solve=False)).computer()`

### RIGID_GATES.py
AND / OR gates where every node has exactly one valid color once the inputs are colored (4 nodes each).
The gates in `lib/binary_logic` work for "is it 3-colorable", but some of their inner nodes can take more than one color.
A backtracking search that hits the BREAK at the end would retry every one of those choices, which is exponential.
With rigid gates a rejecting run unwinds straight back to the start, so the search stays linear in the size of the graph.
The tests brute force every coloring of each gate to check this.

### ../run/ORDERED_SEARCH.py
An iterative backtracking search that colors nodes in a given order (the TM graph uses build order), tries ONE first,
and reports every assign / reject / backtrack to a listener. It skips the O(n^4) clique check in `IS_COLORABLE`,
which is far too slow for these graphs (thousands of nodes).

## Tests

`check_search_follows_machine` in `TM_TO_GRAPH.py` checks, for several machines and inputs, that:
- the graph is 3-colorable exactly when `tm.run` accepts
- the configurations the search finishes, in order, are exactly the machine's trace
- on every step the search probes the head from cell 0 rightwards and only the machine's head cell takes ONE
- the search does linear work (no exponential backtracking), and an accepting coloring is a proper coloring that decodes to the trace

```bash
python3 -m lib.turing_machine.TM_TO_GRAPH
```
