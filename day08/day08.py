#!/usr/bin/env python3


from enum import Enum, auto
from functools import reduce
from more_itertools import grouper
import array


# global variable to make functions more chatty for debugging
verbose = False


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
    expectedSolutionStr = ''
    if expectedSolution != ():
        expectedSolutionStr = '  expected: ' + str(expectedSolution)
        if expectedSolution == solutionUnderTest:
            finishChar = "✅"
        else:
            finishChar = "❌"
    print(finishChar, "Solution found:", solutionUnderTest,
          expectedSolutionStr, "\n")


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

    def __str__(self):
        return "✦(y:{0},x:{1})".format(self.y, self.x)

    def __eq__(self, other) -> bool:
        return (self.y == other.y) and (self.x == other.x)

    def __hash__(self):
        return hash((self.x, self.y))


def countUntil(predicate, list) -> int:
    '''Count until predicate returns a false.
Will return at least 1 for non-empty list.'''
    if len(list) < 1:
        return 0
    index = 0
    predicateViolated = False
    while not predicateViolated:
        # if predicate(list[index]):
        #     index += 1
        # else:
        #    predicateViolated = True
        predicateViolated = not predicate(list[index])
        index += 1
    return index


class Grid_int:
    '''An Array of integers indexable by Coordinates.
height: int; width: int; grid: [int] (is flattened 2D array)'''

    def __init__(self, height: int, width: int, grid: [int]):
        assert (width * height) == len(grid),\
            "w:{0} × h:{1} != len(grid):{2}".format(width, height, len(grid))
        self.height = height
        self.width = width
        self.grid = grid

    @classmethod
    def makeGrid(Cls, array2D: [[int]]):
        '''Make an Int2DGrid from a 2D array of int's.'''
        widths = map(lambda a: len(a), array2D)
        widthsSet = set(widths)
        assert len(widthsSet) == 1
        width = widthsSet.pop()
        height = len(array2D)
        flattened = array.array('i')
        for innerList in array2D:
            flattened.extend(innerList)
        assert (width * height) == len(flattened)
        output = Grid_int.__init__(height, width, flattened)
        return output

    def _makeIndex(self, coordinate: Coordinate) -> int:
        '''Flatten a Coordinate into a single int index to subscript into
self.grid with.'''
        index = (coordinate.y * self.width) + coordinate.x
        assert index < len(self.grid)
        return index

    def __getitem__(self, idx):
        if type(idx) is Coordinate:
            return self.grid[self._makeIndex(idx)]
        elif type(idx) is int:
            return self.grid[idx]
        else:
            raise Exception("Invalid index type; expected Coordinate or int,\
            not: {0}.".format(type(idx)))

    def __setitem__(self, idx, newValue: int):
        if type(idx) is Coordinate:
            self.grid[self._makeIndex(idx)] = newValue
        elif type(idx) is int:
            self.grid[idx] = newValue
        else:
            raise Exception("Invalid index type; expected Coordinate or int,\
            not: {0}.".format(type(idx)))

    def __len__(self) -> int:
        return len(self.grid)

    def __str__(self) -> str:
        chunks = list(grouper(self.grid, self.width))
        lines: [str] = list()
        for i in range(0, len(chunks)):
            chunk = chunks[i]
            line = str()
            if i == 0:
                line = '['
            else:
                line = ' ['
            line += ', '.join(map(lambda i: str(i), chunk))
            line += ']'
            lines.append(line)
        output = '[' + ',\n'.join(lines) + ']\n'
        return output

    def allCoordinates(self) -> [Coordinate]:
        '''All valid coordinates of this 2D array.'''
        return [Coordinate(y, x)
                for y in range(0, self.height)
                for x in range(0, self.width)]


def areAllCoordsLessThan(grid_int: Grid_int, coords: [Coordinate],
                         treeHeight: int) -> bool:
    if verbose:
        coordStr = '[' + ','.join(map(lambda c: str(c), coords)) + ']'
        print("λareAllCoordsLessThan treeHeight:", treeHeight, "coords:", coordStr)
    output = True
    for c in coords:
        if grid_int[c] >= treeHeight:
            output = False
            break
    return output


def isVisibleFromOutside(grid_int: Grid_int, coordinate) -> bool:
    # is it on the edge?
    if (coordinate.x == 0) or (coordinate.x == (grid_int.width - 1)):
        return True
    if (coordinate.y == 0) or (coordinate.y == (grid_int.height - 1)):
        return True
    # check heights
    toTopEdgeYrange  = range(0, coordinate.y)
    toTopEdge = list(map(lambda y: Coordinate(y, coordinate.x), toTopEdgeYrange))
    toBotEdgeYrange  = range(coordinate.y + 1, grid_int.height)
    toBotEdge = list(map(lambda y: Coordinate(y, coordinate.x), toBotEdgeYrange))
    toWestEdgeXrange = range(0, coordinate.x)
    toWestEdge = list(map(lambda x: Coordinate(coordinate.y, x), toWestEdgeXrange))
    toEastEdgeXrange = range(coordinate.x + 1, grid_int.width)
    toEastEdge = list(map(lambda x: Coordinate(coordinate.y, x), toEastEdgeXrange))
    edgeGroups = list()
    for eg in [toTopEdge, toBotEdge, toWestEdge, toEastEdge]:
        if len(eg) > 0:
            edgeGroups.append(eg)
    output = False
    for edgeGroup in edgeGroups:
        if areAllCoordsLessThan(grid_int, edgeGroup,
                                grid_int[coordinate]):
            output = True
    return output


def makeGridOfVisible(grid_int: Grid_int) -> [int]:
    """Makes an array (flattened 2d grid) same `len` as grid_int.grid, of
integers.  0 = not visible, 1 = visible interior, 2 = visible because it's on
an edge."""
    grid = list()    # list of array.array('i')
    for y in range(0, grid_int.height):
        row = array.array('i')
        for x in range(0, grid_int.width):
            coord = Coordinate(y, x)
            isVisible = isVisibleFromOutside(grid_int, coord)
            if isVisible:
                if (y == 0) or (y == (grid_int.height - 1)) or \
                   (x == 0) or (x == (grid_int.width - 1)):
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


def prettyPrintColor(grid_int: Grid_int):
    # Escape Sequences
    fgWhite = "\u001B[38;5;7m"
    fgYellow = "\u001B[38;5;3m"
    fgGreen = "\u001B[38;5;2m"
    fgCyan = "\u001B[38;5;6m"
    fgOff = "\u001B[39m"
    bgGray = "\u001B[48;5;240m"
    bgOff = "\u001B[49m"
    bold = "\u001B[1m"
    boldOff = "\u001B[22m"

    def format(treeHeight: int, visibility: int) -> str:
        start = ''
        end = fgOff
        match visibility:
            case 0:  # not visible
                start = bgGray + fgWhite
                end = fgOff + bgOff
            case 1:  # visible
                start = fgYellow
            case 2:  # visible on the edge
                start = fgGreen
        return start + str(treeHeight) + end

    print("---- TREE GRID   w: {0}   h: {1} ----"
          .format(grid_int.width, grid_int.height))

    line1 = "{0}X→{1}            1    1    2    2    3{2}"\
        .format(fgCyan + bold, boldOff, fgOff)
    line2 = "{0}Y↓{1}  0    5    0    5    0    5    0{2}"\
        .format(fgCyan + bold, boldOff, fgOff)
    line3 = "  {0}┌────────────────────────────────{1}".format(fgCyan, fgOff)
    for l in [line1, line2, line3]:
        print(l)

    vGrid = makeGridOfVisible(grid_int)

    lines = list()
    for y in range(0, grid_int.height):
        line = ''
        for x in range (0, grid_int.width):
            coord = Coordinate(y, x)
            idx = grid_int._makeIndex(coord)
            treeheight = grid_int[idx]
            visibility = vGrid[idx]
            output = format(treeheight, visibility)
            line += output
        lines.append(line)

    for y in range(0, len(lines)):
        print('{1}{0:<2}│{2}'.format(y, fgCyan, fgOff), lines[y])

    if verbose:
        for i in range(0, len(vGrid), grid_int.width):
            line = ''.join(map(lambda i: str(i),
                               vGrid[i : i + grid_int.width]))
            print('   ', line)
        print('↑----- vGrid -----↑')


# class TreeGrid:
#     '''height: int; width: int; grid: [int] (is flattened 2D array)'''

#     def __init__(self, height: int, width: int, grid: [int]):
#         assert (width * height) == len(grid)
#         self.height = height
#         self.width = width
#         self.grid = grid

#     def makeIndex(self, coordinate) -> int:
#         '''Flatten a Coordinate into a single int index to subscript into
# self.grid with.'''
#         index = (coordinate.y * self.width) + coordinate.x
#         assert index < len(self.grid)
#         return index

#     def __getitem__(self, coordinate):
#         return self.grid[self.makeIndex(coordinate)]

#     def __setitem__(self, coordinate, newValue):
#         self.grid[self.makeIndex(coordinate)] = newValue

#     def areAllCoordsLessThan(self, coords: [Coordinate], treeHeight: int) -> bool:
#         if verbose:
#             coordStr = '[' + ','.join(map(lambda c: str(c), coords)) + ']'
#             print("λareAllCoordsLessThan treeHeight:", treeHeight, "coords:", coordStr)
#         output = True
#         for c in coords:
#             if self.grid[self.makeIndex(c)] >= treeHeight:
#                 output = False
#                 break
#         return output

#     def isVisibleFromOutside(self, coordinate) -> bool:
#         # is it on the edge?
#         if (coordinate.x == 0) or (coordinate.x == (self.width - 1)):
#             return True
#         if (coordinate.y == 0) or (coordinate.y == (self.height - 1)):
#             return True
#         # check heights
#         toTopEdgeYrange  = range(0, coordinate.y)
#         toTopEdge = list(map(lambda y: Coordinate(y, coordinate.x), toTopEdgeYrange))
#         toBotEdgeYrange  = range(coordinate.y + 1, self.height)
#         toBotEdge = list(map(lambda y: Coordinate(y, coordinate.x), toBotEdgeYrange))
#         toWestEdgeXrange = range(0, coordinate.x)
#         toWestEdge = list(map(lambda x: Coordinate(coordinate.y, x), toWestEdgeXrange))
#         toEastEdgeXrange = range(coordinate.x + 1, self.width)
#         toEastEdge = list(map(lambda x: Coordinate(coordinate.y, x), toEastEdgeXrange))
#         edgeGroups = list()
#         for eg in [toTopEdge, toBotEdge, toWestEdge, toEastEdge]:
#             if len(eg) > 0:
#                 edgeGroups.append(eg)
#         output = False
#         for edgeGroup in edgeGroups:
#             if self.areAllCoordsLessThan(edgeGroup, self.grid[self.makeIndex(coordinate)]):
#                 output = True
#         return output

#     def prettyPrint(self):
#         chunks = list(grouper(self.grid, self.width))
#         print("---- TREE GRID   w: {0}   h: {1} ----"
#               .format(self.width, self.height))

#         line1 = "X→            1    1    2    2    3"
#         line2 = "Y↓  0    5    0    5    0    5    0"
#         line3 = "  ┌────────────────────────────────"
#         maxLength = 5 + self.width
#         lines1to3 = [line1, line2, line3]
#         lines1to3Trimmed = map(lambda l: l[:maxLength], lines1to3)
#         for l in lines1to3Trimmed:
#             print(l)
#         for h in range(0, self.height):
#             chunk = chunks[h]
#             chars = map(lambda n: str(n), chunk)
#             line = ''.join(chars)
#             print("{0:<2}│".format(h), line)

#     def makeGridOfVisible(self) -> [int]:
#         """Makes an array (flattened 2d grid) same `len` as self.grid, of
# integers.  0 = not visible, 1 = visible interior, 2 = visible because it's on an edge
# """
#         grid = list()    # list of array.array('i')
#         for y in range(0, self.height):
#             row = array.array('i')
#             for x in range(0, self.width):
#                 coord = Coordinate(y, x)
#                 isVisible = self.isVisibleFromOutside(coord)
#                 if isVisible:
#                     if (y == 0) or (y == (self.height - 1)) or \
#                        (x == 0) or (x == (self.width - 1)):
#                         row.append(2)
#                     else:
#                         row.append(1)
#                 else:
#                     row.append(0)
#             grid.append(row)
#         flattened = array.array('i')
#         for row in grid:
#             flattened.extend(row)
#         return flattened

#     def prettyPrintColor(self):
#         # Escape Sequences
#         fgWhite = "\u001B[38;5;7m"
#         fgYellow = "\u001B[38;5;3m"
#         fgGreen = "\u001B[38;5;2m"
#         fgCyan = "\u001B[38;5;6m"
#         fgOff = "\u001B[39m"
#         bgGray = "\u001B[48;5;240m"
#         bgOff = "\u001B[49m"
#         bold = "\u001B[1m"
#         boldOff = "\u001B[22m"

#         def format(treeHeight: int, visibility: int) -> str:
#             start = ''
#             end = fgOff
#             match visibility:
#                 case 0:  # not visible
#                     start = bgGray + fgWhite
#                     end = fgOff + bgOff
#                 case 1:  # visible
#                     start = fgYellow
#                 case 2:  # visible on the edge
#                     start = fgGreen
#             return start + str(treeHeight) + end

#         print("---- TREE GRID   w: {0}   h: {1} ----"
#               .format(self.width, self.height))

#         line1 = "{0}X→{1}            1    1    2    2    3{2}"\
#             .format(fgCyan + bold, boldOff, fgOff)
#         line2 = "{0}Y↓{1}  0    5    0    5    0    5    0{2}"\
#             .format(fgCyan + bold, boldOff, fgOff)
#         line3 = "  {0}┌────────────────────────────────{1}".format(fgCyan, fgOff)
#         for l in [line1, line2, line3]:
#             print(l)

#         vGrid = self.makeGridOfVisible()

#         lines = list()
#         for y in range(0, self.height):
#             line = ''
#             for x in range (0, self.width):
#                 coord = Coordinate(y, x)
#                 idx = self.makeIndex(coord)
#                 treeheight = self.grid[idx]
#                 visibility = vGrid[idx]
#                 output = format(treeheight, visibility)
#                 line += output
#             lines.append(line)

#         for y in range(0, len(lines)):
#             print('{1}{0:<2}│{2}'.format(y, fgCyan, fgOff), lines[y])

#         if verbose:
#             for i in range(0, len(vGrid), self.width):
#                 line = ''.join(map(lambda i: str(i), vGrid[i : i + self.width]))
#                 print('   ', line)
#             print('↑----- vGrid -----↑')

#     def scenicScoreForTree(self, treeCoord: Coordinate) -> int:
#         upCoords = [Coordinate(y, treeCoord.x) for y in range(treeCoord.y, -1, -1)]
#         downCoords = [Coordinate(y, treeCoord.x)\
#                       for y in range(treeCoord.y + 1, self.height)]
#         leftCoords = [Coordinate(treeCoord.y, x)\
#                       for x in range(treeCoord.x - 1, -1, -1)]
#         rightCoords = [Coordinate(treeCoord.y, x)\
#                        for x in range(treeCoord.x + 1, self.width)]
#         treeHeight = self.grid[self.makeIndex(treeCoord)]
#         # TODO
#         upCount = countUntil(lambda n: n >= treeHeight,
#                              map(lambda c: self.grid[self.makeIndex(c)], upCoords))

#         # or this way:
#         # upCoords = [Coordinate(y, treeCoord.x) for y in range(treeCoord.y, -1, -1)]
#         # upTrees = map(lambda c: self.grid[self.makeIndex(c)], upCoords)
#         # upcount = countUntil(lambda n: n >= treeHeight, upTrees)
#         # so this would needs it's own function to be broken out and repeated
#         # four times

#         def countOfTreesBelowHeight(coords: [Coordinate], height: int) -> int:
#             '''Goes down list of coords, in order, counting how many trees are
# below given height.'''
#             index = 0
#             hitTreeAtOrGreaterThanHeight = False
#             while (not hitTreeAtOrGreaterThanHeight) and (index < len(coords)):
#                 testCoord = coords[index]
#                 testTreeHeight = self.grid[self.makeIndex(testCoord)]
#                 if testTreeHeight >= height:
#                     hitTreeAtOrGreaterThanHeight = True
#                 index += 1
#             return index

#         upCount = countOfTreesBelowHeight(upCoords, self.grid[self.makeIndex(treeCoord)])
#         downCount = countOfTreesBelowHeight(downCoords, self[treeCoord])
#         leftCount = countOfTreesBelowHeight(leftCoords, self[treeCoord])
#         rightCount = countOfTreesBelowHeight(rightCoords, self[treeCoord])
#         counts = [upCount, downCount, leftCount, rightCount]
#         filterOutZeroes = filter(lambda n: n > 0, counts)
#         scenicScoreForTree = reduce(lambda lhs, rhs: lhs * rhs,
#                                     filterOutZeroes, 1)
#         return scenicScoreForTree

#     def makeGridOfScenicScore(self) -> [int]:
#         '''Make flattened 2D grid of the scenic score for each tree.'''
#         grid = list()
#         for y in range(0, self.height):
#             row = list()
#             for x in range(0, self.width):
#                 coord = Coordinate(y, x)
#                 scenicScore = self.scenicScoreForTree(coord)
#                 row.append(scenicScore)
#             grid.append(row)
#         flattened = array.array('i')
#         for row in grid:
#             flattened.extend(row)
#         return flattened


# def parse(input: str) -> TreeGrid:
#     splitByLine = input.splitlines()
#     trees = list()
#     lineLengths = set()
#     for line in splitByLine:
#         nums = list()
#         lineAsList = list(line)
#         lineLengths.add(len(lineAsList))
#         if len(lineLengths) > 1:
#             print("ERRROR: lineLengths > 1.  length followed by content:", len(lineLengths))
#             print(lineLengths)
#         assert len(lineLengths) == 1
#         for char in lineAsList:
#             newNum = int(char)
#             nums.append(newNum)
#         a = array.array('i')
#         a.fromlist(nums)
#         trees.append(a)
#     width = lineLengths.pop()
#     height = len(trees)
#     assert height == len(splitByLine)
#     flattenTrees = array.array('i')
#     for arr in trees:
#         flattenTrees.extend(arr)
#     return TreeGrid(height, width, flattenTrees)


def parse(input: str) -> Grid_int:
    splitByLine = input.splitlines()
    trees = list()
    lineLengths = set()
    for line in splitByLine:
        nums = list()
        lineAsList = list(line)
        lineLengths.add(len(lineAsList))
        if len(lineLengths) > 1:
            print("ERRROR: lineLengths > 1.  length followed by content:",
                  len(lineLengths))
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
    return Grid_int(height, width, flattenTrees)


def solve(input: str, part=1) -> int:
    treeGrid = parse(input)
    # treeGrid.prettyPrint()
    if verbose:
        print()
        prettyPrintColor(treeGrid)
        print("---------------")

    if part == 1:
        gridOfVisible = makeGridOfVisible(treeGrid)
        visibleCount = 0
        for v in gridOfVisible:
            if v > 0:
                visibleCount += 1
        return visibleCount
    elif part == 2:
        pass


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=21)
run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
