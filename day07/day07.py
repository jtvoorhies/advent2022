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
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
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


# Directories are just their name which is a dictionary key.
# The value is a list containing the contents
# Thus, root is '{ "/" : [files] }'
# Files are their name followed by their size: '{ "filename" : 1234 }'
# hmmm… so much easier with Swift enums / tagged union

def findDir(name: str, withRoot: dict) -> dict:
    if name in withRoot:
        return withRoot[name]
    else:
        pass


class File:

    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size


def repeatStr(s: str, count: int) -> str:
    output = ''
    for _ in range(0, count):
        output += s
    return output


class Directory:

    def __init__(self, name: str, contents: [File | Directory]):
        self.name = name
        self.contents = contents

    def sumSize(self) -> int:
        sum = 0
        for f in self.contents:
            if f is File:
                sum += f.size
            if f is Directory:
                sum += f.sumSize()
        return sum

    INDENT_STEP_SIZE = 4

    def prettyPrint(self, baseIdentation: int = 0):
        print(repeatStr(" ", baseIdentation * INDENT_STEP_SIZE) + self.name + '/')
        for f in self.contents:
            if f is File:
                print(repeatStr(" ", (baseIdentation + 1) * INDENT_STEP_SIZE)
                      + f.name + '\t' + f.size)
            if f is Directory:
                f.prettyPrint(baseIdentation + 1)


def solve(input, part=1) -> int:
    root = Directory("/")
    splitByLine = input.splitlines()
    pwd: Directory
    for line in splitByLine:
        splitBySpace = line.split()
        if splitBySpace[0] == "$":
            if splitBySpace[1] == "cd":
                match splitBySpace[2]:
                    case "/":
                        pwd = root
                    case "..":
                        # weakref to parent
                        # pwd =
            else if splitBySpace[1] == "ls":
                continue
        else if splitBySpace[0] = "dir":
            newDirectory = Directory(splitBySpace[1])
            pwd.contents.append(newDirectory)


# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=95437)
# run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
