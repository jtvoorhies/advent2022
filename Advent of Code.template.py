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
    TODO: fill in
"""
            case InputProvider.INPUTFILE:
                 inputFile = open("input.txt", mode="rt")
                 return inputFile.read()


def solve(input, part=1):
    # TODO Write solution
    return -1


def run(inputProvider, part=1, expectedSolution=()):
    print("Solving part", part, "for", inputProvider)
    if (part < 1) or (part > 2):
        raise ValueError("parameter 'part' must be a one or two.")
    finishChar = "🏁"
    solutionUnderTest = solve(inputProvider.getInput(), part=part)
    if expectedSolution is not None:
        if expectedSolution == solutionUnderTest:
            finishChar = "✅"
        else:
            finishChar = "❌"
    print(finishChar, "Solution found:", solutionUnderTest, "  expected:", str(expectedSolution), "\n")

# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=12345)
#run(InputProvider.INPUTFILE, part=1, expectedSolution=)
#run(InputProvider.EXAMPLE, part=2, expectedSolution=)
#run(InputProvider.INPUTFILE, part=2, expectedSolution=)
