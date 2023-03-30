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
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
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



class Monkey:
    def __init__(self, id: int, items: [int], operation, ifDivisibleBy: int,
                 ifTestTrue: int, ifTestFalse: int):
        self.id = id
        self.items = items
        self.operation = operation
        self.ifDivisibleBy = ifDivisibleBy
        self.ifTestTrue = ifTestTrue
        self.ifTestFalse = ifTestFalse

    def relief(worry: int) -> int:
        # floor division returns an int
        return worry // 3


def parseMonkey(input: str) -> Monkey:
    # matchMonkeyId = re.compile("^Monkey ([0-9]+):")
    # matchItems = re.compile("^\s+Starting items: ([0-9]+(, )?)*")
    # matchOperation = re.compile("^\s+Operation: new = old ([+*]) ([0-9old]+)")
    # matchIfDivisibleBy = re.compile("^\s+Test: divisible by ([0-9]+)")
    # matchIfTestTrue = re.compile("^\s+If true: throw to monkey ([0-9]+)")
    # matchIfTestFalse = re.compile("^\s+If false: throw to monkey ([0-9]+)")
    # id = matchMonkeyId.search(input)
    # items = matchItems.search(input)
    # operation = matchItems.search(input)
    # ifDivisibleBy = matchIfDivisiFalse.search(input)
    # ifTestTrue = matchIfTestTrue.search(input)
    # ifTestFalse = matchIfTestFalse.search(input)
    monkeyMatch = re.compile("""
Monkey (?P<id>[0-9]+):
  Starting items: (?P<itemsList>[0-9, ]+)
  Operation: new = old (?P<opOperator>[+*]) (?P=<opValue>([0-9]+|old))
  Test: divisible by (?P<ifDivisibleBy>[0-9]+)
    If true: throw to monkey (?P<ifTestTrue>[0-9]+)
    If false: throw to monkey (?P<ifTestFalse>[0-9]+)
""")


def parse(input: str) -> [Monkey]:
    pass


def solve(input, part=1) -> int:
    # TODO Write solution
    pass


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=10605)
run(InputProvider.INPUTFILE, part=1, expectedSolution=95472)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
