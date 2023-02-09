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

    # def eq(lhs, rhs) -> bool:
    #     return (lhs.x == rhs.x) and (lhs.y == rhs.y)

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
        self.x += transformer.x
        self.y += transformer.y


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
            # check if tail needs move
            # if not head.isTouching(tail):
            # dy = head.y - tail.y
            # dx = head.x - tail.x
            # tailTransform = None    # Coordinate

            # if (abs(dx) > 1) or (abs(dy) > 1):  # need to move tail
            #     match (dy, dx):
            #         case (diffy, 0) if diffy < -1:    # same column, diff rows
            #             tailTransform = Coordinate(+1, 0)
            #         case (diffy, 0) if diffy > 1:
            #             tailTransform = Coordinate(-1, 0)
            #         case (0, diffx) if diffx < -1:
            #             tailTransform = Coordinate(0, 1)
            #         case (0, diffx) if diffx > 1:
            #             tailTransform = Coordinate(0, -1)
            #         case [(-2, -1),  (-1, -2), (-2, -2)]:
            #             tailTransform = Coordinate(1, 1)
            #         case [(-2, 1),  (-1, 2), (-2, 2)]:
            #             tailTransform = Coordinate(1, -1)
            #         case [(2, -1),  (1, -2), (2, -2)]:
            #             tailTransform = Coordinate(-1, 1)
            #         case [(2, 1),  (1, 2), (2, 2)]:
            #             tailTransform = Coordinate(-1, -1)
            #         case (0, 0):                        # overlap
            #             pass
            #         case _:
            #             print("ERROR.  Should be unreachable.  dy:{0}, dx:{1}"
            #                   .format(dy, dx))

            diff = Coordinate(head.y - tail.y, head.x - tail.x)
            y: int
            x: int

            # TODO
            # Bug is that if diif doesn't have a zero in either x or y then
            # tail needs to move a diagonal.  But diff must have an x or y of
            # absolute value greater than 1.
            #
            # if (abs(diff.x) > 1) … we move horizontal
            # or (abs(diff.y) > 1) … we move vertical
            # if (diff.x == 0) or (diff.y == 0):
            #     pass
            # else:
            #     # move diagonal
            # if diff.y < -1:
            #     y = -1
            # elif diff.y > 1:
            #     y = 1
            # else:
            #     y = 0
            # if diff.x < -1:
            #     x = -1
            # elif diff.x > 1:
            #     x = 1
            # else:
            #     x = 0
            # tailTransform: Coordinate
            # if (y == 0) and (x == 0):
            #     tailTransform = None
            # else:
            #     tailTransform = Coordinate(y, x)

            # move tail and if tail move, add new coordinate to the set

            match (abs(diff.y), abs(diff.x)):
                case (2, _):
                case (_, 2):

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
