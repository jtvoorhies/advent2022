# Advent of Code

from enum import Enum, auto
from functools import reduce
from itertools import repeat

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
    solver = solvePart1
    if part == 2:
        solver = solvePart2
    solutionUnderTest = solver(inputProvider.getInput())
    if expectedSolution != ():
        if expectedSolution == solutionUnderTest:
            finishChar = "✅"
        else:
            finishChar = "❌"
    print(finishChar, "Solution found:", solutionUnderTest,
          "  expected:", str(expectedSolution), "\n")


def isInterestingCycle(n: int) -> bool:
    return (n - 20) % 40 == 0


def solvePart1(input) -> int:
    splitByLine = input.splitlines()
    regX = 1
    cycleCount = 0
    LAST_CYCLE = 220
    instructionInputIndex = 0
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
            regX = instruction(regX)
            instructionCycleCount = 0
            instructionInputIndex += 1
            newInstructionString = splitByLine[instructionInputIndex]
            if newInstructionString == "noop":
                instruction = lambda n: n
                instructionCyclesRequired = 1
            elif newInstructionString.startswith("addx "):
                parameter = int(newInstructionString[5:])
                instruction = lambda n: n + parameter
                instructionCyclesRequired = 2
    output = reduce(lambda l, r: l + r, signalStrengths)
    return output


class Display:
    """Python's 'str' is immutable."""

    def __init__(self):
        self.data = list(repeat(False, 240))

    def strView(self) -> str:
        '''The string representation of the display'''
        rows = list()
        for row in range(0, 6):
            start = 40 * row
            end = start + 40
            characters = map(lambda b: "#" if b else ".", self.data[start:end])
            s = ''.join(characters)
            rows.append(s)
        return "\n".join(rows)

    def betterStrView(self) -> str:
        '''The string representation of the display'''
        rows = list()
        for row in range(0, 6):
            start = 40 * row
            end = start + 40
            characters = map(lambda b: "█" if b else " ", self.data[start:end])
            s = ''.join(characters)
            rows.append(s)
        return "\n".join(rows)

    def update(self, regX: int, cycle: int):
        """Use the value of 'regX' and the current 'cycle' to update 'data'."""
        cycle0 = cycle - 1
        horizDrawCenter = cycle0 % 40
        spriteRange = list([regX - 1,
                            regX,
                            regX + 1])
        if horizDrawCenter in spriteRange:
            self.data[cycle0] = True


def solvePart2(input: str) -> str:
    splitByLine = input.splitlines()
    cycleCount = 0
    regX = 1
    display = Display()
    instCycleCount = 0
    instStr = splitByLine[0]
    instCyclesNeeded = 1
    instruction: lambda n: n
    if instStr == "noop":
        pass
    elif instStr.startswith("addx"):
        parameter = int(instStr[5:])
        instruction = lambda n: n + parameter
        instCyclesNeeded = 2
    LAST_CYCLE = 240
    instIndex = 1
    while (cycleCount < LAST_CYCLE) and (instStr != "HALT"):
        cycleCount += 1
        instCycleCount += 1

        # draw pixel
        display.update(regX, cycleCount)

        # check instructions
        if instCycleCount >= instCyclesNeeded:
            regX = instruction(regX)
            instCycleCount = 0
            if instIndex < len(splitByLine):
                instStr = splitByLine[instIndex]
            else:
                instStr = "HALT"
            if instStr == "noop":
                instCyclesNeeded = 1
                instruction = lambda n: n
            elif instStr.startswith("addx "):
                parameter = int(instStr[5:])
                instCyclesNeeded = 2
                instruction = lambda n: n + parameter
            instIndex += 1
    # output = display.strView()
    output = display.betterStrView()
    print('-------   output  -------')
    print(output)
    return output


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=13140)
run(InputProvider.INPUTFILE, part=1, expectedSolution=13480)
# run(InputProvider.EXAMPLE, part=2)
run(InputProvider.INPUTFILE, part=2)
