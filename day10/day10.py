# Advent of Code

from enum import Enum, auto

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
    solutionUnderTest = solvePart1(inputProvider.getInput())
    if expectedSolution != ():
        if expectedSolution == solutionUnderTest:
            finishChar = "✅"
        else:
            finishChar = "❌"
    print(finishChar, "Solution found:", solutionUnderTest,
          "  expected:", str(expectedSolution), "\n")


def parseInput(input: str) -> list:
    instructions = list()
    for line in input.splitlines():
        if line == "noop":
            instructions.append(None)
        elif line.startswith("addx "):
            num = int(line[5:])
            instructions.append(num)
    return instructions


def interestingCycle(cycleCount) -> bool:
    if cycleCount == 0:
        return False
    if ((cycleCount - 20) % 40) == 0:
        return True
    else:
        return False


def addx(register: int, parameter: int) -> int:
    return register + parameter


def noop(register: int) -> int:
    return register


def solvePart1(input) -> int:
    rx = 1
    cycleCount = 0
    LAST_CYCLE = 220
    cycleCountInstruction = 0
    instructions = parseInput(input)
    instructionPointer = 0
    interestingRegisterValues = list()
    while cycleCount < LAST_CYCLE:
        if interestingCycle(cycleCount):
            interestingRegisterValues.append(rx)
        cycleCount += 1
        cycleCountInstruction += 1
        currentInstruction = instructions[instructionPointer]
        instructionRequiredCycles: int
        currentInstructionFunction = ()
        if currentInstruction:
            instructionRequiredCycles = 2
            currentInstructionFunction = addx
        else:
            instructionRequiredCycles = 1
            currentInstructionFunction = noop
        if cycleCountInstruction >= instructionRequiredCycles:
            # apply function
            rx = currentInstructionFunction(rx)
            # start next instruction
            instructionPointer += 1
            cycleCountInstruction = 0



# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=13140)
# run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
