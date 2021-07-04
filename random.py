from pprint import pprint as p
import random

opposites = {"l": "r", "u": "d", "r": "l", "d": "u",
             "ul": "dr", "ur": "dl", "dl": "ur", "dr": "ul"}


def nextPossibleMoves(square, currentCell, previousMove=None):
    cx, cy = currentCell
    # p(f"possible moves from {cx}, {cy} - (previous move {previousMove})")

    moves = []
    if (cx > 2 and square[cy][cx-3] == 0):
        moves.append("l")
    if (cx < 7 and square[cy][cx+3] == 0):
        moves.append("r")
    if (cy > 2 and square[cy-3][cx] == 0):
        moves.append("u")
    if (cy < 7 and square[cy+3][cx] == 0):
        moves.append("d")
    if (cx > 1 and cy > 1 and square[cy-2][cx-2] == 0):
        moves.append("ul")
    if (cx < 8 and cy > 1 and square[cy-2][cx+2] == 0):
        moves.append("ur")
    if (cx > 1 and cy < 8 and square[cy+2][cx-2] == 0):
        moves.append("dl")
    if (cx < 8 and cy < 8 and square[cy+2][cx+2] == 0):
        moves.append("dr")

    if (previousMove):
        moveToExclude = opposites[previousMove]
        if (moveToExclude in moves):
            moves.remove(opposites[previousMove])

    return moves


def nextCell(currentCell, move):
    cx, cy = currentCell
    if (move == "l"):
        return (cx-3, cy)
    if (move == "r"):
        return (cx+3, cy)
    if (move == "u"):
        return (cx, cy-3)
    if (move == "d"):
        return (cx, cy+3)
    if (move == "ul"):
        return (cx-2, cy-2)
    if (move == "ur"):
        return (cx+2, cy-2)
    if (move == "dl"):
        return (cx-2, cy+2)
    if (move == "dr"):
        return (cx+2, cy+2)


def solve(currentCell):
    # initialize square
    square = []
    for i in range(10):
        row = []
        for j in range(10):
            row.append(0)
        square.append(row)

    possibleMoves = nextPossibleMoves(square, currentCell)
    i = 1
    while(len(possibleMoves) > 0):
        moveChoice = random.choice(possibleMoves)
        square[currentCell[1]][currentCell[0]] = i
        currentCell = nextCell(currentCell, moveChoice)
        possibleMoves = nextPossibleMoves(square, currentCell, moveChoice)
        i += 1

    square[currentCell[1]][currentCell[0]] = i
    return square


# cc = (3, 3)
# p(nextPossibleMoves(cc, "l"))

def isSquareFull(square):
    for row in square:
        if 0 in row:
            return False
    return True


# p(solve(mat, (random.randint(0, 9), random.randint(0, 9))))
square = solve((random.randint(0, 9), random.randint(0, 9)))
counter = 1
while (not isSquareFull(square)):
    print(counter, end="\r")
    square = solve((random.randint(0, 9), random.randint(0, 9)))
    counter += 1
p(square)
