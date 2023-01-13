# Advent of Code 2022 day 05 "Supply Stacks"

from enum import Enum, auto
from more_itertools import chunked
import re
import sys

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
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
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


class Dock:
    '''Ivar: stacks: an [[str]].  As the stack numbers are zero-based, they
    will be numbered one less than the puzzle input.'''

    def __init__(self, stacks: [[str]]):
        self.stacks = stacks

    STACKLABELMATCHER = re.compile(" ([0-9]+)\s*$")

    @staticmethod
    def fromLines(input: [str]):
        '''Create a new Dock from lines of input.  Parameter should be [str]'''
        print("fromLinesλ =====")
        print(input)
        print("---------")
        # look at numeric labels on line just before partition line.  That will
        # tell how many stacks we need
        labelLine: str = input[-1]
        print("Dock.fromLinesλ type(labelLine):", type(labelLine),
              "  content of labelLine starts on next line.\n", labelLine)
        lastLabelMatch = Dock.STACKLABELMATCHER.search(labelLine)
        if not lastLabelMatch:
            print("Unable to find a match in the labelLine",
                file=sys.stderr)
        print("Dock.fromLinesλ type(lastLabelMatch) is:", type(lastLabelMatch))
        lastStackLabel = int(lastLabelMatch.group()[1])
        print("Dock.fromLinesλ lastStackLabel:", lastStackLabel)

        myStacks = list(list())
        # initialize myStacks with empty stacks, count equal to last label
        for n in range(lastStackLabel):
            myStacks.append(list())

        print("Dock.fromLinesλ myStacks:", myStacks)
        checkMatcherRegEx = re.compile('\[([A-Z])\]')
        for line in input:
            chunkedLine = chunked(line, 4)

            i = 0
            for chunkl in chunkedLine:
                chunk = str(chunkl)
                lBracket = chunk.find('[')
                if lBracket > -1:
                    crateIndex = lBracket + 1
                    crate = chunk[crateIndex]
                    print('Found crate:', crate, 'in chunk:', chunk, "from chunkl:", chunkl)
                    myStacks[i].append(crate)
                i = i + 1

        # reverse stacks
        for stack in myStacks:
            stack.reverse()
        # return Dock
        dock = Dock(myStacks)
        return dock

    def stackCount(self) -> int:
        '''Total number of stacks.'''
        return len(self.stacks)

    def maxStackHeight(self) -> int:
        '''The length of the deepest stack.'''
        heights: [int] = map(lambda stack: len(stack), self.stacks)
        return max(heights)

    def topCrateInEachStack(self) -> str:
        '''A string composed of the letter of the top crate in each stack.'''
        output: str = ''
        for stack in self.stacks:
            length = len(stack)
            if length > 0:
                output = output + stack[length - 1]
        return output

    def move(self, count: int, fromStack: int, toStack: int):
        '''The fromStack/toStack will be decremented by 1 because input is
        1-based index while python list is 0-based index.'''
        assert type(count) == int, count >= 0
        assert type(fromStack) == int, fromStack in range(1, self.stackCount() + 1)
        assert type(toStack) == int, toStack in range(1, self.stackCount() + 1)
        print("Dock.moveλ =====  {0:>4d},  {1:>4d} ➙ {2:>4d}"\
              .format(count, fromStack, toStack), "  =====")
        # self.prettyPrint()
        # the slice makes a new list.
        moveables = self.stacks[fromStack - 1][-count:]
        del self.stacks[fromStack - 1][-count:]
        moveables.reverse
        self.stacks[toStack - 1].extend(moveables)

    def prettyPrint(self):
        # print("prettyPrintλ self.stacks:", self.stacks)
        for level in range(self.maxStackHeight() - 1, -1, -1):
            filteredIndexes = []
            for index, aStack in enumerate(self.stacks):
                if len(aStack) > level:
                    filteredIndexes.append(index)
            for n in range(0, self.stackCount()):
                if n in filteredIndexes:
                    oneCharString = self.stacks[n][level]
                    print('[{}] '.format(oneCharString), end='')
                else:
                    # print 4 spaces
                    print('    ', end='')
            print()  # end the line
        for stackLabel in range(1, self.stackCount() + 1):
            print('{:^4d}'.format(stackLabel), end='')
        print()  # end the line


def makeDock(input: [str]) -> Dock:
    labelLine = input.pop()
    MATCHER = re.compile(' ([0-9]+)$')
    labelMatched = MATCHER.search(labelLine).group()[1]
    stackCount = int(labelMatched)
    print('🚢 makeDock: ', stackCount)

    myStacks = list()
    firstCargosLine = input.pop()
    for stack in range(0, stackCount):
        startIdx = 4 * stack
        endIdx = min(startIdx + 4, len(firstCargosLine))
        lineSlice = firstCargosLine[startIdx:endIdx]
        lBracket = lineSlice.find('[')
        newStack = list()
        if lBracket > -1:
            rBracket = lineSlice.find(']')
            assert rBracket > -1
            cargoIdx = lBracket + 1
            cargo = lineSlice[cargoIdx:rBracket]
            newStack = list(cargo)
        myStacks.append(newStack)

    print("myStacks:", myStacks)

    while len(input) > 0:
        cargosLine = input.pop()
        for stack in range(0, stackCount):
            startIdx = 4 * stack
            if startIdx < len(cargosLine):
                endIdx = min(startIdx + 4, len(cargosLine))
                lineSlice = cargosLine[startIdx:endIdx]
                lBracketIdx = lineSlice.find('[')
                if lBracketIdx > -1:
                    rBracketIdx = lineSlice.find(']')
                    assert rBracketIdx > -1
                    cargoIdx = lBracket + 1
                    cargo = lineSlice[cargoIdx:rBracketIdx]
                    myStacks[stack].append(cargo)
            print("myStacks:", myStacks)

    return Dock(myStacks)


class Move:

    MOVELINEREGEX = re.compile("move ([0-9]+) from ([0-9]+) to ([0-9]+)")

    def __init__(self, count: int, fromStack: int, toStack: int):
        self.count = count
        self.fromStack = fromStack
        self.toStack = toStack

    def fromString(string):
        '''Create and return a Move instance from a str.'''
        matches = Move.MOVELINEREGEX.search(string)
        count = int(matches.groups()[0])
        fromStack = int(matches.groups()[1])
        toStack = int(matches.groups()[2])
        return Move(count, fromStack, toStack)


def solve(input, part=1) -> str:
    splitByLines = input.splitlines()
    splitLineIndex = splitByLines.index('')
    # includes the label string of each line
    dockLines: [str] = splitByLines[:splitLineIndex]
    # dock = Dock.fromLines(dockLines)
    dock = makeDock(dockLines)
    if verbose:
        print("solveλ initial Dock: =============")
        dock.prettyPrint()
    moveLines: [str] = splitByLines[splitLineIndex + 1:]
    moves = map(lambda l: Move.fromString(l), moveLines)
    for move in moves:
        dock.move(move.count, move.fromStack, move.toStack)
        if verbose:
            print("solveλ move count: {0: >2} fromStack: {1: >2} toStack: {2: >2}"\
                  .format(move.count, move.fromStack, move.toStack))
    return dock.topCrateInEachStack()


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution='CMZ')
# run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
