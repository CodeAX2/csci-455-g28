import random
import re

# Represents a dialog tree


class Dialog:
    # Creates a new dialog tree
    # defMap is a mapping from string to string/list to provide values for definitions
    # startingBranches is a list of DialogBranch that defines the starting dialog options
    def __init__(self):
        self.__varMap = {}
        self.__defMap = {}
        self.__curBranches: list[DialogBranch] = []
        self.__baseBranches: list[DialogBranch] = []

    def setStartingBranches(self, startingBranches):
        self.__baseBranches = startingBranches

    def setDefMap(self, defMap):
        self.__defMap = defMap

    # Set the current branches to check user input against
    # branches is a list of DialogBranch
    def setCurBranches(self, branches):
        self.__curBranches = branches

    # Handle current user input
    # userInput is a string that will be tested against each branch
    def handleInput(self, userInput):
        for branch in self.__curBranches:
            if (branch.matchInput(userInput)):
                return branch.handleInput(userInput, self.__defMap, self.__varMap, self)
        return None

    # Resets the tree back to its initial state
    def reset(self):
        self.__curBranches = self.__baseBranches


# Represents one branch of dialog, which can have children branches
class DialogBranch:
    # Creates a new branch of dialog
    # expectedInput is an array of strings and variable names of the format $varName
    # output is the format of the output, using variable and definition names $varName ~defName
    # updateVarMap is a map of variables names to be updated by their keys
    def __init__(self, expectedInput, output, updateVarMap):
        self.__expectedInput = expectedInput
        self.__output = output
        self.__updateVarMap = updateVarMap
        self.__childrenBranches = []

    def addChildBranch(self, branch):
        self.__childrenBranches.append(branch)

    # Returns true if the given input matches this branch
    def matchInput(self, input):
        inputWords = re.split(" ", input)
        for i in range(len(self.__expectedInput)):
            if (self.__expectedInput[i][0] != "$"):
                if (self.__expectedInput[i] != inputWords[i]):
                    return False
        return True

    # Handles user input, given a defMap and varMap and a working tree
    def handleInput(self, input, defMap, varMap, dialogTree: Dialog):
        inputWords = re.split(" ", input)
        # Save new variables from input
        for i in range(len(self.__expectedInput)):
            if (self.__expectedInput[i][0] == "$"):
                varName = self.__expectedInput[i][1:]
                varMap[varName] = inputWords[i]

        # Create the output
        formattedOutput = ""
        for i in range(len(self.__output)):
            curWord = ""
            # If the word is a variable
            if (self.__output[i][0] == "$"):
                varName = self.__output[i][1:]
                curWord = varMap[varName]
            # If the word is a definition
            elif (self.__output[i][0] == "~"):
                defName = self.__output[i][1:]
                curWord = DialogBranch.__getDefOutput(defMap, defName)
            # The word is just a word
            else:
                curWord = self.__output[i]

            formattedOutput += curWord + " "

        # Update variables with their new values
        for updateVarKey in self.__updateVarMap:
            varMap[updateVarKey] = varMap[self.__updateVarMap[updateVarKey]]

        # Update the branch of the tree
        if (len(self.__childrenBranches) != 0):
            dialogTree.setCurBranches(self.__childrenBranches)

        # Return the dialog
        return formattedOutput

    # Gets the output from a def
    # If the def points to a list, a random element is chosen
    def __getDefOutput(defMap, defName):
        defValue = defMap[defName]
        if(isinstance(defValue, list)):
            return random.choice(defValue)
        else:
            return defValue


# Parses a dialog file
class DialogParser:

    # Creates a new DialogParser that will parse the file at the given inputFilePath
    def __init__(self, inputFilePath):
        file = open(inputFilePath)
        self.__tokenizer: DialogTokenizer = DialogTokenizer(file.read())

    # Parses the dialog file and returns a new dialog tree object
    def parseFile(self):
        # TODO: Implement the actual parsing and creation of the dialog tree and branches
        self.__tree = Dialog()

        self._parseSegList()

        return self.__tree

    def getTree(self):
        return self.__tree

    def __parseSegList(self):
        self.__parseSegment()

        if (self.__tokenizer.peekNextToken() == "\n"):
            self.__tokenizer.getNextToken()
            if (self.__tokenizer.hasNextToken()):
                self.__parseSegList()

    def __parseSegment(self):
        peekedToken = self.__tokenizer.peekNextToken()
        # Comment
        if (peekedToken[0] == "#"):
            # Skip token
            self.__tokenizer.getNextToken()
            return
        # Definition
        if (peekedToken[0] == "~"):
            self.__parseDefinition()
            return
        # USegment
        if (peekedToken[0] == "u"):
            self.__parseUSegment()
            return

    def __parseDefinition():
        pass

    def __parseUSegment():
        pass

# Represents the tokenizer for a dialog file
class DialogTokenizer:
    # Tokenizes a given string into tokens matching the format of a dialog file
    def __init__(self, asString):
        self.__asString = asString
        self.__tokenize()

    # Actually tokenize the string
    def __tokenize(self):
        # This scuffed regex targets keywords, keeps strings together, etc.
        self.__tokens = re.findall(
            r"#.+|~\w+|:|\[|\]|\".+\"|_|\(|\)|\$\w+=\$\w+|\$\w+|\w+|\n", self.__asString)
        self.__curToken = 0

    # Returns the next token in the list and increments the pointer
    def getNextToken(self):
        self.__curToken += 1
        if (len(self.__tokens) == self.__curToken):
            return None
        else:
            return self.__tokens[self.__curToken]

    # Returns the current token in the list
    def getCurToken(self):
        return self.__tokens[self.__curToken]

    # Returns the next token in the list without incrementing the pointer
    def peekNextToken(self):
        pos = self.__curToken + 1
        if (len(self.__tokens) == pos):
            return None
        else:
            return self.__tokens[pos]

    # Returns the list of all tokens
    def getAllTokens(self):
        return self.__tokens

    # Returns if there is a next token
    def hasNextToken(self):
        return self.__curToken != len(self.__tokens) - 1
