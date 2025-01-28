# Test puzzles from Kaggle: https://www.kaggle.com/datasets/bryanpark/sudoku?resource=download
import numpy as np
import puzzle

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

for i, quiz in enumerate(quizzes):
    p = puzzle.Puzzle(quiz.tolist())
    result = p.solve()
    result_str = ""
    for j in result:
        if len(j) == 1:
            result_str += str(j[0])
        else:
            result_str += str(j)
    sol = "".join(str(x) for y in solutions[i].tolist() for x in y)
    if sol == result_str:
        print("Solved correctly.")
    else:
        print("Error:")
        print(f"Problem          : {"".join(str(x) for y in quiz.tolist() for x in y)}")
        print(f"Intended solution: {sol}")
        found = ""
        print(f"Solution found   : {result_str}")
