#!/usr/bin/env python3
#
# !/usr/bin/env PYTHONPATH="${HOME}/Developer/python/usr/lib/" /usr/bin/env python3
#

from enum import Enum, auto
import itertools
from more_itertools import grouper
import array
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("sgr", "/home/jt/Developer/python/usr/lib/sgr.py")
module = importlib.util.module_from_spec(spec)
sys.modules['sgr'] = module
spec.loader.exec_module(module)


# print sgr
# print("========= sgr dir(): ==========")
# print(dir('sgr'))
# exit(0)

# global variable to make functions more chatty for debugging
verbose = True


class InputProvider(Enum):
    """The function getInput() is the star here, giving you the input string to
    work with."""
    EXAMPLE   = auto()
    INPUTFILE = auto()

    def getInput(self) -> str:
        match self:
            case InputProvider.EXAMPLE:
                return """\
30373
25512
65332
33549
35390
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



class Direction(Enum):
    NORTH = auto()
    SOUTH = auto()
    EAST  = auto()
    WEST  = auto()

    def neighborTransform(self):
        match self:
            case Direction.NORTH:
                return Coordinate(-1, 0)
            case Direction.SOUTH:
                return Coordinate( 1, 0)
            case Direction.EAST:
                return Coordinate(0,  1)
            case Direction.WEST:
                return Coordinate(0, -1)


class Coordinate:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x
    def __add__(self, other):
        newX = self.x + other.x
        newY = self.y + other.y
        return Coordinate(newY, newX)


class TreeGrid:
    def __init__(self, height: int, width: int, grid: [int]):
        assert (width * height) == len(grid)
        self.height = height
        self.width = width
        self.grid = grid
    def makeIndex(self, coordinate) -> int:
        index = (coordinate.y * self.width) + coordinate.x
        assert index < len(self.grid)
        return index
    def __getitem__(self, coordinate):
        return self.grid[makeIndex(coordinate)]
    def __setitem__(self, coordinate, newValue):
        self.grid[makeIndex(coordinate)] = newValue
    def areAllCoordsLessThan(self, coords: [Coordinate], treeCoord: Coordinate) -> bool:
        treeHeight = self.grid[self.makeIndex(treeCoord)]
        for c in coords:
            if self.grid[self.makeIndex(c)] >= treeHeight:
                return False
        return True
    def isVisibleFromOutside(self, coordinate) -> bool:
        # is it on the edge?
        if (coordinate.x == 0) or (coordinate.x == (self.width - 1)):
            return True
        if (coordinate.y == 0) or (coordinate.y == (self.height - 1)):
            return True
        # check heights
        #   vertical
        toTopEdgeYrange  = range(0, coordinate.y - 1)
        toTopEdge = list(map(lambda y: Coordinate(y, coordinate.x), toTopEdgeYrange))
        toBotEdgeYrange  = range(coordinate.y + 1, self.height - 1)
        toBotEdge = list(map(lambda y: Coordinate(y, coordinate.x), toBotEdgeYrange))
        toWestEdgeXrange = range(0, coordinate.x - 1)
        toWestEdge = list(map(lambda x: Coordinate(coordinate.y, x), toWestEdgeXrange))
        toEastEdgeXrange = range(coordinate.x + 1, self.width - 1)
        toEastEdge = list(map(lambda x: Coordinate(coordinate.y, x), toEastEdgeXrange))
        edgeGroups = [toTopEdge, toBotEdge, toWestEdge, toEastEdge]
        for edgeGroup in edgeGroups:
            if self.areAllCoordsLessThan(edgeGroup, coordinate):
                return True
        return False
    def prettyPrint(self):
        chunks = list(grouper(self.grid, self.width))
        print("---- TREE GRID   w: {0}   h: {1} ----".format(self.width, self.height))

        line1 = "X→            1    1    2    2    3"
        line2 = "Y↓  0    5    0    5    0    5    0"
        line3 = "  ┌────────────────────────────────"
        maxLength = 5 + self.width
        lines1to3 = [line1, line2, line3]
        lines1to3Trimmed = map(lambda l: l[:maxLength], lines1to3)
        for l in lines1to3Trimmed:
            print(l)
        #for chunk in chunks:
        for h in range(0, self.height):
            chunk = chunks[h]
            chars = map(lambda n: str(n), chunk)
            line = ''.join(chars)
            print("{0:<2}│".format(h), line)

    def makeGridOfVisible(self) -> [int]:
        """Makes an array (flattened 2d grid) same `len` as self.grid, of
integers.  0 = not visible, 1 = visible interior, 2 = visible because it's on an edge
"""
        grid = list()    # list of array.array('i')
        for y in range(0, self.height):
            row = array.array('i')
            for x in range(0, self.width):
                coord = Coordinate(y, x)
                isVisible = self.isVisibleFromOutside(coord)
                if isVisible:
                    if (y == 0) or (y == (self.height - 1)) or \
                       (x == 0) or (x == (self.width - 1)):
                        row.append(2)
                    else:
                        row.append(1)
                else:
                    row.append(0)
            grid.append(row)
        flattened = array.array('i')
        for row in grid:
            flattened.extend(row)
        return flattened
    def prettyPrintColor(self):
        # Escape Sequences
        fgWhite = "\u001B[38;5;7m"
        fgYellow = "\u001B[38;5;3m"
        fgGreen = "\u001B[38;5;2m"
        fgCyan = "\u001B[38;5;6m"
        fgOff = "\u001B[39m"
        bold = "\u001B[1m"
        boldOff = "\u001B[22m"

        def format(treeHeight: int, visibility: int) -> str:
            start = ''
            match visibility:
                case 0:  # not visible
                    start = fgWhite
                case 1:  # visible
                    start = fgYellow
                case 2:  # visible on the edge
                    start = fgGreen
            return start + str(treeHeight) + fgOff

        chunks = list(grouper(self.grid, self.width))
        print("---- TREE GRID   w: {0}   h: {1} ----".format(self.width, self.height))

        line1 = "{0}X→{1}            1    1    2    2    3{2}"\
            .format(fgCyan + bold, boldOff, fgOff)
        line2 = "{0}Y↓{1}  0    5    0    5    0    5    0{2}"\
            .format(fgCyan + bold, boldOff, fgOff)
        line3 = "  {0}┌────────────────────────────────{1}".format(fgCyan, fgOff)
        # maxLength = 5 + self.width
        # lines1to3 = [line1, line2, line3]
        # lines1to3Trimmed = map(lambda l: l[:maxLength], lines1to3)
        # line3 += fgOff
        # for l in lines1to3Trimmed:
        #     print(l)
        for l in [line1, line2, line3]:
            print(l)

        vGrid = self.makeGridOfVisible()

        lines = list()
        for y in range(0, self.height):
            # chunk = chunks[y]
            # chars = map(lambda n: format(n), chunk)
            # line = ''.join(chars)
            line = ''
            for x in range (0, self.width):
                coord = Coordinate(y, x)
                idx = self.makeIndex(coord)
                treeheight = self.grid[idx]
                visibility = vGrid[idx]
                output = format(treeheight, visibility)
                line += output
            lines.append(line)

        for line in lines:
            print('{0:<2}│'.format(y), line)



def parse(input: str) -> TreeGrid:
    splitByLine = input.splitlines()
    trees = list()
    lineLengths = set()
    for line in splitByLine:
        nums = list()
        lineAsList = list(line)
        lineLengths.add(len(lineAsList))
        if len(lineLengths) > 1:
            print("ERRROR: lineLengths > 1.  length followed by content:", len(lineLengths))
            print(lineLengths)
        assert len(lineLengths) == 1
        for char in lineAsList:
            newNum = int(char)
            nums.append(newNum)
        a = array.array('i')
        a.fromlist(nums)
        trees.append(a)
    width = lineLengths.pop()
    height = len(trees)
    assert height == len(splitByLine)
    flattenTrees = array.array('i')
    for arr in trees:
        flattenTrees.extend(arr)
    return TreeGrid(height, width, flattenTrees)


def solve(input: str, part=1) -> int:
    treeGrid = parse(input)
    # TODO Write solution
    treeGrid.prettyPrint()
    print("---------------")
    treeGrid.prettyPrintColor()
    print("---------------")
    visibleCount = 0
    for y in range(0, treeGrid.height):
        for x in range(0, treeGrid.width):
            c = Coordinate(y, x)
            isVisible = treeGrid.isVisibleFromOutside(c)
            if isVisible:
                visibleCount += 1
    return visibleCount


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=21)
# run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
