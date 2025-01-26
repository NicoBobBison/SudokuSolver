# Test puzzles from Kaggle: https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download
import numpy as np

num = int(input("Enter the number of puzzles you want to solve (max 1000000):"))

quizzes = np.zeros((num, 81), np.int32)
solutions = np.zeros((num, 81), np.int32)
for i, line in enumerate(open('sudoku.csv', 'r').read(num * (81 * 2 + 1)).splitlines()[1:]):
    quiz, solution = line.split(",")
    for j, q_s in enumerate(zip(quiz, solution)):
        q, s = q_s
        quizzes[i, j] = q
        solutions[i, j] = s
quizzes = quizzes.reshape((-1, 9, 9))
solutions = solutions.reshape((-1, 9, 9))
