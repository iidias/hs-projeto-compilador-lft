# Dicionario que representa a tabela de simbolos.
symbolTable = []
# Tipos suportados
INT     = 'Int'
BOOL    = 'Bool'
STRING  = 'String'
CHAR    = 'Char'
UNKNOWN = 'desconhecido'

# Constantes de estrutura
TYPE      = 'type'
PARAMS    = 'params'
BINDABLE  = 'bindable'
FUNCTION  = 'funcao'
VARIABLE  = 'variavel'
SCOPE     = 'escopo'

Numerico  = [INT]

# Se DEBUG = -1, imprime conteúdo da tabela após cada mudança
DEBUG = 0

def printTable():
    global DEBUG
    if DEBUG == -1:
        print('Tabela:', symbolTable)

def beginScope(nameScope):
    global symbolTable
    symbolTable.append({})
    symbolTable[-1][SCOPE] = nameScope
    printTable()

def endScope():
    global symbolTable
    symbolTable = symbolTable[0:-1]
    printTable()

def addVar(name, type):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: VARIABLE, TYPE: type}
    printTable()

def addFunction(name, params, returnType):
    global symbolTable
    symbolTable[-1][name] = {BINDABLE: FUNCTION, PARAMS: params, TYPE: returnType}
    printTable()

def getBindable(name):
    global symbolTable
    for i in reversed(range(len(symbolTable))):
        if name in symbolTable[i].keys():
            return symbolTable[i][name]
    return None

def getScope():
    global symbolTable
    if len(symbolTable) > 0:
        return symbolTable[-1].get(SCOPE, 'global')
    return 'global'
