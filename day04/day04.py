# Advent of Code

from enum import Enum, auto
import re


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
        self.start = start
        self.last = last
    def __str__(self):
        return "{0}-{1}".format(self.start, self.last)
    # @total_ordering methods considered
    def __eq__(self, other):
        if not self._is_valid_operand(other):
            return NotImplemented
        return (self.start, self.last) == (other.start, other.last)
    # moving to inside the class
    # def contains(self, other) -> bool:
    #     if type(self) != type(other):
    #         return NotImplemented
    #     print("wtf:")
    #     print(self.start <= other.start and self.last >= other.last)
    #     return self.start <= other.start and self.last >= other.last


def enclosingPair(left: InclusiveBounds, right: InclusiveBounds) -> bool:
    '''Tests pair to see if either contains the right.'''
    # print("enclosingPairλ", left, right)
    # print("left.start:", left.start, "left.last:", left.last,
    #       " right.start", right.start, "right.last:", right.last)
    # testA = left.start <= right.start
    # print("testA = left.start <= right.start:", testA)
    # testB = left.last >= right.last
    # print("testB = left.last >= right.last:", testB)
    # testC = left.start >= right.start
    # print("testC = left.start >= right.start:", testC)
    # testD = left.last <= right.last
    # print("testD = left.last <= right.last:", testD)
    # test1 = (left.start <= right.start) and (left.last >= right.last)
    # test2 = left.start >= right.start and left.last <= right.last
    # print("test1:", test1, '    left.start <= right.start and left.last >= right.last')
    # print("test2:", test2, '    left.start >= right.start and left.last <= right.last')
    return (left.start <= right.start and left.last >= right.last)\
        or (left.start >= right.start and left.last <= right.last)


inputLineRegEx = re.compile('(\d+)-(\d+),(\d+)-(\d+)')


def solve(input, part=1) -> int:
    splitByLine = input.splitlines()
    rangePairs: [(InclusiveBounds, InclusiveBounds)] = []
    countOfFullyContainedPairs = 0
    for line in splitByLine:
        matcher = inputLineRegEx.search(line)
        # I'm comparing strings and nto ints?
        # leftRange = InclusiveBounds(matcher.groups()[0], matcher.groups()[1])
        # rightRange = InclusiveBounds(matcher.groups()[2], matcher.groups()[3])
        groups = list(map(lambda s: int(s), matcher.groups()))
        # if verbose:
        #     print("solveλ groups after map:", groups)
        leftRange = InclusiveBounds(groups[0], groups[1])
        rightRange = InclusiveBounds(groups[2], groups[3])
        if enclosingPair(leftRange, rightRange):
        # if leftRange.contains(rightRange):
            if verbose:
                print("solveλ MATCH FOUND:", line, "   ", leftRange, "   ", rightRange)
            countOfFullyContainedPairs += 1
    return countOfFullyContainedPairs


run(InputProvider.EXAMPLE, part=1, expectedSolution=2)
run(InputProvider.INPUTFILE, part=1)
run(InputProvider.EXAMPLE, part=2, expectedSolution=4)
# run(InputProvider.INPUTFILE, part=2)
