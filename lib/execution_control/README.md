# lib/execution_control

This directory contains execution control mechanisms for the NP-Computer system, enabling conditional execution and search capabilities through graph coloring constraints.

## Files

### BREAK.py
The core functionality that enables the "FIND" paradigm:
- **Purpose**: Forces the graph to become non-3-colorable when a condition is met
- **Mechanism**: Connects an input node to a node that must be 1, creating a constraint conflict when input is 1
- **Use case**: Replaces traditional loops by allowing mass searching of configurations
- **Key insight**: Demonstrates why the 3-coloring problem cannot be solved in polynomial time

```python
# If input is 1, graph becomes non-3-colorable (breaks execution)
# If input is 0, graph remains 3-colorable (continues execution)
BREAK(computer, condition_node)
```

### IF.py
Conditional execution control for the NP-Computer:
- **Purpose**: Implements conditional logic without traditional branching
- **Mechanism**: Creates input/output gates that control data flow based on a toggle condition (see picture below)
- **Input blocking**: Prevents BREAK logic from propagating when condition is false
- **Output blocking**: Acts as if the computation never executed when condition is false
- **Implementation**: Uses complex SWAP and NOT operations with tri-state logic

![This image shows how to allow input through and deny input](./TriBitOpenCloseGate.png.png)

```python
# Returns output nodes that mirror input nodes when toggle is 1,
# or are isolated when toggle is 0
output_nodes = generate_IF_layer(computer, input_nodes, toggle_node)
```

## Architecture Concepts

### FIND Paradigm
The execution control system enables a revolutionary "FIND" approach:
1. Generate a VAR with unconstrained values (can represent any value 0 ≤ value < 2^n)
2. Build logic that conditionally calls BREAK based on search criteria
3. The system automatically searches all possible configurations
4. Only valid solutions maintain 3-colorability

### Hardware-Like Execution
Unlike software with branching, this system works like hardware:
- No traditional if/else statements that change execution flow
- All paths are computed simultaneously through graph constraints
- Conditions control which paths remain valid (3-colorable)

### Constraint Propagation
- **Valid path**: Graph remains 3-colorable, solution is possible
- **Invalid path**: BREAK is triggered, graph becomes non-3-colorable
- **Result**: Only configurations satisfying all constraints produce valid colorings

## Usage Examples

### Basic BREAK Usage
```python
from lib.execution_control.BREAK import BREAK
from lib.run.VAR import VAR

computer = NPComputer()
search_var = VAR(computer, n=8)  # Can be any 8-bit value

# Build logic to test if search_var equals target value
condition = build_equality_test(search_var, target_value)

# Break if condition is NOT met (continue only if equal)
BREAK(computer, NOT(computer, condition))

# Only solutions where search_var == target_value remain valid
```

### Conditional Execution with IF
```python
from lib.execution_control.IF import generate_IF_layer

computer = NPComputer()
data_nodes = [var1.bits[0], var2.bits[0]]  # Input data
condition = some_test_result  # 1 = execute, 0 = skip

# Only process data when condition is true
processed_data = generate_IF_layer(computer, data_nodes, condition)
```

## Theoretical Significance

This execution control system demonstrates:
1. **NP-completeness**: The ability to encode search problems as 3-coloring problems
2. **Polynomial reduction**: Traditional loops are replaced by constraint satisfaction
3. **Non-deterministic computation**: All possibilities are explored simultaneously
4. **Constraint satisfaction**: Solutions emerge from graph colorability rather than explicit computation