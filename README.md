# Sudoku Solver
## Summary
Sudoku solver... solves sudokus. It frames sudokus as a constraint satisfaction problem (CSP), then uses a mix of establishing arc consistency and backtracking to solve around 60 sudokus per second.

## Features
- Solves sudokus from an included database quickly and verifies their answers
- Solves custom sudokus through the command line

## How to use
1. Download/clone the repository
2. cd into the directory.
3. Either:
   - Run ```python main.py``` to solve problems from the database
   - Run ```python main.py --custom``` to enter a specific sudoku for the algorithm to solve

## Credit
Many of the algorithms used are based on those found in Artificial Intelligence: A Modern Approach 4th edition by Peter Norvig and Stuart J. Russell.

The provided database includes the first 100,000 entries from [Kyubyong Park's database on Kaggle](https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download).
