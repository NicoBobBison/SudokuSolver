# Test puzzles from Kaggle: https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download

# EXTRA PUZZLES THAT CURRENTLY DON'T WORK (sometimes followed by their solution)
# 000102000060000070008000900400000003050007000200080001009000805070000060000304000

# 008030090000000423045100800050200030870600100060813900012746000089005710006000000
# 628437591197568423345192867951274638873659142264813975512746389489325716736981254

# 300400961006008700024017050090062018708050309040030000610040007005001030800500000
# 387425961156398742924617853593762418768154329241839675619243587475981236832576194

import numpy as np
import puzzle
import time
import argparse

parser = argparse.ArgumentParser(prog="SudokuSolver", description="A sudoku solver.")
parser.add_argument("--custom", action="store_true")
args = parser.parse_args()

if args.custom:
    user_input = input(
            "\nEnter a sudoku puzzle. Each number should be from 1-9, or 0 if the cell is empty.\n" +
              "Numbers should be inputted as one long string, with no spaces.\n" +
              "Enter values starting from the top left and moving left to right:\n")
    if len(user_input) != 81:
        print("Invalid input.")
        exit()
    start = time.time()
    p = puzzle.Puzzle([int(x) for x in list(user_input)])
    result = p.solve()
    result_str = ""
    for j in result:
        if len(j) == 1:
            result_str += str(j[0])
        else:
            result_str += str(j)
    print(f"Result: {result_str}")
    print(f"Finished in {round(1000 * (time.time() - start), 2)} ms")
    exit()

num = int(input("Enter the number of puzzles you want to solve (max 100000):"))

# Import code is from Kaggle dataset
quizzes = np.zeros((num, 81), np.int32)
solutions = np.zeros((num, 81), np.int32)
for i, line in enumerate(open('sudoku.csv', 'r').read().splitlines()[1:num+1]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s
quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))

print("Starting to solve...")
start = time.time()
errors = 0

for i, quiz in enumerate(quizzes):
    combined = []
    for r in quiz.tolist():
        combined += r
    p = puzzle.Puzzle(combined)
    result = p.solve()
    result_str = ""
    for j in result:
        if len(j) == 1:
            result_str += str(j[0])
        else:
            result_str += str(j)
    sol = "".join(str(x) for y in solutions[i].tolist() for x in y)
    if sol == result_str:
        print(f"{i+1}: Solved correctly.")
    else:
        print(f"{i+1}: Error")
        print(f"Problem          : {"".join(str(x) for y in quiz.tolist() for x in y)}")
        print(f"Intended solution: {sol}")
        found = ""
        print(f"Solution found   : {result_str}")
        errors += 1

total_time = time.time() - start
print(f"Finished solving {num} sudokus in {round(total_time, 2)} seconds")
print(f"Average rate: {round(num / total_time, 2)} sudokus per second")
print(f"Average time for one sudoku: {round(1000 * total_time / num, 2)} ms")
print(f"Errors: {errors}")