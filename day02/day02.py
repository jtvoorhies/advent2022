# Advent of Code Day 2: Rock Paper Scissors

import re
from enum import Enum, auto


verbose = False


lineParser = re.compile('([ABC]) ([XYZ])')


class Rps(Enum):
    '''The choice to make in each round of this game.'''
    ROCK = auto()
    PAPER = auto()
    SCISSORS = auto()

    def pointValue(self) -> int:
        match self:
            case Rps.ROCK: return 1
            case Rps.PAPER: return 2
            case Rps.SCISSORS: return 3


class Outcome(Enum):
    '''The 3 possible outcomes of Rock Paper Scissors'''
    WIN = auto()
    LOSE = auto()
    TIE = auto()

    def pointValue(self) -> int:
        match self:
            case Outcome.WIN: return 6
            case Outcome.LOSE: return 0
            case Outcome.TIE: return 3


def lineToPoints(line: str) -> int:
    '''Takes line of puzzle input and determines points awarded to me.'''
    playMatcher = lineParser.search(line)
    if verbose:
        print("lineToPointsλ type(lineParser):", type(lineParser),
              " type(playMatcher):", type(playMatcher))
    opPlayCh = playMatcher.group(1)
    myPlayCh = playMatcher.group(2)
    opPlay: Rps
    myPlay: Rps
    match opPlayCh:
        case "A": opPlay = Rps.ROCK
        case "B": opPlay = Rps.PAPER
        case "C": opPlay = Rps.SCISSORS
    match myPlayCh:
        case "X": myPlay = Rps.ROCK
        case "Y": myPlay = Rps.PAPER
        case "Z": myPlay = Rps.SCISSORS
    outcome: Outcome
    match opPlay.pointValue() - myPlay.pointValue():
        case -2: outcome = Outcome.LOSE
        case -1: outcome = Outcome.WIN
        case 0: outcome = Outcome.TIE
        case 1: outcome = Outcome.LOSE
        case 2: outcome = Outcome.WIN
    myPointsEarned = outcome.pointValue() + myPlay.pointValue()
    if verbose:
        print("lineToPointsλ opPlay:", opPlay, " myPlay:", myPlay,
              " outcome:", outcome)
        print("    myPointsEarned:", myPointsEarned)
    return myPointsEarned


def playAgainstForOutcome(opPlay: Rps, outcome: Outcome) -> Rps:
    match outcome:
        case Outcome.WIN:
            match opPlay:
                case Rps.ROCK:
                    return Rps.PAPER
                case Rps.PAPER:
                    return Rps.SCISSORS
                case Rps.SCISSORS:
                    return Rps.ROCK
        case Outcome.LOSE:
            match opPlay:
                case Rps.ROCK:
                    return Rps.SCISSORS
                case Rps.PAPER:
                    return Rps.ROCK
                case Rps.SCISSORS:
                    return Rps.PAPER
        case Outcome.TIE:
            return opPlay


def lineToPointsPart2(line: str) -> int:
    playMatcher = lineParser.search(line)
    opPlayCh = playMatcher.group(1)
    myOutcomeCh = playMatcher.group(2)
    opPlay: Rps
    myOutcome: Rps
    match opPlayCh:
        case "A": opPlay = Rps.ROCK
        case "B": opPlay = Rps.PAPER
        case "C": opPlay = Rps.SCISSORS
    match myOutcomeCh:
        case "X": myOutcome = Outcome.LOSE
        case "Y": myOutcome = Outcome.TIE
        case "Z": myOutcome = Outcome.WIN
    myPlay: Rps = playAgainstForOutcome(opPlay, myOutcome)
    myPointsEarned = myOutcome.pointValue() + myPlay.pointValue()
    if verbose:
        print("lineToPointsPart2λ opPlay:", opPlay, " myOutcome:", myOutcome,
              " myPlay:", myPlay)
        print("    myPointsEarned:", myPointsEarned)
    return myPointsEarned


class InputProvider(Enum):
    EXAMPLE = auto()
    FILE = auto()

    def getInput(self) -> str:
        match self:
            case InputProvider.EXAMPLE: return '''\
A Y
B X
C Z
'''
            case InputProvider.FILE:
                file = open("input.txt")
                return file.read()


def run(inputProvider: InputProvider, part=1, expectedSolution=()):
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


def solve(input: str, part: int) -> int:
    myPoints = 0
    splitByLine = input.splitlines()
    for line in splitByLine:
        pointsForLine: int
        if part == 1:
            pointsForLine = lineToPoints(line)
        elif part == 2:
            pointsForLine = lineToPointsPart2(line)
        myPoints += pointsForLine
        if verbose:
            print("solveλ line:", line, "  points:", pointsForLine,
                  "current total:", myPoints)
    return myPoints


run(InputProvider.EXAMPLE, part=1, expectedSolution=15)
run(InputProvider.FILE, part=1)
run(InputProvider.EXAMPLE, part=2, expectedSolution=12)
run(InputProvider.FILE, part=2)
