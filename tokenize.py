# parser.py
# Friday, November 6, 2020

class InvalidTokenizerMode(Exception):
    pass

def wltokenize(inputString, tokenSets):
    """
    Returns a list of tokens generated from analyzing the inputString argument. 
    
    A set of characters makes up a single symbolSet. This tokenizer function supports tokenizing a string using multiple different symbol sets at once. 
    For instance, if one symbol set is composed of only digits and another symbol set is composed of parentheses, then the string "(12 1234)" will be tokenized 
    into ["(", "12", "1234", ")"]. 
    
    The different symbol sets are stored in the tokenSets list. The algorithm checks these sets one by one, in the order that they are in tokenSets. If two
    symbolSets contain the same character, behavior depends on both the the previous character and the order of the symbolSets in tokenSets. If the previous character is part of some token, then current character will also become part of this token as long as the current character is in the same symbolSet as the previous character. 
    
    If the previous character was not part of any token, then the current character will become a token of the first symbolSet that contains the character. 
    
    The wltokenize method treats the characters in the symbolSets as a whitelist: only character in the symbolSet can become part of the token. The bltokenize 
    method is the opposite. It blacklists the character in the symbolSets. Although the bltokenize function also supports multiple symbolSets, this feature is
    questionably useful since chracters blacklisted by one symbolSet might not be blacklisted by other sets. 
    
    """
    tokens = []
    
    inputIterator = 0
    stopIterator = len(inputString)
    
    while inputIterator < stopIterator:
        atCharacter = inputString[inputIterator]
        
        for symbolSet in tokenSets:
            if atCharacter in symbolSet:
                tempToken = atCharacter
                while inputIterator < (stopIterator - 1):
                    tempCharacter = inputString[inputIterator + 1]
                    if tempCharacter in symbolSet:
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
        
        for symbolSet in tokenSets:
            if not (atCharacter in symbolSet):
                tempToken = atCharacter
                while inputIterator < (stopIterator - 1):
                    tempCharacter = inputString[inputIterator + 1]
                    if not (tempCharacter in symbolSet):
                        tempToken = tempToken + tempCharacter
                        inputIterator += 1
                    else:
                        break
                tokens.append(tempToken)
        inputIterator += 1
    
    return tokens

def tokenize(inputString, tokenCharacters, mode="wl"):
    """
    The user facing function that tokenizes an inputString. Tokens are returned in a list. 
    The tokenCharacters argument must be a list or set containing at least one symbolSet. 
    
    Depending on the mode argument, tokenize calls either wltokenize or bltokenize. See the documentation for these two methods for information about how 
    the tokenizer works. 
    """
    if mode == "wl":
        return wltokenize(inputString, tokenCharacters)
    elif mode == "bl":
        return bltokenize(inputString, tokenCharacters)
    else:
        raise InvalidTokenizerMode