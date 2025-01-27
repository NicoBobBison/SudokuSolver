import numpy as np
import queue

class Puzzle:
    def __init__(self, rows):
        self.row_domains = []
        for row_count, row in enumerate(rows):
            self.row_domains.append([])
            for val_count, val in enumerate(row):
                self.row_domains[row_count].append([])
                if val == 0:
                    self.row_domains[row_count][val_count] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                else:
                    self.row_domains[row_count][val_count] = [val]
        # print(self)
        # print("\n")
        # print(self.__get_all_boxes())

    def solve(self):
        q = queue.Queue()
        for row in self.__get_all_rows():
            q.put(row)
        for col in self.__get_all_columns():
            q.put(col)
        for box in self.__get_all_boxes():
            q.put(box)
        while not q.empty():
            popped = q.get()
            if self.__alldiff(popped):
                q.put(popped)
        return self.row_domains

    # Updates each list in domains to retain consistency
    # Returns true if the domains were updated
    def __alldiff(self, domains):
        was_changed = False
        dom = sorted(domains, key=len)
        if len(dom[0]) > 1:
            # No singleton domains
            return False
        
        for i in range(len(dom)):
            if len(dom[i]) == 1:
                val = dom[i][0]
                for list in dom[i + 1:]:
                    if val in list:
                        list.remove(val)
                        was_changed = True
        
        return was_changed
    
    def __get_all_rows(self):
        return self.row_domains

    def __get_all_columns(self):
        domains = []
        for row in range(9):
            domains.append([])
            for col in range(9):
                domains[row].append(self.row_domains[col][row])
        return domains
    
    def __get_all_boxes(self):
        domains = []
        for start_row in range(3):
            for start_col in range(3):
                domains.append([])
                for row in range(start_row * 3, (start_row + 1) * 3):
                    for col in range(start_col * 3, (start_col + 1) * 3):
                        domains[start_row * 3 + start_col].append(self.row_domains[row][col])
        return domains
        
    def __str__(self):
        return "\n\n".join("\n".join(str(y) for y in x) for x in self.row_domains)