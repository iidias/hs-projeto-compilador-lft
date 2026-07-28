symbolTable = []

SCOPE = 'escopo'
SCOPE_MAIN = 'main'
OFFSET = 'offset'
SP = 'sp'
# Se DEBUG = -1, imprime a tabela apos cada mudanca
DEBUG = 0

def printTable():
    if DEBUG == -1:
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
    symbolTable[-1][SP] += value

def getSP():
    return symbolTable[-1][SP]

def main():
    global DEBUG
    DEBUG = -1

    print('\n# Criando escopo main')
    beginScope(SCOPE_MAIN)

    print('\n# Adicionando local x (offset automatico)')
    addVar('x')

    print('\n# Adicionando local y (offset automatico)')
    addVar('y')

    print('\n# Criando escopo da funcao soma')
    beginScope('soma')

    print('\n# Adicionando parametros a e b (offsets explicitos, positivos)')
    addVar('a', 12)
    addVar('b', 8)

    print('\n# Adicionando local dobro dentro de soma')
    addVar('dobro')

    print('\n# Consultando offset de a (parametro)')
    print(getOffset('a'))

    print('\n# Consultando offset de dobro (local)')
    print(getOffset('dobro'))

    print('\n# Consultando offset de nome inexistente')
    print(getOffset('naoexiste'))

    print('\n# SP de soma antes do escopo aninhado')
    print(getSP())

    print('\n# Criando escopo aninhado (let dentro de soma)')
    beginNestedScope('let')

    print('\n# Adicionando local soma_parcial dentro do let')
    addVar('soma_parcial')

    print('\n# x do escopo main ainda visivel de dentro do let')
    print(getOffset('x'))

    print('\n# Sombreamento: novo x local ao let')
    addVar('x')
    print(getOffset('x'))

    print('\n# Removendo escopo let')
    endScope()

    print('\n# Apos endScope, x volta a ser o do escopo main')
    print(getOffset('x'))

    print('\n# Removendo escopo soma')
    endScope()

if __name__ == "__main__":
    main()