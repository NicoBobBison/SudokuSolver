import numpy as np
import copy
from collections import defaultdict
from collections import deque

# Coordinates start with 0 at top left, then move right and wrap around. Bottom right is 80.
class Puzzle:
    def __init__(self, rows):
        self.domains = []
        self.constraints = defaultdict(list)
        # Indeces of incomplete values
        self.incomplete = set()
        for i, val in enumerate(rows):
            if val == 0:
                self.incomplete.add(i)
                self.domains.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                self.domains.append([val])

    def solve(self):
        q = deque()
        for group in self.__get_all_rows() + self.__get_all_columns() + self.__get_all_boxes():
            for pair in self.__alldiff_getpairs(group):
                q.append(pair)
                q.append((pair[1], pair[0]))
                self.constraints[pair[0]].append(pair[1])
                self.constraints[pair[1]].append(pair[0])

        if not self.ac3(q):
            print("Inconsistency detected.")
            return None
        
        # print(self.domains)
        if len(self.incomplete) > 0:
            print("Not fully solved with AC-3")
            print(self.domains)
            assignment = self.backtracking_search()
            # print(f"Assignment: {assignment}")
            if assignment == None:
                return None
            for a in assignment:
                self.domains[a[0]] = [a[1]]
        # print(len(self.incomplete))
        return self.domains

    # Takes in a queue with every initial pair to check
    # Returns false if an inconsistency is detected, true otherwise
    def ac3(self, queue):
        while len(queue) > 0:
            popped = queue.popleft()
            # print(f"Popped: {popped}")
            if self.__revise(popped[0], popped[1]):
                if len(self.domains[popped[0]]) == 0:
                    # print("AC3 fail")
                    return False
                for neighbor in self.__get_neighbors(popped[0]):
                    if neighbor[1] == popped[1] or neighbor[1] not in self.incomplete:
                        continue
                    queue.append((neighbor[1], neighbor[0]))
        return True
    
    def __revise(self, x, y):
        revised = False
        if len(self.domains[y]) == 1:
            to_remove = None
            for i, val in enumerate(self.domains[x]):
                if val == self.domains[y][0]:
                    to_remove = val
                    break
            if to_remove is not None:
                self.domains[x].remove(to_remove)
                revised = True
            if len(self.domains[x]) == 1 and x in self.incomplete:
                self.incomplete.remove(x)
        return revised
    
    def backtracking_search(self):
        # print(f"Initial: {self.domains}")
        return self.backtrack([])
        
    # Recursive call
    def backtrack(self, assignment: list):
        def least_constraining_value(i):
            # A list containing all possible values among incomplete domains
            # Ex: if domains are [1, 2] and [1, 3], this would be [1, 1, 2, 3]
            possible_incomplete = []
            for j in self.incomplete:
                possible_incomplete += self.domains[j]
            return possible_incomplete.count(i)

        # print(f"Assignment: {assignment}")
        if len(self.incomplete) == 0:
            q = deque()
            for group in self.__get_all_rows() + self.__get_all_columns() + self.__get_all_boxes():
                for pair in self.__alldiff_getpairs(group):
                    q.append(pair)
            if(self.ac3(q)):
                # print(f"Complete assignment: {assignment}")
                return assignment
            else:
                return None
        
        incomplete_list = list(self.incomplete)

        incomplete_list.sort(key=self.len_domains)
        # print(f"Incomplete: {self.incomplete}")
        # print(f"Domains: {self.domains}")
        index = incomplete_list.pop(0)
        neighbors = self.__get_neighbors(index)
        # TODO: Order domain values?
        for val in sorted(self.domains[index], key=least_constraining_value):
            assignment.append((index, val))
            # print(f"Assigning {(index, val)}")
            q = deque()
            for n in neighbors:
                q.append(n)
            puzzle_copy = copy.deepcopy(self)
            puzzle_copy.domains[index] = [val]
            init_incomplete = list(copy.deepcopy(puzzle_copy.incomplete))
            # print("Running AC3")
            if puzzle_copy.ac3(q):
                # Check if performing ac3 solved some cells
                for i in init_incomplete:
                    if i not in puzzle_copy.incomplete and len(puzzle_copy.domains[i]) == 1:
                        # print(f"Assignment from AC-3: {(i, puzzle_copy.domains[i][0])}")
                        assignment.append((i, puzzle_copy.domains[i][0]))
                result = puzzle_copy.backtrack(assignment)
                if result != None:
                    return result
            # print(f"Unassign: {(index, val)}")
            assignment.remove((index, val))
        incomplete_list.append(index)
        return None

    # Converts a list of 9 values to a tuple with every possible binary constraint between them
    def __alldiff_getpairs(self, group):
        result = []
        for i in range(len(group)):
            for j in range(i + 1, len(group)):
                result.append((group[i], group[j]))
        return result
    
    def __get_all_rows(self):
        result = []
        for i in range(9):
            result.append([])
            for j in range(9):
                result[i].append(i * 9 + j)
        return result

    def __get_all_columns(self):
        result = []
        for i in range(9):
            result.append([])
            count = i
            while count < 81:
                result[i].append(count)
                count += 9
        return result
    
    def __get_all_boxes(self):
        result = []
        for start_row in range(3):
            for start_col in range(3):
                result.append([])
                for row in range(start_row * 3, (start_row + 1) * 3):
                    for col in range(start_col * 3, (start_col + 1) * 3):
                        result[start_row * 3 + start_col].append(row * 9 + col)
        return result

    def __get_neighbors(self, coord: int):
        return [(coord, x) for x in self.constraints[coord]]
    
    def len_domains(self, i):
        return len(self.domains[i])