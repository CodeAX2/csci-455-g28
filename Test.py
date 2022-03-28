from cgitb import reset
from RobotDialog import *

defMap = {
    "test": "This is a string",
    "listTest": ["Good", "Bad", "Fantastic"]
}

varMap = {}


baseBranches = []
d1 = DialogBranch(["say", "test"], ["okay", "~test"], {})

d2 = DialogBranch(["my", "name", "is", "$1"], ["hello", "$1"], {"name": "1"})

d3 = DialogBranch(["how", "are", "you"], ["i", "am", "~listTest"], {})
d2.addChildBranch(d3)

d4 = DialogBranch(["what", "are", "you"], ["i", "am", "a", "robot"], {})
d2.addChildBranch(d4)


baseBranches.append(d1)
baseBranches.append(d2)

tree = Dialog(defMap, varMap, baseBranches)


while True:
    inp = str(input("Enter a statement: "))
    if (inp == "reset"):
        tree.reset()
        continue
    print(tree.handleInput(inp))
