# Advent of Code
# day07

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
                return '''\
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
'''
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


def addDirectory(name: str, root: dict, pwd: [str]):
    cwd = root
    if len(pwd) > 0:
        for idx in range(0, len(pwd)):
            cwd = cwd[pwd[idx]]
    cwd.setdefault[name] = list()

def addFile(name: str, size: int, root: dict, pwd: [str]):
    cwd = root
    if len(pwd) > 0:
        for idx in range(0, len(pwd)):
            cwd = cwd[pwd[idx]]
    cwd.setdefault[name] = size


def parse(input: str) -> dict:
    splitByLine = input.splitlines()
    root = dict()
    # pwd is a list of the hierarchy where the unseen -1 item is root ('/').
    # The last item is the name of the pwd; empty means it's root.
    pwd = []
    # if we're in a list
    inListing = False
    for line in splitByLine:
        words = line.split()
        if words[0] == '$':
            inListing = False
            if words[1] == "cd":
                if words[2] == "/":
                    pwd = ['/']
                else if words[2] == "..":
                    pwd.pop()
                else:
                    pwd.append(words[2])
                if verbose:
                    print('pwd:', pwd)
            else if words[1] == "ls":
                inListing = True
                continue
        else if words[0] = "dir":
            addDirectory(words[1], root, pwd)
        else:
            size = int(words[0])
            if size:
                addFile(words[1], size, root, pwd)
            else:
                raise Exception("line not processed:" + line)
    return root


def makeIndent(level: int) -> str:
    indent = '    '
    if level == 0:
        return ''
    else:
        indents = []
        for _ in range(0, level):
            indents.append(indent)
        return ''.join(indents)

def prettyPrint(root: dict):
    indentLevel = 0
    print('/')
    for k in root.keys:

            


def solve(input, part=1) -> int:



# TODO: fill in example solution
run(InputProvider.EXAMPLE, part=1, expectedSolution=95437)
# run(InputProvider.INPUTFILE, part=1)
# run(InputProvider.EXAMPLE, part=2, expectedSolution=)
# run(InputProvider.INPUTFILE, part=2)
