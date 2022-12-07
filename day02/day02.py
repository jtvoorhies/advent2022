# Advent of Code Day 2: Rock Paper Scissors

import re
from enum import Enum, auto


lineParser = re.compile("\([ABC]\) \([XYZ]\)")

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


def lineToPointsa(line: str) -> inn:
    '''Take a single line of puzzle input and determine amount awarded to me.'''
    playMatcher = lineParser.search(line)
    opPlayCh, myPlayCh = playMatcher.group(1), playMatcher.group(2)
    # opPlay, myPlay = pass, pass
    opPlay = Error
    match opPlayCh:
        case "A": opPlay = Rps.ROCK
        case "B": opPlay = Rps.PAPER
        case "C": opPlay = Rps.SCISSORS
    match myPlayCh:
        case "X": myPlay = Rps.ROCK
        case "Y": myPlay = Rps.PAPER
        case "Z": myPlay = Rps.SCISSORS
