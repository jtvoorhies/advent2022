# Advent of Code

from enum import Enum, auto

# global variable to make functions more chatty for debugging
verbose = False


class InputProvider(Enum):
    """The function getInput() is the star here, giving you the input string to
    work with."""
    EXAMPLE = auto()
    INPUTFILE = auto()

    def getInput(self) -> str:
        match self:
            case InputProvider.EXAMPLE:
                return """\
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""
            case InputProvider.INPUTFILE:
                inputFile = open("input.txt", mode="rt")
                return inputFile.read()


def run(inputProvider, part=1, expectedSolution=()):
    print("Solving part", part, "for", inputProvider)
    if (part < 1) or (part > 2):
        raise ValueError("parameter 'part' must be a one or two.")
    finishChar = "🏁"
    solutionUnderTest = solve(inputProvider.getInput(), part=part)
    if expectedSolution != ():
        if expectedSolution == solutionUnderTest:
            finishChar = "✅"
        else:
            finishChar = "❌"
    print(finishChar, "Solution found:", solutionUnderTest,
          "  expected:", str(expectedSolution), "\n")


def getPriority(char: chr) -> int:
    '''Convert parameter character (a-z,A-Z) to priority number.'''
    allLetters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    idx = allLetters.index(char)
    return idx + 1


def solve(input, part=1) -> int:
    if part == 2:
        return solvePart2(input)
    splitByLine = input.splitlines()
    prioritySum = 0
    for line in splitByLine:
        # cut in half with bitshift right
        lengthOfSack = len(line) >> 1
        leftSackStr = line[:lengthOfSack]
        rightSackStr = line[lengthOfSack:]
        if verbose:
            print("solveλ L:", leftSackStr)
            print("       R:", rightSackStr)
        leftSack = set(leftSackStr)
        rightSack = set(rightSackStr)
        shared = leftSack & rightSack
        assert len(shared) == 1
        sharedItem: chr = shared.pop()
        priority = getPriority(sharedItem)
        prioritySum += priority
        if verbose:
            print("solveλ sharedItem:", sharedItem, " priority:", priority,
                  "        prioritySum:", prioritySum)
    return prioritySum


def solvePart2(input: str) -> int:
    prioritySum = 0
    splitByLine = input.splitlines()
    for groupOf3Start in range(len(splitByLine))[::3]:
        first = set(splitByLine[groupOf3Start])
        second = set(splitByLine[groupOf3Start + 1])
        third = set(splitByLine[groupOf3Start + 2])
        commonItemSet = first & second & third
        assert len(commonItemSet) == 1
        commonItem = commonItemSet.pop()
        priority = getPriority(commonItem)
        prioritySum += priority
        if verbose:
            print("solvePart2λ groupOf3Start:", groupOf3Start,
                  "commonItem:", commonItem, "priority:", priority,
                  "prioritySum:", prioritySum)
    return prioritySum


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=157)
run(InputProvider.INPUTFILE, part=1)
run(InputProvider.EXAMPLE, part=2, expectedSolution=70)
run(InputProvider.INPUTFILE, part=2)
