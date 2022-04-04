from email.mime import base
from RobotDialog import *

parser = DialogParser("test2.txt")
tree = parser.parseFile()

while True:
    inp = str(input("Enter a statement: "))
    if (inp == "reset"):
        tree.reset()
        continue
    if (inp == "exit"):
        break
    print(tree.handleInput(inp))

# TODO: tree should go back to base branches if reached bottom