import sys
import re

inputFile = sys.argv[1]
outputFile = re.sub("\.asm", ".hack", inputFile)
lineNumber = 0
variables = []
labels = []
lableLine = []
storeCode = []
with open(inputFile, "r") as asm, open(outputFile, "w+") as hack:
    for line in asm:
        # Start by formatting the hack file

        line = re.sub("\s", "", line) # Strip all whitespace
        line = re.sub("/{2}.*", "", line) # Strip all comments

        # Create list of all labels
        isLabel = re.search("^(\([a-z|A-Z|\.|_|\$|:\][\w|\.|:|\$]*\))$", line)
        if(isLabel):
            labels.append(isLabel.string[1:-1])
            lableLine.append(lineNumber)
        
        if((not isLabel) and (line != "")):
            storeCode.append(line)
            lineNumber += 1

    for i in range(len(storeCode)):
        # Handle Symbols

        # Start with predefined symbols
        
        # First, handle all Rs
        storeCode[i] = re.sub("^@(R[0-9]|R1[0-5])", "@" + storeCode[i][2:], storeCode[i])

        # Next, handle the other predifined symbols
        storeCode[i] = re.sub("^@SCREEN", "@" + "16384", storeCode[i])
        storeCode[i] = re.sub("^@KBD", "@" + "24576", storeCode[i])
        storeCode[i] = re.sub("^@SP", "@" + "0", storeCode[i])
        storeCode[i] = re.sub("^@LCL", "@" + "1", storeCode[i])
        storeCode[i] = re.sub("^@ARG", "@" + "2", storeCode[i])
        storeCode[i] = re.sub("^@THIS", "@" + "3", storeCode[i])
        storeCode[i] = re.sub("^@THAT", "@" + "4", storeCode[i])
        
        # Next, handle variables and labels in A commands
        isVariable = re.search("^@(?![0-9]{1,3}|R[0-9]|R1[0-5]|SCREEN|KBD|SP|LCL|ARG|THIS|THAT)", storeCode[i])
        if isVariable:
            variable = isVariable.string[1:]
            if((variable not in variables) and (variable not in labels)):
                variables.append(variable)
            if(variable not in labels):
                storeCode[i] = "@" + str(variables.index(variable) + 16)
            else:
                storeCode[i] = "@" + str(lableLine[labels.index(variable)])


    for j in range(len(storeCode)):
        # Deal with A commands
        isACommand = re.search("^@[0-9]{1,3}", storeCode[j]) # Check to see if it is an A command
        if isACommand:
            value = int(storeCode[j][1:]) # Strip the number from the A command
            binaryValue = format(value, '016b') # Convert to binary
            storeCode[j] = str(binaryValue)
        
        # Deal with C commands
        
        # Write to output
        hack.write(storeCode[j] + "\n")
