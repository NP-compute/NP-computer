# NP-Computer

The idea of this repo is to build a computer from graphs and to run it using a graph coloring algothim. The computer is designed to control if it is 3-colorable or not using a BREAK function, allowing the computer to return True (it is 3 colorable) or False (it is not 3 colorabl)

## Quick Start

### 1. Environment Setup

Create and activate a Python virtual environment:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Tests

Execute the comprehensive test suite:

```bash
# Run all tests via shell script
./test_all.sh

# Or run directly with Python
python3 -m lib.test_all
```

## Architecture

The system is organized into specialized modules, each with detailed documentation:

### Core Runtime (`lib/run/`)
Contains the fundamental computational engine:
- **NPComputer**: Main graph-based computation system
- **IS_COLORABLE**: 3-coloring algorithms with constraint propagation
- **MEM/VAR/CONST**: Memory abstractions and data types
- **FINALS**: Core constants and tri-state logic definitions

📖 [Detailed documentation](lib/run/README.md)

### Binary Logic (`lib/binary_logic/`)
Fundamental logic operations implemented through graph constraints:
- **NOT, SWAP, AND**: Core building blocks ⭐
- **NAND, OR, XOR, NOR, XNOR**: Derived operations
- All operations preserve 3-colorability when valid

📖 [Detailed documentation](lib/binary_logic/README.md)

### Execution Control (`lib/execution_control/`)
Advanced control flow without traditional branching:
- **BREAK**: Forces non-3-colorability to terminate invalid paths
- **IF**: Conditional execution through graph connectivity
- Enables the revolutionary "FIND" paradigm

📖 [Detailed documentation](lib/execution_control/README.md)

### Calculator Logic (`lib/calculator_logic/`)
Arithmetic operations:
- **ADD, SUB, MUL, DIV**: Basic arithmetic
- Built using binary logic primitives
- Performance characteristics vary due to NP-complete nature

### Turing Machine (`lib/turing_machine/`)
Finite memory Turing machines compiled into a graph coloring problem:
- **TM**: Declare a machine (states, alphabet, transitions, tape length) and run it in plain python
- **TM_TO_GRAPH**: Build the graph, it is 3-colorable only if the machine accepts within `max_steps`
- **RIGID_GATES**: AND / OR gates with exactly one valid coloring per input
- **ORDERED_SEARCH** (`lib/run/`): Colors the graph in the order the machine runs, so the search follows the machine step by step

📖 [Detailed documentation](lib/turing_machine/README.md)

## Usage Examples

### Basic Computation
```python
from lib.run.INIT import NPComputer
from lib.run.VAR import VAR
from lib.run.CONST import CONST
from lib.binary_logic.AND import AND
from lib.execution_control.BREAK import BREAK

# Create computer
computer = NPComputer()

# Create variables and constants
var_a = VAR(computer, n=4)    # 4-bit variable
const_5 = CONST(computer, value=5, n=4)  # Constant 5

# Perform logic operations
result = AND(computer, var_a.bits[0], const_5.bits[0])

# Check if computation is valid
is_valid = computer()  # Returns True if 3-colorable
```

### Testing
The test suite covers all components:
- Unit tests for each logic operation
- Integration tests for complex operations
- Graph colorability verification
- Performance benchmarks

### Contributing
When adding new operations:
1. Ensure 3-colorability is preserved for valid inputs
2. Add comprehensive test coverage
3. Document the constraint-based implementation
4. Consider performance implications

