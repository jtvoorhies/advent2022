# Advent of Code 2022
# Day 1: Calorie Countinge

from enum import Enum, auto
import functools


# global variable to make functions more chatty for debugging
verbose = True


class InputProvider(Enum):
    """The function getInput() is the star here, giving you the input string to
    work with."""
    EXAMPLE = auto()
    INPUTFILE = auto()

    def getInput(self) -> str:
        match self:
            case InputProvider.EXAMPLE:
                return """\
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""
            case InputProvider.INPUTFILE:
                inputFile = open("input.txt", mode="rt")
                return inputFile.read()


def solve(input: str, part=1) -> int:
    # don't use splitlines() because we want to keep the blank lines
    splitByLine = input.split("\n")

    elves = []
    currentGroup = []
    for line in splitByLine:
        if line == '' and len(currentGroup) > 0:     # end of current
            sum = functools.reduce(lambda l, r: l+r, currentGroup)
            elves.append(sum)
            currentGroup = []
        else:
            n = int(line)
            currentGroup.append(n)
    if part == 1:
        biggestElf = max(elves)
        if verbose:
            print("solveλ elves:", elves)
            print("     λ biggest elf:", biggestElf)
        return biggestElf
    elif part == 2:
        elves.sort()
        topThree = elves[-3:]
        if verbose:
            print("solveλ elves:", elves)
            print("     λ top3 elves:", topThree)
        sumOfTopThree = functools.reduce(lambda l, r: l+r, topThree)
        return sumOfTopThree


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


run(InputProvider.EXAMPLE, part=1, expectedSolution=24000)
run(InputProvider.INPUTFILE, part=1)
run(InputProvider.EXAMPLE, part=2, expectedSolution=45000)
run(InputProvider.INPUTFILE, part=2)
