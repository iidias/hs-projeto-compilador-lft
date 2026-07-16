from Visitor import *
import SymbolTable as st

def compativel(tipo1, tipo2):
    if tipo1 == tipo2:
        return tipo1
    if tipo1 == st.UNKNOWN or tipo2 == st.UNKNOWN:
        return st.UNKNOWN
    return None

class SemanticVisitor(AbstractVisitor):

    def __init__(self):
        self.printer = Visitor()
        self.n_errors = 0
        # Flag que indica se estamos dentro de um bloco where/let
        # Quando True, visitFuncDecl adiciona o nome ao escopo atual
        # em vez de abrir um novo escopo
        self.em_escopo_local = False
        st.beginScope('global')
        # Predefinidos de Haskell reconhecidos pelo compilador
        st.addVar('otherwise', st.BOOL)
        st.addVar('return', st.UNKNOWN)
        st.addVar('not',  st.BOOL)
        st.addVar('odd', st.BOOL)
        st.addVar('even', st.BOOL)
        st.addVar('show', st.STRING)
        st.addVar('sqrt', st.UNKNOWN)
        st.addVar('map', st.UNKNOWN)
        st.addVar('filter', st.UNKNOWN)
        st.addVar('foldr', st.UNKNOWN)
        st.addVar('foldl', st.UNKNOWN)

    # PROGRAMA

    def visitSingleDecl(self, singleDecl):
        singleDecl.decl.accept(self)

    def visitCompoundDecl(self, compoundDecl):
        compoundDecl.decl.accept(self)
        compoundDecl.program.accept(self)

    # DECLARAÇÕES

    def visitTypeSig(self, typeSig):
        # Registra a assinatura de tipo no escopo global
        st.addFunction(typeSig.name, [], str(typeSig.type_expr))

    """
    def visitFuncDecl(self, funcDecl):
       

    def visitFuncDeclWhere(self, funcDeclWhere):
        

    def visitFuncDeclGuards(self, funcDeclGuards):
        

    def visitDataDecl(self, dataDecl):"""
        

    # TIPOS

    def visitSimpleType(self, simpleType):
        return simpleType.name

    def visitArrowType(self, arrowType):
        return str(arrowType)

    def visitListType(self, listType):
        return str(listType)

    def visitTupleType(self, tupleType):
        return str(tupleType)

    def visitUnitType(self, unitType):
        return '()'

    # CONSTRUTORES DE DADOS

    def visitConstructor(self, constructor):
        st.addVar(constructor.name, st.UNKNOWN)

    def visitConstructorArgs(self, constructorArgs):
        # Registra o construtor no escopo (para declarações de dados)
        # e processa sub-padrões quando usado em casamento de padrões
        st.addVar(constructorArgs.name, st.UNKNOWN)
        for item in constructorArgs.types:
            if not isinstance(item, str):
                item.accept(self)

    # GUARDAS

    """
    def visitGuard(self, guard):
        
    def visitSingleGuards(self, singleGuards):

    def visitCompoundGuards(self, compoundGuards):"""

    # DECLARAÇÕES LOCAIS

    def visitSingleLocaldecl(self, singleLocaldecl):
        singleLocaldecl.decl.accept(self)

    def visitCompoundLocaldecl(self, compoundLocaldecl):
        compoundLocaldecl.decls.accept(self)
        compoundLocaldecl.decl.accept(self)

    # EXPRESSÕES

    def visitVarExp(self, varExp):
        bindable = st.getBindable(varExp.name)
        if bindable is None:
            self.n_errors += 1
            print('\t[Erro] Variavel ou funcao "' + varExp.name + '" nao declarada')
            return st.UNKNOWN
        return bindable[st.TYPE]

    def visitConExp(self, conExp):
        bindable = st.getBindable(conExp.name)
        if bindable is None:
            return st.UNKNOWN
        return bindable[st.TYPE]

    def visitIntExp(self, intExp):
        return st.INT

    def visitBoolExp(self, boolExp):
        return st.BOOL

    def visitCharExp(self, charExp):
        return st.CHAR

    def visitStringExp(self, stringExp):
        return st.STRING

    def visitAppExp(self, appExp):
        appExp.func.accept(self)
        appExp.arg.accept(self)
        return st.UNKNOWN

    """
    def visitInfixExp(self, infixExp):

    def visitNegExp(self, negExp):

    def visitNotExp(self, notExp):

    def visitIfExp(self, ifExp):

    def visitCaseExp(self, caseExp):

    def visitLetExp(self, letExp):
    

    def visitDoExp(self, doExp):"""
        
    def visitLambdaExp(self, lambdaExp):
        st.beginScope('lambda')
        for pat in lambdaExp.pats:
            pat.accept(self)
        lambdaExp.body.accept(self)
        st.endScope()
        return st.UNKNOWN

    def visitListExp(self, listExp):
        for elem in listExp.elems:
            elem.accept(self)
        return st.UNKNOWN

    def visitEmptyListExp(self, emptyListExp):
        return st.UNKNOWN

    def visitRangeExp(self, rangeExp):
        tipoInicio = rangeExp.start.accept(self)
        if tipoInicio not in [st.INT, st.UNKNOWN]:
            self.n_errors += 1
            print('\t[Erro] Inicio do intervalo deve ser Int. Encontrado:', tipoInicio)
        if rangeExp.end is not None:
            tipoFim = rangeExp.end.accept(self)
            if tipoFim not in [st.INT, st.UNKNOWN]:
                self.n_errors += 1
                print('\t[Erro] Fim do intervalo deve ser Int. Encontrado:', tipoFim)
        return st.UNKNOWN

    def visitTupleExp(self, tupleExp):
        for elem in tupleExp.elems:
            elem.accept(self)
        return st.UNKNOWN

    # ALTERNATIVAS DE CASE

    def visitSingleCaseAlts(self, singleCaseAlts):
        singleCaseAlts.alt.accept(self)

    def visitCompoundCaseAlts(self, compoundCaseAlts):
        compoundCaseAlts.alts.accept(self)
        compoundCaseAlts.alt.accept(self)

    def visitCaseAlt(self, caseAlt):
        st.beginScope('case')
        caseAlt.pat.accept(self)
        caseAlt.body.accept(self)
        st.endScope()

    # COMANDOS DO BLOCO DO

    def visitSingleDoStmts(self, singleDoStmts):
        singleDoStmts.stmt.accept(self)

    def visitCompoundDoStmts(self, compoundDoStmts):
        compoundDoStmts.stmts.accept(self)
        compoundDoStmts.stmt.accept(self)

    def visitBindStmt(self, bindStmt):
        tipo = bindStmt.expr.accept(self)
        st.addVar(bindStmt.var, tipo)

    def visitLetDoStmt(self, letDoStmt):
        anterior = self.em_escopo_local
        self.em_escopo_local = True
        letDoStmt.decls.accept(self)
        self.em_escopo_local = anterior

    def visitExprDoStmt(self, exprDoStmt):
        exprDoStmt.expr.accept(self)

    # PADRÕES (declaram variáveis no escopo atual)

    def visitWildcardPat(self, wildcardPat):
        return st.UNKNOWN

    def visitVarPat(self, varPat):
        st.addVar(varPat.name, st.UNKNOWN)
        return st.UNKNOWN

    def visitConPat(self, conPat):
        return st.UNKNOWN

    def visitIntPat(self, intPat):
        return st.INT

    def visitBoolPat(self, boolPat):
        return st.BOOL

    def visitCharPat(self, charPat):
        return st.CHAR

    def visitConsPat(self, consPat):
        consPat.head.accept(self)
        consPat.tail.accept(self)
        return st.UNKNOWN

    def visitTuplePat(self, tuplePat):
        for pat in tuplePat.pats:
            pat.accept(self)
        return st.UNKNOWN

    def visitListPat(self, listPat):
        for pat in listPat.pats:
            pat.accept(self)
        return st.UNKNOWN

    def visitEmptyListPat(self, emptyListPat):
        return st.UNKNOWN

    def getnerros(self):
        return self.n_errors


def main():
    f = open("input1.hs", "r")
    data = f.read()
    f.close()
    lexer  = HaskellLexer()
    parser = yacc.yacc()
    result = parser.parse('\n' + data, lexer=lexer)
    print("# verificacao semantica do programa de entrada\n")
    svisitor = SemanticVisitor()
    result.accept(svisitor)
    print(f"\nForam encontrados {svisitor.getnerros()} erro(s) semantico(s)")

if __name__ == "__main__":
    main()
