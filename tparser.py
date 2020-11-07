# parser.py
# Friday, November 6, 2020

def tokenizer(inputString):
    tokens = []
    tokenCharacters = ['a', 'b', 'c']
    
    inputIterator = 0
    stopIterator = len(inputString)
    
    while inputIterator < stopIterator:
        atCharacter = inputString[inputIterator]
        if atCharacter in tokenCharacters:
            tempToken = atCharacter
            while inputIterator < (stopIterator - 1):
                tempCharacter = inputString[inputIterator + 1]
                if tempCharacter in tokenCharacters:
                    tempToken = tempToken + tempCharacter
                    inputIterator += 1
                else:
                    break
            tokens.append(tempToken)
        inputIterator += 1
    
    return tokens