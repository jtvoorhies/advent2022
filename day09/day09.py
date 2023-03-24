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
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2
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


# Rules
# Tail must be adjacent or overlapping head.
# If head and tail are two steps away in cardinal 4 directions, tail moves one
# step in that direction.
# If head and tail are not touching and are not in same row or column, tail
# always move diagnally to keep up.
#
# Count up coordinates tail visits at least once.


class Direction(Enum):
    UP = "U"
    DOWN = "D"
    LEFT = "L"
    RIGHT = "R"

    def neighborTransform(self):
        match self:
            case Direction.UP:
                return Coordinate(-1, 0)
            case Direction.DOWN:
                return Coordinate(+1, 0)
            case Direction.LEFT:
                return Coordinate(0, -1)
            case Direction.RIGHT:
                return Coordinate(0, +1)

    @classmethod
    def makeDirectionFromString(cls, s: str):
        match s:
            case "U":
                return Direction.UP
            case "D":
                return Direction.DOWN
            case "L":
                return Direction.LEFT
            case "R":
                return Direction.RIGHT
            case _:
                return None


class Motion:
    def __init__(self, direction: Direction, steps: int):
        self.direction = direction
        self.steps = steps

    def __str__(self) -> str:
        return "{0}⋆{1}".format(self.direction, self.steps)


class Coordinate:
    '''y for row, x for column.'''

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __str__(self) -> str:
        return "✦(y:{0},x:{1})".format(self.y, self.x)

    def __eq__(self, other) -> bool:
        return (self.x == other.x) and (self.y == other.y)

    def __hash__(self):
        return hash((self.y, self.x))

    def moveInDirection(self, direction: Direction):
        match direction:
            case Direction.UP:
                self.y -= 1
            case Direction.DOWN:
                self.y += 1
            case Direction.RIGHT:
                self.x += 1
            case Direction.LEFT:
                self.x -= 1

    def isTouching(self, other) -> bool:
        '''Determines if this coordinate is "touching" another.
Touching being adjacent (including diagonals) or overlap.'''
        dy = abs(self.y - other.y)
        dx = abs(self.x - other.x)
        if (dx <= 1) and (dy <= 1):
            return True
        else:
            return False

    def transform(self, transformer):
        '''Use another coordinate where y and x are the distances.'''
        if type(transformer) is Coordinate:
            self.x += transformer.x
            self.y += transformer.y
        elif type(transformer) is Distance:
            self.x += transformer.dx
            self.y += transformer.dy


class Distance:

    def __init__(self, dy: int, dx: int):
        self.dy = dy
        self.dx = dx

    def manhattanDistance(self) -> int:
        return abs(dy) + abs(dx)

    def __str__(self):
        return "⇅⇆(dy:{0},dx:{1})".format(self.dy, self.dx)

    def __neg__(self):
        return Distance(-self.dy, -self.dx)

    @classmethod
    def makeDistance(cls, lhsCoord: Coordinate, rhsCoord: Coordinate):
        dy = lhsCoord.y - rhsCoord.y
        dx = lhsCoord.x - rhsCoord.x
        return Distance(dy, dx)


def parse(input: str) -> [Motion]:
    '''Parse puzzle input and return a list of Motions.'''
    splitByLine = input.splitlines()
    output = list()
    for line in splitByLine:
        splitOnWhitespace = line.split()
        direction = Direction.makeDirectionFromString(splitOnWhitespace[0])
        steps = int(splitOnWhitespace[1])
        if (not direction) or (not steps):
            raise Exception("Error encountred.  Could not make direction or\
            steps with line: {0}".format(line))
        newMotion = Motion(direction, steps)
        output.append(newMotion)
    return output


def solve(input, part=1) -> int:
    motions = parse(input)
    head = Coordinate(0, 0)
    tail = Coordinate(0, 0)
    coordinatesVisitedByTail: set = {Coordinate(0, 0)}
    for motion in motions:
        if verbose:
            print("Executing Motion:", motion)
        stepsLeftInCurrentMotion = motion.steps
        while stepsLeftInCurrentMotion > 0:
            # move head
            head.moveInDirection(motion.direction)
            tailDistance = Distance.makeDistance(head, tail)
            if verbose:
                print("tailDistance:", tailDistance)
            # we move at all
            dy = tailDistance.dy
            dx = tailDistance.dx
            tailTransformDy: int
            tailTransformDx: int
            tailTransform: Distance
            if (dy > 1) or (dx > 1):
                # we move in straight line or diagonal
                if dy == 0:                         # straight line horiz
                    tailTransformDy = 0
                    if dx < 0:
                        tailTransformDx = -1
                    elif dx > 0:
                        tailTransformDx = 1
                elif dx == 0:                       # straight line vert
                    tailTransformDx = 0
                    if dy < 0:
                        tailTransformDy = -1
                    elif dy > 0:
                        tailTransformDy = 1
                else:                               # we move diagonal
                    if dx < 0:
                        tailTransformDx = -1
                    else:     # dx > 0:
                        tailTransformDx = 1
                    if dy < 0:
                        tailTransformDy = -1
                    else:    # dy > 0:
                        tailTransformDy = 1
                tailTransform = Distance(tailTransformDy, tailTransformDx)
            else:
                tailTransform = None

            if tailTransform:       # tailTransform is not 'None'
                tail.transform(tailTransform)
                coordinatesVisitedByTail.add(tail)
            stepsLeftInCurrentMotion -= 1
            if verbose:
                tailString = str(tail)
                if tailTransform:
                    tailString = "\u001B[38;5;11m" + tailString + "\u001B[39m"\
                        + "[tform:" + str(tailTransform) + "]"
                print("H:{0} T:{1}  stepsRemaining:{2}  coordsVisitedByTail:{3}"
                      .format(head, tailString, stepsLeftInCurrentMotion,
                              len(coordinatesVisitedByTail)))
    return len(coordinatesVisitedByTail)


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=13)
# run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
