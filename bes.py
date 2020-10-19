#Boolean Exmpression Solver
#Monday, August 21, 2020

class InvalidInputError(Exception):
    pass

class VAR:
    def __init__(self, var):
        self.var = var
    def __call__(self, variables, buildRes):
        buildRes.append((self.var, variables[self.var]))
        return variables[self.var]

class NOT:
    def __init__(self, func):
        self.operand = func
    def __call__(self, variables, buildRes):
        op = self.operand(variables, buildRes)
        if op == '1':
            ret = '0'
        else:
            ret = '1'
        buildRes.append(('NOT', ret))
        return ret

class AND:
    def __init__(self, func1, func2):
        self.operand1 = func1
        self.operand2 = func2
    def __call__(self, variables, buildRes):
        op1 = self.operand1(variables, buildRes)
        op2 = self.operand2(variables, buildRes)
        if op1 == '1' and op2 == '1':
            ret = '1'
        else:
            ret = '0'
        buildRes.append(('AND', ret))
        return ret

class OR:
    def __init__(self, func1, func2):
        self.operand1 = func1
        self.operand2 = func2
    def __call__(self, variables, buildRes):
        op1 = self.operand1(variables, buildRes)
        op2 = self.operand2(variables, buildRes)
        if op1 == '1' or op2 == '1':
            ret = '1'
        else:
            ret = '0'
        buildRes.append(('OR', ret))
        return ret
        
def toFunc(funcString):
    funcString = funcString.strip()
    # Build a set of valid characters
    valid = {chr(ord('a') + i) for i in range(26)}
    valid.update({chr(ord('A') + i) for i in range(26)})
    valid.update({' ', '1', '0', '(', ')'})
    operators = {'NOT', 'AND', 'OR'}
    
    funcList = []
    variables = {}
    
    # FuncList is a partially parsed version of funcString that condenses characters into variables and operators.
    funcPointer = 0
    while funcPointer < len(funcString):
        if not funcString[funcPointer] in valid:
            raise InvalidInputError
        elif funcString[funcPointer].isspace():
            funcPointer = funcPointer + 1
        elif funcString[funcPointer] == '(' or funcString[funcPointer] == ')':
            funcList.append(funcString[funcPointer])
            funcPointer = funcPointer + 1
        else:
            word = ''
            while funcPointer < len(funcString) and not funcString[funcPointer].isspace() and funcString[funcPointer] != ')':
                word = word + funcString[funcPointer]
                funcPointer = funcPointer + 1
            word = word.upper()
            if not word in operators:
                variables[word] = 0
                funcList.append(VAR(word))
            else:
                funcList.append(word)
    
    #print('originalfl: ', funcList)
    
    def isValid(entry):
        return not (entry == '(' or entry == ')')
    
    # Converts the funcList into a single callable function
    while len(funcList) > 1:
        #print('partial: ', funcList)
        performed = False
        
        # Parse parentheses
        startPointer = 0
        endPointer = 2
        while endPointer < len(funcList):
            if funcList[startPointer] == '(' and funcList[endPointer] == ')':
                funcList[startPointer: endPointer + 1] = [funcList[startPointer + 1]]
                performed = True
                break
            else:
                startPointer += 1
                endPointer += 1
        
        if performed:
            continue
        
        # Parse NOT 
        startPointer = 0
        endPointer = 1
        while endPointer < len(funcList):
            if funcList[startPointer] == 'NOT' and isValid(funcList[endPointer]):
                funcList[startPointer: endPointer + 1] = [NOT(funcList[endPointer])]
                performed = True
                break
            else:
                startPointer += 1
                endPointer += 1
        
        if performed:
            continue
        
        # Parse AND 
        startPointer = 0
        endPointer = 2
        while endPointer < len(funcList):
            if isValid(funcList[startPointer]) and funcList[startPointer + 1] == 'AND' and isValid(funcList[endPointer]):
                funcList[startPointer: endPointer + 1] = [AND(funcList[startPointer], funcList[endPointer])]
                performed = True
                break
            else:
                startPointer += 1
                endPointer += 1
        
        if performed:
            continue
            
        # Parse OR
        startPointer = 0
        endPointer = 2
        while endPointer < len(funcList):
            if isValid(funcList[startPointer]) and funcList[startPointer + 1] == 'OR' and isValid(funcList[endPointer]):
                funcList[startPointer: endPointer + 1] = [OR(funcList[startPointer], funcList[endPointer])]
                performed = True
                break
            else:
                startPointer += 1
                endPointer += 1
        
        if performed:
            continue
    #print('final: ', funcList)
    return (funcList[0], variables)

def genVariablePermutations(variables):
    permutations = []
    
    def recursivePermutations(tempTuple):
        if len(tempTuple) == len(variables):
            permutations.append(dict(zip(tuple(variables.keys()), tempTuple)))
        else:
            recursivePermutations(tempTuple + ('1', ))
            recursivePermutations(tempTuple + ('0', ))
    recursivePermutations(tuple())
    return permutations
    
def test(string):
    t = toFunc(string)
    func = t[0]
    variables = t[1]
    permutations = genVariablePermutations(variables)
    
    # print(func)
    # print(variables)
    # print(permutations)
    
    table = gm(func, permutations)
    pr(table)
    
def gm(func, permutations):
    table = []
    
    row = []
    variables = permutations[0].keys()
    for var in variables:
        row.append(var)
    row.append('|')
    initSteps = []
    func(permutations[0], initSteps)
    for step in initSteps:
        row.append(step[0])
    row.append('|')
    row.append('RES')
    
    table.append(row)
    
    for entry in permutations:
        buildRow = []
        for var in variables:
            buildRow.append(entry[var])
        buildRow.append('|')
        steps = []
        func(entry, steps)
        for step in steps:
            buildRow.append(step[1])
        buildRow.append('|')
        buildRow.append(steps[-1][1])
        table.append(buildRow)
    
    return table

def pr(table):
    string = ''
    for row in table:
        for entry in row:
            if len(entry) == 1:
                string = string + ' ' + entry + ' '
            elif len(entry) == 2:
                string = string + ' ' + entry
            else:
                string = string + entry
            string = string + '    '
        string = string + '\n'
    print(string)
        
        