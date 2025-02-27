import sys
import re

inputFile = sys.argv[1]
outputFile = re.sub("\.asm", ".hack", inputFile)
lineNumber = 0
variables = []
labels = []
lableLine = []
with open(inputFile, "r") as asm, open(outputFile, "r+") as hack:
    for line in asm:
        # Start by formatting the hack file

        line = re.sub("\s", "", line) # Strip all whitespace
        line = re.sub("/{2}.*", "", line) # Strip all comments
        
        # Handle Symbols

        # Start with predefined symbols
        
        # First, handle all Rs
        line = re.sub("^@(R[0-9]|R1[0-5])", "@" + line[2:], line)

        # Next, handle the other predifined symbols
        line = re.sub("^@SCREEN", "@" + "16384", line)
        line = re.sub("^@KBD", "@" + "24576", line)
        line = re.sub("^@SP", "@" + "0", line)
        line = re.sub("^@LCL", "@" + "1", line)
        line = re.sub("^@ARG", "@" + "2", line)
        line = re.sub("^@THIS", "@" + "3", line)
        line = re.sub("^@THAT", "@" + "4", line)

        # Next, handle creation of labels
        isLabel = re.search("^(\([a-z|A-Z|\.|_|\$|:\][\w|\.|:|\$]*\))$", line)
        if(isLabel):
            labels.append(isLabel.string[1:-1])
            lableLine.append(lineNumber)
        
        # Next, handle variables and labels in A commands
        isVariable = re.search("^@(?![0-9]{1,3}|R[0-9]|R1[0-5]|SCREEN|KBD|SP|LCL|ARG|THIS|THAT)", line)
        if isVariable:
            variable = isVariable.string[1:]
            if((variable not in variables) and (variable not in labels)):
                variables.append(variable)
            if(variable not in labels):
                line = "@" + str(variables.index(variable))
            else:
                line = "@" + lableLine[labels.index(variable)]
        
        if((not isLabel) and (line != "")):
            hack.write(line + "\n")



    for line in hack:
        # Deal with A commands
        isACommand = re.search("^@[0-9]{1,3}", line) # Check to see if it is an A command
        if isACommand:
            value = int(line[1:]) # Strip the number from the A command
            binaryValue = format(value, '016b') # Convert to binary
        
        # Deal with C commands
