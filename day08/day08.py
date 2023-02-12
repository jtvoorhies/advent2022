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

    def __iadd__(self, other):
        # self.y += other.y
        # self.x += other.x
        newCoord = Coordinate(self.y + other.y, self.x + other.x)
        return newCoord

    def __add__(lhs, rhs):
        return Coordinate(lhs.y + rhs.y, lhs.x + rhs.x)

    def __str__(self):
        return "✦(y:{0},x:{1})".format(self.y, self.x)

    def __eq__(self, other) -> bool:
        return (self.y == other.y) and (self.x == other.x)

    def __hash__(self):
        return hash((self.x, self.y))


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

    def isCoordInBounds(self, coord: Coordinate) -> bool:
        yValueOK = (coord.y < self.height) and (coord.y >= 0)
        xValueOK = (coord.x < self.width)  and (coord.x >= 0)
        return yValueOK and xValueOK

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
            # line += ', '.join(map(lambda i: str(i), chunk))
            line += ', '.join(map(lambda i: "{0:>2}".format(i), chunk))
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


def pprintList(alist) -> str:
    listToStrings = list(map(lambda x: str(x), alist))
    output = '[' + ', '.join(listToStrings) + ']'
    return output

def calculateScenicScoreOfTreeAt(trees: Grid_int, treeCoord: Coordinate) -> int:

    class CoordGeneration:
        '''Generates coordinates going away from the startingCoord in the indicated Direction.
Stops when coord goes beyound bounds of trees.'''

        def __init__(self, startingCoord: Coordinate, direction: Direction):
            self.currentCoord = startingCoord
            self.direction = direction
            # if verbose:
            #     print("New Instance of CoordGeneration Made.  startingCoord:{0}, direction:{1}"
            #           .format(startingCoord, direction))

        def __next__(self):
            # self.currentCord = self.currentCoord + self.direction.neighborTransform()
            # self.currentCoord += self.direction.neighborTransform()
            transform = Direction.neighborTransform(self.direction)
            if verbose:
                # print("__next__ transform:", transform, "    type:", type(transform))
                print("self.currentCoord:", self.currentCoord, end=' ❙ ')
            self.currentCoord += transform
            if verbose:
                print("self.currentCoord:", self.currentCoord, "◀◀◀◀ after mutation")
            if trees.isCoordInBounds(self.currentCoord):
                return self.currentCoord
            else:
                if verbose:
                    print("💣StopIteration raised.")
                raise StopIteration()

        def __iter__(self):
            return self

    class BigTreeFound(Exception):
       def __init__(self, coord: Coordinate, height: int):
            self.coord = coord
            self.height = height

    treeHeight = trees[treeCoord]

    if verbose:
        print("✯✯✯✯✯✯ calculateScenicScoreOfTreeAt coord:{0}   which has height: {1}  ✯✯✯✯✯✯"
              .format(treeCoord, treeHeight))

    scoreMapping = dict()
    for direction in list(Direction):
        treeCount = 0
        generator = iter(CoordGeneration(treeCoord, direction))
        if verbose:
            print("    Direction: {0} --- treeCoord: {1}".format(str(direction), treeCoord))
        try:
            while True:
                nextCoord = next(generator)
                treeCount += 1
                nextHeight = trees[nextCoord]
                if verbose:
                    print("        nextCoord:{0}   nextHeight:{1} treeCount:{2}"
                          .format(nextCoord, nextHeight, treeCount))
                if nextHeight >= treeHeight:
                    raise BigTreeFound(nextCoord, nextHeight)
        except (StopIteration, BigTreeFound):
            scoreMapping[direction] = treeCount
            if verbose:
                print("    end of direction {0} ---".format(str(direction)))

    if verbose:
        #print("    calculateScoreOfTreeAt:", treeCoord, "  it's height:", treeHeight)
        for d in list(Direction):
            print("    {0}: {1}".format(str(d), str(scoreMapping[d])))

    # Mistake! Don't remove zero
    # values = filter(lambda n: n > 0, scoreMapping.values())
    # reduction = reduce(lambda lhs, rhs: lhs * rhs, values, 1)
    reduction = reduce(lambda lhs, rhs: lhs * rhs, scoreMapping.values(), 1)

    return reduction
                

def solve(input: str, part=1) -> int:
    treeGrid = parse(input)

    if part == 1:
        if verbose:
            print()
            prettyPrintColor(treeGrid)
            print("---------------")
        gridOfVisible = makeGridOfVisible(treeGrid)
        visibleCount = 0
        for v in gridOfVisible:
            if v > 0:
                visibleCount += 1
        return visibleCount
    elif part == 2:
        scoresMap = map(lambda c: calculateScenicScoreOfTreeAt(treeGrid, c),
                     treeGrid.allCoordinates())
        scores = array.array('i')
        scores.fromlist(list(scoresMap))
        scoreGrid = Grid_int(treeGrid.height, treeGrid.width, scores)
        print("----- scoreGrid: ------")
        print(str(scoreGrid))
        solution = max(scoreGrid.grid)
        return solution


# TODO: fill in example solution
# run(InputProvider.EXAMPLE, part=1, expectedSolution=21)
# run(InputProvider.INPUTFILE, part=1)
run(InputProvider.EXAMPLE, part=2, expectedSolution=8)
run(InputProvider.INPUTFILE, part=2)
