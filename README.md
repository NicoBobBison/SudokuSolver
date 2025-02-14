# Sudoku Solver
## Summary
Sudoku Solver solves sudokus either from the included database or from a custom user input. It frames sudokus as a constraint satisfaction problem (CSP), then uses a mix of establishing arc consistency and backtracking to solve around **350 sudokus per second**.

## Features
- Solves sudokus from an included database quickly and verifies their answers
- Solves custom sudokus through the command line
- Prints helpful statistics about solve speed

## Limitations
Some sudokus (like the one at the top of ```main.py```) are too complex and take too long to run. This might be fixed in the future by improving the backtracking algorithm.

## How to use
1. Download/clone the repository
2. cd into the directory.
3. Run ```python main.py``` to solve problems from the database, or use the command line arguments below.

### Command line arguments
```--help```: Shows command line arguments.

```--custom```: Prompts you to enter a specific sudoku for the algorithm to solve.

```--debug```: Prints helpful debug messages (note: this may slow down the algorithm when mass-solving problems in the database).

## Credit
Many of the algorithms used are based on those found in Artificial Intelligence: A Modern Approach 4th edition by Peter Norvig and Stuart J. Russell.

The provided database includes the first 100,000 entries from [Kyubyong Park's database on Kaggle](https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download).
