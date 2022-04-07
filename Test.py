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

# TODO: What case do we branch back up to the top dialog option? 
# Currently if there are no children branches, goes back to top