import random
import re

# This file got very long and scuffed, but it works
# Sorry guys....

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
            if (branch.matchInput(userInput, self.__defMap)):
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
    def __init__(self, expectedInput, output, updateVarArray):
        self.__expectedInput = expectedInput
        self.__output = output
        self.updateVarArray = updateVarArray
        self.__childrenBranches = []

    def addChildBranch(self, branch):
        self.__childrenBranches.append(branch)

    # TODO: Add checking against strings of multiple words/testing
    # Returns true if the given input matches this branch
    def matchInput(self, input, defMap):
        inputWords = re.split(" ", input)

        # Check against each input
        inpIndex = 0
        for i in range(len(self.__expectedInput)):

            # Check if not enough input
            if (inpIndex >= len(inputWords)):
                return False

            # Checking against a list
            if (type(self.__expectedInput[i]) is list):
                # Check if matches any words in list
                anyMatch = False
                for j in range(len(self.__expectedInput[i])):
                    if (self.__expectedInput[i][j] == inputWords[inpIndex]):
                        anyMatch = True
                        break
                    # Current "word" is actuall a string of words
                    elif (" " in self.__expectedInput[i][j]):

                        # Look ahead in input for potential match
                        lookAheadIndex = inpIndex
                        stringWords = self.__expectedInput[i][j].split(" ")
                        allMatch = True
                        for word in stringWords:
                            if (lookAheadIndex >= len(inputWords)):
                                allMatch = False
                            elif (inputWords[lookAheadIndex] != word):
                                allMatch = False
                                break
                            lookAheadIndex += 1

                        # Found match, change input index to match
                        if (allMatch):
                            anyMatch = True
                            inpIndex = lookAheadIndex - 1
                            break
                        
                if (not anyMatch):
                    return False

            # Checking against a def
            elif (self.__expectedInput[i][0] == "~"):
                loadedDef = defMap[self.__expectedInput[i][1:]]
                # def points to list
                if (type(loadedDef) is list):
                    anyMatch = False
                    for j in range(len(loadedDef)):
                        if (loadedDef[j] == inputWords[inpIndex]):
                            anyMatch = True
                            break

                        # Current "word" is actuall a string of words
                        elif (" " in loadedDef[j]):
                            # Look ahead in input for potential match
                            lookAheadIndex = inpIndex
                            stringWords = loadedDef[j].split(" ")
                            allMatch = True
                            for word in stringWords:
                                if (lookAheadIndex >= len(inputWords)):
                                    allMatch = False
                                elif (inputWords[lookAheadIndex] != word):
                                    allMatch = False
                                    break
                                lookAheadIndex += 1

                            # Found match, change input index to match
                            if (allMatch):
                                anyMatch = True
                                inpIndex = lookAheadIndex
                                break
                        
                    if (not anyMatch):
                        return False
                
                # def points to a string of words
                elif (" " in loadedDef):
                    # Look ahead in input for potential match
                    lookAheadIndex = inpIndex
                    stringWords = loadedDef.split(" ")
                    allMatch = True
                    for word in stringWords:
                        if (lookAheadIndex >= len(inputWords)):
                            allMatch = False
                        elif (inputWords[lookAheadIndex] != word):
                            allMatch = False
                            break
                        lookAheadIndex += 1

                    # Found match, change input index to match
                    if (not allMatch):
                        return False

                    inpIndex = lookAheadIndex

                # def points to a single word
                elif (loadedDef != inputWords[inpIndex]):
                        return False

            # Checking against a variable or regular word
            elif (self.__expectedInput[i][0] != "$"):
                if (self.__expectedInput[i] != inputWords[inpIndex]):
                    return False

            inpIndex += 1
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

            if (type(curWord) is list):
                formattedOutput += random.choice(curWord)
            else:
                formattedOutput += curWord + " "

        # Update variables with their new values
        for updateVarTuple in self.updateVarArray:
            varMap[updateVarTuple[0]] = varMap[updateVarTuple[1]]

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
        self.__tree = Dialog()

        segments = self.__parseSegList()

        defMap = {}
        startingBranches = []

        for segment in segments:
            if (type(segment) is tuple):
                defMap[segment[0]] = segment[1]
            elif (segment != None):
                startingBranches.append(segment)

        self.__tree.setDefMap(defMap)
        self.__tree.setStartingBranches(startingBranches)
        self.__tree.reset()

        return self.__tree

    # Get the dialog tree that was parsed
    def getTree(self):
        return self.__tree

    def __parseSegList(self):
        firstItem = self.__parseSegment()

        # Scrub forward until next \n token
        # Helps with skipping lines that were incorrect
        skipped = ""
        while(self.__tokenizer.hasNextToken() and self.__tokenizer.peekNextToken() != "\n"):
            skipped += self.__tokenizer.getNextToken() + " "

        # We skipped some important code due to a syntax error
        if (skipped != "" and skipped[0] != "#"):
            print("Skipped:", repr(skipped))

        if (self.__tokenizer.peekNextToken() == "\n"):
            self.__tokenizer.getNextToken()
            if (self.__tokenizer.hasNextToken()):
                restItems = self.__parseSegList()
                restItems.insert(0, firstItem)
                return restItems

        return [firstItem]

    # Parses a segment, which is either a comment, definition, or USegment
    # Returns None if comment, the definition tuple if definition, or the DialogBranch if USegment
    def __parseSegment(self):
        peekedToken = self.__tokenizer.peekNextToken()
        if (peekedToken == None):
            return None
        # Comment
        if (peekedToken[0] == "#"):
            # Skip token
            self.__tokenizer.getNextToken()
            return None
        # Definition
        if (peekedToken[0] == "~"):
            return self.__parseDefinition()
        # USegment
        if (peekedToken[0] == "u"):
            return self.__parseUSegmentList()

        return None

    # Parses a definition, returns a tuple of (name,value) or None if syntax was invalid
    def __parseDefinition(self):
        defName = self.__tokenizer.getNextToken()[1:]
        if (self.__tokenizer.getNextToken() != ":"):
            self.__printError(":")
            return None
        defValue = self.__parseDefValue()
        if (defValue == None):
            return None
        return (defName, defValue)

    # Parses a value of a definition and returns either a single value or an array of values
    def __parseDefValue(self):
        result = None
        if (self.__tokenizer.peekNextToken() == "["):
            self.__tokenizer.getNextToken()
            result = self.__parseList()
            if (self.__tokenizer.getNextToken() != "]"):
                self.__printError("]")
                return None
        else:
            result = self.__parseValue()

        return result

    # Parses a list of values and returns an array of the values
    def __parseList(self):
        firstValue = self.__parseValue()

        nextToken = self.__tokenizer.peekNextToken()
        # Check if next token is a value
        if ((nextToken[0] == "\"" and nextToken[-1] == "\"") or re.match(r"[a-zA-Z0-9_]+", nextToken)):
            restValues = self.__parseList()
            restValues.insert(0, firstValue)
            return restValues
        return [firstValue]

    # Parses a value and returns it
    def __parseValue(self):
        value = self.__tokenizer.getNextToken()
        if (value[0] == "\"" and value[-1] == "\""):
            value = value[1:-1]
        return value

    # TODO: Finish USegment
    # Parses a USegment and returns the created DialogBranch
    def __parseUSegmentList(self, x=None):
        if (x == None and self.__tokenizer.getNextToken() != "u"):
            self.__printError("u")
            return None
        if (x != None and self.__tokenizer.getNextToken() != "u" + str(x)):
            self.__printError("u" + str(x))
            return None
        if (self.__tokenizer.getNextToken() != ":"):
            self.__printError(":")
            return None
        if (self.__tokenizer.getNextToken() != "("):
            self.__printError("(")
            return None

        splitInput = self.__parseInput()
        if (splitInput == None):
            return None

        if (self.__tokenizer.getNextToken() != ")"):
            self.__printError(")")
            return None
        if (self.__tokenizer.getNextToken() != ":"):
            self.__printError(":")
            return None

        splitResponse = self.__parseResponse()
        if (splitResponse == None):
            return None

        assignments = []
        if (re.match(r"\$[a-zA-Z0-9]+=\$[a-zA-Z0-9]+", self.__tokenizer.peekNextToken())):
            assignments = self.__parseAssignments()
            if (assignments == None):
                return None

        # Format the input arguments
        curVariablePos = 0
        for i in range(len(splitInput)):
            if (splitInput[i] == "_"):
                varsToSkip = curVariablePos

                # Look for the variable in the responses
                for j in range(len(splitResponse)):
                    if (splitResponse[j][0] == "$"):
                        if (varsToSkip == 0):
                            varsToSkip -= 1
                            splitInput[i] = splitResponse[j]
                            break
                        varsToSkip -= 1

                # Did not find variable, keep looking in the assignments
                if (varsToSkip >= 0):
                    for assignTuple in assignments:
                        if (varsToSkip == 0):
                            varsToSkip -= 1
                            splitInput[i] = "$" + assignTuple[1]
                            break
                        varsToSkip -= 1

                # Unmatched variable
                if (splitInput[i] == "_"):
                    print(
                        "Unmatched input with no variable name in response or assignments")
                    return None
                curVariablePos += 1

        curBranch = DialogBranch(splitInput, splitResponse, assignments)

        newX = 1
        if (x != None):
            newX = x + 1

        if (self.__tokenizer.peekNextToken() == "\n" and self.__tokenizer.peekAhead(2) == "u" + str(newX)):
            self.__tokenizer.getNextToken()
            childrenBranches = self.__parseUSegmentList(x=newX)
            if (childrenBranches != None):
                for childBranch in childrenBranches:
                    curBranch.addChildBranch(childBranch)

        if (x != None and self.__tokenizer.peekNextToken() == "\n" and self.__tokenizer.peekAhead(2) == "u" + str(x)):
            self.__tokenizer.getNextToken()
            siblingBranches = self.__parseUSegmentList(x=x)
            siblingBranches.insert(0, curBranch)
            return siblingBranches

        if (x == None):
            return curBranch

        return [curBranch]

    # Parses the input for a USegment
    # Returns a split list of words/underscores/arrays/~defs for writing to variables
    def __parseInput(self):

        curInput = self.__tokenizer.getNextToken()

        if (curInput == "["):
            curInput = self.__parseList()
            if (self.__tokenizer.getNextToken() != "]"):
                self.__printError("]")

        if (re.match(r"~?[a-zA-Z0-9_]+|\[", self.__tokenizer.peekNextToken())):
            restInput = self.__parseInput()
            restInput.insert(0, curInput)
            return restInput

        return [curInput]

    # Parses the response for a USegment
    # Returns a split list of words, ~definitions, $varibales, arrays
    def __parseResponse(self):
        curVal = None

        if (self.__tokenizer.peekNextToken() == "["):
            self.__tokenizer.getNextToken()
            curVal = self.__parseList()
            if (self.__tokenizer.peekNextToken() != "]"):
                self.__printError("]")
                return None
            self.__tokenizer.getNextToken()

        else:
            curVal = self.__tokenizer.getNextToken()

        nextToken = self.__tokenizer.peekNextToken()
        if (re.fullmatch(r"[~$][a-zA-Z0-9]+|[a-zA-Z0-9]+|\[", nextToken)):
            restResponses = self.__parseResponse()
            restResponses.insert(0, curVal)
            return restResponses

        return [curVal]

    # Returns a list of tuples denoting what variable should be updated by another variable
    def __parseAssignments(self):

        assignment = self.__tokenizer.getNextToken()
        varArray = assignment.split("=")

        varTuple = (varArray[0][1:], varArray[1][1:])

        if (re.match(r"\$[a-zA-Z0-9]+=\$[a-zA-Z0-9]+", self.__tokenizer.peekNextToken())):
            restTuples = self.__parseAssignments()
            restTuples.insert(0, varTuple)
            return restTuples

        return [varTuple]

    def __printError(self, expected):
        print("Invalid Syntax\n\tNear " +
              repr(self.__tokenizer.getCurToken()), "\n\tExpected: " + repr(expected))


# Represents the tokenizer for a dialog file
class DialogTokenizer:
    # Tokenizes a given string into tokens matching the format of a dialog file
    def __init__(self, asString):
        self.__asString = asString
        self.__tokenize()

    # Actually tokenize the string
    def __tokenize(self):
        # This scuffed regex targets keywords, keeps strings together, etc.
        tokens = re.findall(
            r"#.+|~\w+|:|\[|\]|\"[^\"]+\"|_|\(|\)|\$\w+=\$\w+|\$\w+|\w+|\n", self.__asString)

        # Remove comments and excess newlines
        for i in range(len(tokens) - 1, -1, -1):
            if (tokens[i][0] == "#"):
                tokens.pop(i)
            elif (tokens[i] == '\n'):
                if (i + 1 < len(tokens)):
                    if (tokens[i + 1] == '\n'):
                        tokens.pop(i)

        self.__tokens = tokens
        self.__curToken = -1

    # Returns the next token in the list and increments the pointer
    # This does not consider comments
    def getNextToken(self,):
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

    # Peeks the token amount ahead in the list without incrementing the pointer
    def peekAhead(self, amount):
        pos = self.__curToken + amount
        if (len(self.__tokens) == pos):
            return None
        else:
            return self.__tokens[pos]

    # Moves the current position to the next newline character
    def nextLine(self):
        pos = self.__curToken + 1
        while (self.__tokens[pos] != "\n"):
            pos += 1
        self.__curToken = pos

    # Returns the list of all tokens, including comments
    def getAllTokens(self):
        return self.__tokens

    # Returns if there is a next token
    def hasNextToken(self):
        return self.peekNextToken() != None
