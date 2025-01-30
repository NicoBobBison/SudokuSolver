import numpy as np
import queue
import copy

# Coordinates start with 0 at top left, then move right and wrap around. Bottom right is 80.
class Puzzle:
    def __init__(self, rows):
        self.domains = []
        # Indeces of incomplete values
        self.incomplete = []
        for i, val in enumerate(rows):
            if val == 0:
                self.incomplete.append(i)
                self.domains.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                self.domains.append([val])

    def solve(self):
        q = queue.Queue()
        for group in self.__get_all_rows() + self.__get_all_columns() + self.__get_all_boxes():
            q.put(group)
        while not q.empty():
            popped = q.get()
            # print(f"Popped: {popped}")
            updated = self.__alldiff_updatevals(popped)
            # print(f"Updated: {updated}")
            if len(updated) > 0:
                for u in updated:
                    for neighbor in self.__get_neighbor_groups(u):
                        q.put(neighbor)
        # print(self.domains)
        if len(self.incomplete) > 0:
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
        while not queue.empty():
            popped = queue.get()
            if len(self.domains[popped[0]]) == 0 or len(self.domains[popped[1]]) == 0:
                # print("AC3 fail")
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
            q = queue.Queue()
            for group in self.__get_all_rows() + self.__get_all_columns() + self.__get_all_boxes():
                for pair in self.__alldiff_getpairs(group):
                    q.put(pair)
            if(self.ac3(q)):
                # print(f"Complete assignment: {assignment}")
                return assignment
            else:
                return None
        
        self.incomplete.sort(key=self.len_domains)
        # print(f"Incomplete: {self.incomplete}")
        # print(f"Domains: {self.domains}")
        index = self.incomplete.pop(0)
        neighbors = self.__get_neighbors(index)
        # TODO: Order domain values?
        for val in sorted(self.domains[index], key=least_constraining_value):
            assignment.append((index, val))
            # print(f"Assigning {(index, val)}")
            q = queue.Queue()
            for n in neighbors:
                q.put(n)
            puzzle_copy = copy.deepcopy(self)
            puzzle_copy.domains[index] = [val]
            init_incomplete = copy.deepcopy(puzzle_copy.incomplete)
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
        self.incomplete.append(index)
        return None

    # Updates a group's corresponding domains based on alldiff restriction
    # Returns a list of changed indeces
    def __alldiff_updatevals(self, group):
        group.sort(key=self.len_domains)
        changed = []
        if len(self.domains[group[0]]) > 1:
            return changed
        for i, group_val in enumerate(group):
            if len(self.domains[group_val]) == 1:
                val = self.domains[group_val][0]
                for j in range(i + 1, len(group)):
                    if val in self.domains[group[j]]:
                        self.domains[group[j]].remove(val)
                        changed.append(group[j])
        return changed

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

    def __get_neighbor_groups(self, coord: int):
        results = [[], [], []]
        # Same row
        for i in range(coord - (coord % 9), coord - (coord % 9) + 9):
            results[0].append(i)
        #Same column
        for i in range(coord % 9, 81, 9):
            results[1].append(i)
        start = coord - (coord % 3) - (9 * ((coord // 9) % 3))
        for r in range(start, start + 27, 9):
            for c in range(3):
                results[2].append(r+c)
        return results

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
    
    def len_domains(self, i):
        return len(self.domains[i])