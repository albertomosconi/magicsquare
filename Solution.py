from copy import deepcopy


class Solution:
    def __init__(self, square: list[list[int]], moveSequence: list[str], cellSequence: list[tuple[int, int]], score: int) -> None:
        self.square = square
        self.moveSequence = moveSequence
        self.cellSequence = cellSequence
        self.score = score

    def squareAtStep(self, stepIndex: int) -> list[list[int]]:
        partialSquare: list[list[int]] = deepcopy(self.square)
        for row in partialSquare:
            for i, cell in enumerate(row):
                if cell > stepIndex:
                    row[i] = 0
        return partialSquare

    def isValid(self) -> bool:
        i: int = 1
        while i < 101:
            found: bool = False
            for row in self.square:
                if (i in row):
                    found = True
                    continue
            if not found:
                return False
            i += 1
        return True

    def display(self):
        for row in self.square:
            rowstring = ""
            for s in row:
                c = ""
                c = str(s) + " "
                if s < 10:
                    c = "  " + c
                elif s < 100:
                    c = " " + c
                rowstring += c
            print(rowstring)
