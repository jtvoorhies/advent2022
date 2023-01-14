# Advent of Code

from enum import Enum, auto

# global variable to make functions more chatty for debugging
verbose = True


class InputProvider(Enum):
    """The function getInput() is the star here, giving you the input string to
    work with."""
    EXAMPLE1 = auto()
    EXAMPLE2 = auto()
    EXAMPLE3 = auto()
    EXAMPLE4 = auto()
    EXAMPLE5 = auto()
    INPUTFILE = auto()

    def getInput(self) -> str:
        match self:
            case InputProvider.EXAMPLE1:
                return "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
            case InputProvider.EXAMPLE2:
                return "bvwbjplbgvbhsrlpgdmjqwftvncz"
            case InputProvider.EXAMPLE3:
                return "nppdvjthqldpwncqszvftbrmjlhg"
            case InputProvider.EXAMPLE4:
                return "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"
            case InputProvider.EXAMPLE5:
                return "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
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


def solve(input, part=1) -> int:
    windowEnd = 3   # the 4-character window to test for uniqueness.
    foundStartOfPacketMarker = False
    while not foundStartOfPacketMarker:
        windowEnd = windowEnd + 1
        windowStart = windowEnd - 4
        substring = input[windowStart : windowEnd]
        windowSet = set(substring)
        if len(windowSet) == 4:
            foundStartOfPacketMarker = True
    return windowEnd



# TODO: fill in example solution
run(InputProvider.EXAMPLE1, part=1, expectedSolution=7)
run(InputProvider.EXAMPLE2, part=1, expectedSolution=5)
run(InputProvider.EXAMPLE3, part=1, expectedSolution=6)
run(InputProvider.EXAMPLE4, part=1, expectedSolution=10)
run(InputProvider.EXAMPLE5, part=1, expectedSolution=11)
run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
