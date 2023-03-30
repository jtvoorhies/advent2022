# Advent of Code

from enum import Enum, auto
from functools import reduce

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
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""
            case InputProvider.INPUTFILE:
                inputFile = open("input.txt", mode="rt")
                return inputFile.read()


def run(inputProvider, part=1, expectedSolution=()):
    print("Solving part", part, "for", inputProvider)
    if (part < 1) or (part > 2):
        raise ValueError("parameter 'part' must be a one or two.")
    finishChar = "🏁"
    solutionUnderTest = solvePart1(inputProvider.getInput(), part=part)
    if expectedSolution != ():
        if expectedSolution == solutionUnderTest:
            finishChar = "✅"
        else:
            finishChar = "❌"
    print(finishChar, "Solution found:", solutionUnderTest,
          "  expected:", str(expectedSolution), "\n")


def isInterestingCycle(n: int) -> bool:
    return (n - 20) % 40 == 0


def solvePart1(input, part=1) -> int:
    splitByLine = input.splitlines()
    regX = 1
    cycleCount = 0
    LAST_CYCLE = 220
    instructionInputIndex = 1
    instructionCycleCount = 0
    instructionCyclesRequired = 1
    signalStrengths = list()
    instruction = lambda n: n
    if splitByLine[0] == "noop":
        pass
    elif splitByLine[0].startswith("addx"):
        parameter = int(splitByLine[0][5:])
        instruction = lambda n: n + parameter
        instructionCyclesRequired = 2
    while cycleCount < LAST_CYCLE:
        cycleCount += 1
        instructionCycleCount += 1
        if isInterestingCycle(cycleCount):
            signalStrengths.append(cycleCount * regX)
            if verbose:
                print("Cycle:", cycleCount)
                print("signalStrengths:", signalStrengths)
        if instructionCycleCount >= instructionCyclesRequired:
            # apply instruction
            # if verbose:
            #     print("cycle #", cycleCount, "regX =", regX, " → ", instruction(regX))
            regX = instruction(regX)
            instructionCycleCount = 0
            newInstructionString = splitByLine[instructionInputIndex]
            if newInstructionString == "noop":
                instruction = lambda n: n
                instructionCyclesRequired = 1
            elif newInstructionString.startswith("addx "):
                parameter = int(newInstructionString[5:])
                instruction = lambda n: n + parameter
                instructionCyclesRequired = 2
            instructionInputIndex += 1
    output = reduce(lambda l, r: l + r, signalStrengths)
    return output


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=13140)
run(InputProvider.INPUTFILE, part=1, expectedSolution=13480)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
