symbolTable = []

SCOPE = 'escopo'
SCOPE_MAIN = 'main'
OFFSET = 'offset'
SP = 'sp'

def printTable(debug=False):
    if debug:
        print('AssemblyST:', symbolTable)

def beginScope(nameScope):
    symbolTable.append({SCOPE: nameScope, SP: 0})
    printTable()

def beginNestedScope(nameScope):
    sp_atual = symbolTable[-1][SP] if symbolTable else 0
    symbolTable.append({SCOPE: nameScope, SP: sp_atual})
    printTable()

def endScope():
    global symbolTable
    symbolTable = symbolTable[0:-1]
    printTable()

def getScope():
    return symbolTable[-1][SCOPE] if symbolTable else None

def addVar(name, offset=None):
    if offset is not None:
        symbolTable[-1][name] = {OFFSET: offset}
    else:
        symbolTable[-1][SP] -= 4
        symbolTable[-1][name] = {OFFSET: symbolTable[-1][SP]}
    printTable()

def getOffset(name):
    for escopo in reversed(symbolTable):
        if name in escopo:
            return escopo[name][OFFSET]
    return None

def addSP(value):
    """Ajusta manualmente o contador SP do escopo atual (usado só em casos
    especiais; a maior parte do código usa addVar, que já ajusta sozinho)."""
    symbolTable[-1][SP] += value


def getSP():
    """SP (negativo) acumulado no escopo atual — usado para saber quantos
    bytes de locais essa função/escopo já reservou até agora."""
    return symbolTable[-1][SP]