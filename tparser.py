# parser.py
# Friday, November 6, 2020

class InvalidTokenizerMode(Exception):
    pass

def wltokenize(inputString, tokenCharacters):
    tokens = []
    
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

def bltokenize(inputString, tokenCharacters):
    tokens = []
    
    inputIterator = 0
    stopIterator = len(inputString)
    
    while inputIterator < stopIterator:
        atCharacter = inputString[inputIterator]
        if not (atCharacter in tokenCharacters):
            tempToken = atCharacter
            while inputIterator < (stopIterator - 1):
                tempCharacter = inputString[inputIterator + 1]
                if not (tempCharacter in tokenCharacters):
                    tempToken = tempToken + tempCharacter
                    inputIterator += 1
                else:
                    break
            tokens.append(tempToken)
        inputIterator += 1
    
    return tokens

def tokenize(inputString, tokenCharacters, mode="wl"):
    if mode == "wl":
        return wltokenize(inputString, tokenCharacters)
    elif mode == "bl":
        return bltokenize(inputString, tokenCharacters)
    else:
        raise InvalidTokenizerMode