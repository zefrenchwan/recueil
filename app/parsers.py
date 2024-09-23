from typing import Tuple
import re


class TreeParser:
    """
    Parses a hierarchy csv file
    """    
    def __init__(self):
        # all completed lines
        self.paths:list[str] = []
        # current elements per index, from line and previous values
        self.elements: dict[int,str] = dict()
        self.separator = ','

    def split(self, line:str) -> list[str]:
        if len(line) == 0 or re.match(r"\s+", line):
            return list()
        # split the line  
        clean_line = line.strip().split(self.separator)
        size = len(clean_line)
        if size == 0:
            return list()
        # and now to the token matching, just clean data, avoid extra , if any
        values = list()
        index = 0
        for token in line.strip().split(self.separator):
            token = token.strip()
            if index <= size - 2:
                values.append(token)
            elif len(token) != 0:
                values.append(token)
            index = index + 1 
        return values

    def add(self, line: str):
        """
        Reads a line from a hierarchy file
        """
        # parse line, that is split with separator and normalize
        values = self.split(line)
        # complete the line to get the full hierarchy
        size = len(values)
        # step one: clean values from self.elements
        indexes_to_clean = list()
        for i in self.elements:
            if i >= size:
               indexes_to_clean.append(i)
            elif values[i] != "":
                self.elements[i] = values[i]
        for index in indexes_to_clean:
            del self.elements[index] 
        # step 2, get value from line, or previous set value if not found
        completed_line = list()
        for index in range(0, size):
            element = values[index]
            if len(element) == 0:
                element = self.elements.get(index, '')
                if len(element) == 0:
                    raise Exception(f'no data for level {index}')
            element = element.upper()
            completed_line.append(element) 
            self.elements[index] = element 
        if len(completed_line) != 0:
            self.paths.append(completed_line)

    def expand(self) -> list[Tuple[str]]:
        """
        Get the list of all parent -> child links 
        and all the roots (with no child) values
        """
        all_roots = set()
        all_values = set()
        for path in self.paths: 
            all_roots.add(path[0])
            if len(path) != 1:
                all_roots.remove(path[0])
                for i in range(1, len(path)):
                    parent = path[i-1]
                    child = path[i]
                    value = (parent, child)
                    all_values.add(value)
        for root in all_roots:
            all_values.add(root)
        return all_values
