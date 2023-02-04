# Advent of Code 2022 Day 07

from itertools import repeat
from functools import reduce

# protocol FSNode
#   var name: String { get }
#   var size: Int { get }


class File:
    def __init__(self, name: str, size: int):
        self.name = name
        self.size = size

    def getSize(self) -> int:
        return self.size


class Directory:
    def __init__(self, name: str):
        self.name = name
        self.contents = list()
        self.parent = None

    def getSize(self) -> int:
        output = 0
        for fsnode in self.contents:
            output += fsnode.getSize()
        return output

    def add(self, newNode):
        # if newNode is Directory:
        #     newNode.parent = self
        #  above just checks identity
        if type(newNode) is Directory:
            newNode.parent = self
        self.contents.append(newNode)

    def prettyPrint(self, indentLevel: int = 0):
        indent = ''.join(repeat(' ', 4 * indentLevel))
        endslash = '/'
        if self.name == '/':
            endslash = ''
        size = str(self.getSize())
        print(indent, self.name, endslash, '\t', size)
        # sortedContents = self.contents.copy()
        # sortedContents.sort()
        sortedContents = sorted(self.contents, key=lambda node: node.name)
        for fsnode in sortedContents:
            if type(fsnode) is Directory:
                fsnode.prettyPrint(indentLevel + 1)
            if type(fsnode) is File:
                print(indent, '    ', fsnode.name, '\t', str(fsnode.getSize()))


def getDirectoriesUnder100000(rootDir: Directory):
    output = list()
    if rootDir.getSize() < 100000:
        output.append(rootDir)
    for node in rootDir.contents:
        if type(node) is Directory:
            output += getDirectoriesUnder100000(node)
    return output


def parse(input: str) -> Directory:
    splitByLine = input.splitlines()
    root = Directory("/")
    pwd: Directory = root
    for line in splitByLine:
        splitBySpace = line.split()
        match splitBySpace[0]:
            case "$":
                match splitBySpace[1]:
                    case "cd":
                        match splitBySpace[2]:
                            case "/":
                                pwd = root
                            case "..":
                                if not pwd.parent:
                                    print("No parent.  pwd:", pwd.name)
                                    print("line:", line)
                                pwd = pwd.parent
                            case _:
                                for fd in pwd.contents:
                                    if fd.name == splitBySpace[2]:
                                        pwd = fd
                                        break
                    case "ls":
                        continue
            case "dir":
                newDir = Directory(splitBySpace[1])
                pwd.add(newDir)
            case _:
                newFile = File(splitBySpace[1], int(splitBySpace[0]))
                pwd.add(newFile)
    return root


class InputProvider:
    EXAMPLE = 0
    FILE = 1
    EXAMPLE_STRING = """$ cd /
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

    def getInput(source: int) -> str:
        match source:
            case InputProvider.EXAMPLE:
                return InputProvider.EXAMPLE_STRING
            case InputProvider.FILE:
                file = open("input.txt")
                contents = file.read()
                return contents
            case _:
                raise Exception("Bad parameter.")


def getDirectoriesAtLeast(rootDir: Directory, spaceToFreeUp: int):
    output = list()
    if rootDir.getSize() >= spaceToFreeUp:
        output.append(rootDir)
    for node in rootDir.contents:
        if type(node) is Directory:
            output += getDirectoriesAtLeast(node, spaceToFreeUp)
    return output


def solve(input: str, part: int = 1) -> int:
    root = parse(input)
    if part == 1:
        print("--------------------- Finished parsing input. ------------------")
        dirsUnder100k = getDirectoriesUnder100000(root)
        print("Directories < 100k:")
        for d in dirsUnder100k:
            print("    {0:>8}  {1}".format(d.getSize(), d.name))
        dirsUnder100kSizes = map(lambda x: x.getSize(), dirsUnder100k)
        sumDirsUnder100k = reduce(lambda lhs, rhs: lhs+rhs,
                                  dirsUnder100kSizes)
        return sumDirsUnder100k
    elif part == 2:
        diskSpaceTotal = 70000000
        updateSpaceNeeded = 30000000
        spaceCurrentlyFree = diskSpaceTotal - root.getSize()
        spaceToFreeUp = updateSpaceNeeded - spaceCurrentlyFree
        print("--------------------- Finished parsing input. ------------------")
        print("free space (total disk space - root.getSize()):", spaceCurrentlyFree)
        print("space to free up (updateSpaceNeeded - free space):", spaceToFreeUp)
        dirsAtLeastX = getDirectoriesAtLeast(root, spaceToFreeUp)
        print("Directories at least {0}:".format(spaceToFreeUp))
        for d in dirsAtLeastX:
            print("    {0:>8}  {1}".format(d.getSize(), d.name))
        minDir = min(dirsAtLeastX, key=Directory.getSize)
        minDirSize = minDir.getSize()
        print("The minumum directory is", minDir.name, "at size:", minDirSize)
        # dirsAtLeastXSizes = map(lambda x: x.getSize(), dirsAtLeastX)
        # sumDirs = reduce(lambda lhs, rhs: lhs+rhs, dirsAtLeastXSizes)
        return minDirSize


def run(input: str, part: int = 1, expectedSolution=()):
    foundSolution = solve(input, part)
    solvedIcon = '🏁'
    expectedSolutionString = ''
    if expectedSolution:
        expectedSolutionString = '      Expected: ' + str(expectedSolution)
        if foundSolution == expectedSolution:
            solvedIcon = '👍'
        else:
            solvedIcon = '❌'
    print(solvedIcon, "answer:", foundSolution, expectedSolutionString)


# run(InputProvider.getInput(InputProvider.EXAMPLE), 1, 95437)
# run(InputProvider.getInput(InputProvider.FILE), 1, 1770595)
# run(InputProvider.getInput(InputProvider.EXAMPLE), 2, 24933642)
run(InputProvider.getInput(InputProvider.FILE), 2)
