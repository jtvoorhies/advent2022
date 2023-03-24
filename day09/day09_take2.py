# Advent of Code

from enum import Enum, auto

# global variable to make functions more chatty for debugging
verbose = True


class InputProvider(Enum):
    """The function getInput() is the star here, giving you the input string to
    work with."""
    EXAMPLE = auto()
    EXAMPLE2 = auto()
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
            case InputProvider.EXAMPLE2:
                return """\
R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
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



class Distance:

    def __init__(self, dy: int, dx: int):
        self.dy = dy
        self.dx = dx

    def __eq__(self, other) -> bool:
        if self.dy == other.dy:
            return self.dx == other.dx
        else:
            return False

    def __ne__(self, other) -> bool:
        if self.dy != other.dy:
            return True
        else:
            return self.dx != other.dx

    def __str__(self) -> str:
        return '↕{0},↔{1}'.format(self.dy, self.dx)

    @classmethod
    def makeZero(cls):
        return Distance(0, 0)


class Coordinate:

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __eq__(self, other) -> bool:
        if self.y == other.y:
            return self.x == other.x
        else:
            return False

    def __ne__(self, other) -> bool:
        if self.y != self.y:
            return True
        else:
            return self.x != other.x

    def __str__(self) -> str:
        return "✦(y:{0},x:{1})".format(self.y, self.x)

    def __hash__(self):
        return hash((self.y, self.x))

    def move(self, distance: Distance):
        self.y += distance.dy
        self.x += distance.dx

    def distanceTo(self, other) -> Distance:
        return Distance(other.y - self.y,
                        other.x - self.x)

    @classmethod
    def makeZero(cls):
        return Coordinate(0, 0)


class Movement:

    def __init__(self, direction: str, count: int):
        self.direction = direction
        self.count = count

    def neighborTransform(self) -> Distance:
        match self.direction:
            case 'U':
                return Distance(1, 0)
            case 'D':
                return Distance(-1, 0)
            case 'L':
                return Distance(0, -1)
            case 'R':
                return Distance(0, 1)
            case _:
                raise Exception("Unreachable.  direction: {0}"
                                .format(self.direction))

    @classmethod
    def makeMovement(cls, line: str):
        splitBySpace = line.split()
        assert len(splitBySpace) == 2
        direction = splitBySpace[0]
        count = int(splitBySpace[1])  # will raise exception if not integer
        assert direction in ["U", "D", "L", "R"]
        return Movement(direction, count)


def updateTail(head, tail) -> Distance:
    distance = tail.distanceTo(head)
    if abs(distance.dy) < 2 and abs(distance.dx) < 2:
        return Distance.makeZero()
    newDy = 0
    newDx = 0
    if distance.dy > 0:
        newDy = 1
    if distance.dy < 0:
        newDy = -1
    if distance.dx > 0:
        newDx = 1
    if distance.dx < 0:
        newDx = -1
    return Distance(newDy, newDx)


def solvePart1(input: str) -> int:
    head = Coordinate.makeZero()
    tail = Coordinate.makeZero()
    tailVisits = {Coordinate.makeZero()}

    for line in input.splitlines():
        movement = Movement.makeMovement(line)
        neighborTransform = movement.neighborTransform()
        distanceRemaining = movement.count
        while distanceRemaining > 0:
            head.move(neighborTransform)
            tailMove = updateTail(head, tail)
            if tailMove != Distance.makeZero():
                tail.move(tailMove)
                tailVisits.add(tail)
            if verbose:
                print('H:{0: >2},{1: >2}  T:{2: >2},{3: >2}'\
                      .format(head.y, head.x, tail.y, tail.x))
            distanceRemaining -= 1
    return len(tailVisits)


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=13)
# run(InputProvider.INPUTFILE, part=1, expectedSolution=6018)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=1)
# run(InputProvider.EXAMPLE2, part=2, expectedSolution=36)
# run(InputProvider.INPUTFILE, part=2, expectedSolution=2619)
