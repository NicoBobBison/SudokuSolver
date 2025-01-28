import numpy as np
import queue

# Coordinates start with 0 at top left, then move right and wrap around. Bottom right is 80.
class Puzzle:
    def __init__(self, rows):
        self.domains = []
        combined = []
        for r in rows:
            combined += r
        for val in combined:
            if val == 0:
                self.domains.append([1, 2, 3, 4, 5, 6, 7, 8, 9])
            else:
                self.domains.append([val])

    # AC-3
    def solve(self):
        q = queue.Queue()
        for group in self.__get_all_rows() + self.__get_all_columns() + self.__get_all_boxes():
            for pair in self.__alldiff(group):
                q.put(pair)
                # print(f"Put: {pair}")
        while not q.empty():
            popped = q.get()
            # print(f"Popped: {popped}")
            if self.__revise(popped[0], popped[1]):
                for neighbor in self.__get_neighbors(popped[0]):
                    q.put(neighbor)
                    # print(f"New put: {neighbor}")
        return self.domains
    
    def __revise(self, x, y):
        try:
            xval = self.domains[x][0]
            yval = self.domains[y][0]
        except:
            print("Error")
            print(self.domains)
            print((x, y))
            exit()
        if len(self.domains[x]) == 1 and xval in self.domains[y]:
            self.domains[y].remove(xval)
            return True
        if len(self.domains[y]) == 1 and yval in self.domains[x]:
            self.domains[x].remove(yval)
            return True
        return False

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
    