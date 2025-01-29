import numpy as np
import queue
import copy

# Coordinates start with 0 at top left, then move right and wrap around. Bottom right is 80.
class Puzzle:
    def __init__(self, rows):
        self.domains = []
        # Indeces of incomplete values
        self.incomplete = []
        combined = []
        for r in rows:
            combined += r
        for i, val in enumerate(combined):
            if val == 0:
                self.incomplete.append(i)
                self.domains.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                self.domains.append([val])

    def solve(self):
        q = queue.Queue()
        for group in self.__get_all_rows() + self.__get_all_columns() + self.__get_all_boxes():
            for pair in self.__alldiff(group):
                q.put(pair)
        self.ac3(q)
        if len(self.incomplete) > 0:
            assignment = self.__backtracking_search()
            # print(f"Assignment: {assignment}")
            for a in assignment:
                self.domains[a[0]] = [a[1]]
        # print(len(self.incomplete))
        return self.domains

    # Takes in a queue with every initial pair to check
    # Returns false if an inconsistency is detected, true otherwise
    def ac3(self, queue):
        while not queue.empty():
            popped = queue.get()
            if len(self.domains[popped[0]]) == 0 or len(self.domains[popped[1]]) == 0:
                return False
            # print(f"Popped: {popped}")
            if self.__revise(popped[0], popped[1]):
                for neighbor in self.__get_neighbors(popped[0]):
                    queue.put(neighbor)
        return True
    
    def __revise(self, x, y):
        xval = self.domains[x][0]
        yval = self.domains[y][0]
        if len(self.domains[x]) == 1 and xval in self.domains[y]:
            self.domains[y].remove(xval)
            if len(self.domains[y]) == 1:
                # print(f"Incomplete before: {self.incomplete}")
                # print(f"Remove: {y}")
                self.incomplete.remove(y)
                # print(f"Incomplete after: {self.incomplete}")
            return True
        if len(self.domains[y]) == 1 and yval in self.domains[x]:
            self.domains[x].remove(yval)
            if len(self.domains[x]) == 1:
                # print(f"Incomplete before: {self.incomplete}")
                # print(f"Remove: {x}")
                self.incomplete.remove(x)
                # print(f"Incomplete after: {self.incomplete}")
            return True
        return False
    
    def __backtracking_search(self):
        # print(f"Initial: {self.domains}")
        return self.__backtrack([])
        
    # Recursive call
    def __backtrack(self, assignment: list):
        def len_of_array_from_index(i):
            return len(self.domains[i])
        
        # print(f"Assignment: {assignment}")
        if len(self.incomplete) == 0:
            # print(f"Complete assignment: {assignment}")
            return assignment
        
        self.incomplete.sort(key=len_of_array_from_index)
        # print(f"Incomplete: {self.incomplete}")
        # print(f"Domains: {self.domains}")
        index = self.incomplete.pop(0)
        neighbors = self.__get_neighbors(index)
        # TODO: Order domain values?
        for val in self.domains[index]:
            assignment.append((index, val))
            q = queue.Queue()
            for n in neighbors:
                q.put(n)
            puzzle_copy = copy.deepcopy(self)
            puzzle_copy.domains[index] = [val]
            init_incomplete = puzzle_copy.incomplete.copy()
            if puzzle_copy.ac3(q):
                # Check if performing ac3 solved some cells
                for i in init_incomplete:
                    if i not in puzzle_copy.incomplete:
                        assignment.append((i, puzzle_copy.domains[i][0]))
                result = puzzle_copy.__backtrack(assignment)
                if result != None:
                    return result
            assignment.remove((index, val))
        self.incomplete.append(index)
        return None

    # Converts a list of 9 values to a tuple with every possible binary constraint between them
    def __alldiff(self, group):
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
        results = []
        # Same row
        for i in range(coord - (coord % 9), coord - (coord % 9) + 9):
            if i != coord:
                results.append((coord, i))
                #Same column
        for i in range(coord % 9, 81, 9):
            if i != coord:
                results.append((coord, i))
        # Same box
        # Wizard magic to get the top left tile of the current box
        start = coord - (coord % 3) - (9 * ((coord // 9) % 3))
        for r in range(start, start + 27, 9):
            for c in range(3):
                if r + c != coord:
                    results.append((coord, r + c))
        return results
    