# Advent of Code

from enum import Enum, auto
import re


# global variable to make functions more chatty for debugging
verbose = False
# parsing each line of input
# I don't know why pycode style says \d in invalid escape sequence; it's works
inputLineRegEx = re.compile('(\d+)-(\d+),(\d+)-(\d+)')


class InputProvider(Enum):
    """The function getInput() is the star here, giving you the input string to
    work with."""
    EXAMPLE = auto()
    INPUTFILE = auto()

    def getInput(self) -> str:
        match self:
            case InputProvider.EXAMPLE:
                return """\
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
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


class InclusiveBounds:

    def __init__(self, start: int, last: int):
        # I was comparing 'str's and not 'int's before!
        # The type hints above didn't raise any flags.  So what am I not doing
        # to utilize them?
        assert start.__class__ == int
        assert last.__class__ == int
        self.start = start
        self.last = last

    def __str__(self):
        return "{0}-{1}".format(self.start, self.last)

    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.start, self.last) == (other.start, other.last)


def enclosingPair(left: InclusiveBounds, right: InclusiveBounds) -> bool:
    '''Tests pair to see if either contains the right.'''
    return (left.start <= right.start and left.last >= right.last)\
        or (left.start >= right.start and left.last <= right.last)


def overlappingPair(left: InclusiveBounds, right: InclusiveBounds) -> bool:
    return not ((left.start > right.last) or (left.last < right.start))


def solve(input, part=1) -> int:
    splitByLine = input.splitlines()
    counterForSolution = 0
    for line in splitByLine:
        matcher = inputLineRegEx.search(line)
        # I've been comparing strings and not ints!  Convert to ints.
        groups = list(map(lambda s: int(s), matcher.groups()))
        # if verbose:
        #     print("solveλ groups after map:", groups)
        leftRange = InclusiveBounds(groups[0], groups[1])
        rightRange = InclusiveBounds(groups[2], groups[3])
        solveFunction = enclosingPair
        if part == 2:
            solveFunction = overlappingPair
        if solveFunction(leftRange, rightRange):
            if verbose:
                print("solveλ MATCH FOUND:",
                      line, "   ", leftRange, "   ", rightRange)
            counterForSolution += 1
    return counterForSolution


run(InputProvider.EXAMPLE, part=1, expectedSolution=2)
run(InputProvider.INPUTFILE, part=1, expectedSolution=582)
run(InputProvider.EXAMPLE, part=2, expectedSolution=4)
run(InputProvider.INPUTFILE, part=2)
