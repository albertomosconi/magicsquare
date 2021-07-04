from copy import deepcopy
import random
from Solution import Solution

opposites: dict[str, str] = {"l": "r", "u": "d", "r": "l", "d": "u",
                             "ul": "dr", "ur": "dl", "dl": "ur", "dr": "ul"}


def nextPossibleMoves(square: list[list[int]], currentCell: tuple[int, int], previousMove: str = None) -> list[str]:
    cx, cy = currentCell

    moves: list[str] = []
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
        moveToExclude: str = opposites[previousMove]
        if (moveToExclude in moves):
            moves.remove(opposites[previousMove])

    return moves


def nextCell(currentCell: tuple[int, int], move: str) -> tuple[int, int]:
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
    return (-1, -1)


def baseSquare() -> list[list[int]]:
    """creates an empty 10x10 grid of zeros

    :return: the empty square
    :rtype: list[list[int]]
    """
    square: list[list[int]] = []
    for _ in range(10):
        row: list[int] = []
        for _ in range(10):
            row.append(0)
        square.append(row)
    return square


def computeSolution(
    square: list[list[int]],
    currentCell: tuple[int, int],
    currentIndex: int,
    cellSequence: list[tuple[int, int]],
    moveSequence: list[str]
) -> Solution:

    possibleMoves: list[str] = nextPossibleMoves(square, currentCell)

    if (len(cellSequence) > 0):
        cellSequence = cellSequence[:-1]
        moveSequence = moveSequence[:-1]

    while(len(possibleMoves) > 0):
        moveChoice = random.choice(possibleMoves)
        moveSequence.append(moveChoice)

        square[currentCell[1]][currentCell[0]] = currentIndex
        cellSequence.append(currentCell)

        currentCell = nextCell(currentCell, moveChoice)
        possibleMoves = nextPossibleMoves(square, currentCell, moveChoice)

        currentIndex += 1

    cellSequence.append(currentCell)
    square[currentCell[1]][currentCell[0]] = currentIndex

    solution = Solution(square, moveSequence, cellSequence,
                        currentIndex)
    return solution


def generateInitialPopulation(size: int) -> list[Solution]:
    """returns an initial population of random solutions

    :param size: the size of the population
    :type size: int
    :return: the initial population
    :rtype: list[Solution]
    """
    population: list[Solution] = []
    for _ in range(size):
        square: list[list[int]] = baseSquare()

        currentCell: tuple[int, int] = (
            random.randint(0, 9), random.randint(0, 9))

        solution: Solution = computeSolution(
            square, currentCell, 1, [], [])

        population.append(solution)

    return population


def selectFittest(population: list[Solution]) -> list[Solution]:
    """given a population of solutions, returns only the 15% best ones

    :param population: the original population
    :type population: list[Solution]
    :return: the 15% with the best score
    :rtype: list[Solution]
    """
    population.sort(key=lambda s: s.score, reverse=True)
    return deepcopy(population[:int(len(population)*0.15)])


def regrowPopulation(population: list[Solution], requiredSize: int) -> list[Solution]:
    """take a small sample of a population and regrow it by 
    generating mutations until the required size is reached

    :param population: the sample of population
    :type population: list[Solution]
    :param requiredSize: the required number of elements in the population
    :type requiredSize: int
    :return: the full population
    :rtype: list[Solution]
    """

    mutatedSolutions: list[Solution] = []
    # loop until the population is full again
    while (len(mutatedSolutions) < requiredSize - len(population)):
        # select a random 'parent' solution to mutate
        randomParent: Solution = random.choice(population)
        # select a random step, this is where the mutation starts
        mutatedStep: int = random.randint(0, len(randomParent.moveSequence)-1)
        baseSquare: list[list[int]] = randomParent.squareAtStep(mutatedStep+1)
        startingCell: tuple[int, int] = randomParent.cellSequence[mutatedStep]

        # 'regrow' the solution starting from the mutated step
        solution: Solution = computeSolution(
            deepcopy(baseSquare),
            deepcopy(startingCell), deepcopy(mutatedStep+1),
            randomParent.cellSequence[:mutatedStep+1],
            randomParent.moveSequence[:mutatedStep+1])

        mutatedSolutions.append(solution)

    return deepcopy(population + mutatedSolutions)


POP_SIZE = 1000

population = generateInitialPopulation(POP_SIZE)
fittest = selectFittest(population)
generationCounter = 0
while(fittest[0].score < 100):
    print(f"generation {generationCounter}: best {fittest[0].score}", end="\r")
    generationCounter += 1
    if (generationCounter < 200):
        population = regrowPopulation(fittest, POP_SIZE)
    else:
        print("too many generations, resetting evolution...")
        population = generateInitialPopulation(POP_SIZE)
        generationCounter = 0
    fittest = selectFittest(population)

# select only the complete solutions
best: list[Solution] = list(filter(lambda s: s.score == 100, fittest))
# check validity of solutions
for b in best:
    if not b.isValid():
        raise Exception("Unexpected error")

# display
print()
if (len(best) == 1):
    print("SOLUTION FOUND")
else:
    print("MULTIPLE SOLUTIONS FOUND")
print(f"total generations: {generationCounter}")
for i, b in enumerate(best):
    print(f"solution {i+1}:")
    b.display()
