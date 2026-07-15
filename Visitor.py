from abc import abstractmethod, ABCMeta
from ExpressionLanguageParser import *

tab = 0

def blank():
    p = ''
    for x in range(tab):
        p = p + ' '
    return p

class AbstractVisitor(metaclass=ABCMeta):

    # PROGRAMA
    @abstractmethod
    def visitSingleDecl(self, singleDecl): pass
    @abstractmethod
    def visitCompoundDecl(self, compoundDecl): pass

    # DECLARAÇÕES
    @abstractmethod
    def visitTypeSig(self, typeSig): pass
    @abstractmethod
    def visitFuncDecl(self, funcDecl): pass
    @abstractmethod
    def visitFuncDeclWhere(self, funcDeclWhere): pass
    @abstractmethod
    def visitFuncDeclGuards(self, funcDeclGuards): pass
    @abstractmethod
    def visitDataDecl(self, dataDecl): pass

    # TIPOS
    @abstractmethod
    def visitSimpleType(self, simpleType): pass
    @abstractmethod
    def visitArrowType(self, arrowType): pass
    @abstractmethod
    def visitListType(self, listType): pass
    @abstractmethod
    def visitTupleType(self, tupleType): pass
    @abstractmethod
    def visitUnitType(self, unitType): pass

    # CONSTRUTORES DE DADOS
    @abstractmethod
    def visitConstructor(self, constructor): pass
    @abstractmethod
    def visitConstructorArgs(self, constructorArgs): pass

    # GUARDAS
    @abstractmethod
    def visitGuard(self, guard): pass
    @abstractmethod
    def visitSingleGuards(self, singleGuards): pass
    @abstractmethod
    def visitCompoundGuards(self, compoundGuards): pass

    # DECLARAÇÕES LOCAIS
    @abstractmethod
    def visitSingleLocaldecl(self, singleLocaldecl): pass
    @abstractmethod
    def visitCompoundLocaldecl(self, compoundLocaldecl): pass

    # EXPRESSÕES
    @abstractmethod
    def visitVarExp(self, varExp): pass
    @abstractmethod
    def visitConExp(self, conExp): pass
    @abstractmethod
    def visitIntExp(self, intExp): pass
    @abstractmethod
    def visitBoolExp(self, boolExp): pass
    @abstractmethod
    def visitCharExp(self, charExp): pass
    @abstractmethod
    def visitStringExp(self, stringExp): pass
    @abstractmethod
    def visitAppExp(self, appExp): pass
    @abstractmethod
    def visitInfixExp(self, infixExp): pass
    @abstractmethod
    def visitNegExp(self, negExp): pass
    @abstractmethod
    def visitNotExp(self, notExp): pass
    @abstractmethod
    def visitIfExp(self, ifExp): pass
    @abstractmethod
    def visitCaseExp(self, caseExp): pass
    @abstractmethod
    def visitLetExp(self, letExp): pass
    @abstractmethod
    def visitDoExp(self, doExp): pass
    @abstractmethod
    def visitLambdaExp(self, lambdaExp): pass
    @abstractmethod
    def visitListExp(self, listExp): pass
    @abstractmethod
    def visitEmptyListExp(self, emptyListExp): pass
    @abstractmethod
    def visitRangeExp(self, rangeExp): pass
    @abstractmethod
    def visitTupleExp(self, tupleExp): pass

    # ALTERNATIVAS DE CASE
    @abstractmethod
    def visitSingleCaseAlts(self, singleCaseAlts): pass
    @abstractmethod
    def visitCompoundCaseAlts(self, compoundCaseAlts): pass
    @abstractmethod
    def visitCaseAlt(self, caseAlt): pass

    # COMANDOS DO BLOCO DO
    @abstractmethod
    def visitSingleDoStmts(self, singleDoStmts): pass
    @abstractmethod
    def visitCompoundDoStmts(self, compoundDoStmts): pass
    @abstractmethod
    def visitBindStmt(self, bindStmt): pass
    @abstractmethod
    def visitLetDoStmt(self, letDoStmt): pass
    @abstractmethod
    def visitExprDoStmt(self, exprDoStmt): pass

    # PADRÕES
    @abstractmethod
    def visitWildcardPat(self, wildcardPat): pass
    @abstractmethod
    def visitVarPat(self, varPat): pass
    @abstractmethod
    def visitConPat(self, conPat): pass
    @abstractmethod
    def visitIntPat(self, intPat): pass
    @abstractmethod
    def visitBoolPat(self, boolPat): pass
    @abstractmethod
    def visitCharPat(self, charPat): pass
    @abstractmethod
    def visitConsPat(self, consPat): pass
    @abstractmethod
    def visitTuplePat(self, tuplePat): pass
    @abstractmethod
    def visitListPat(self, listPat): pass
    @abstractmethod
    def visitEmptyListPat(self, emptyListPat): pass


class Visitor(AbstractVisitor):

    # PROGRAMA

    def visitSingleDecl(self, singleDecl):
        singleDecl.decl.accept(self)

    def visitCompoundDecl(self, compoundDecl):
        compoundDecl.decl.accept(self)
        print()
        compoundDecl.program.accept(self)

    # DECLARAÇÕES

    def visitTypeSig(self, typeSig):
        print(blank(), typeSig.name, ' :: ', sep='', end='')
        typeSig.type_expr.accept(self)
        print()

    def visitFuncDecl(self, funcDecl):
        print(blank(), funcDecl.name, sep='', end='')
        for pat in funcDecl.pats:
            print(' ', end='')
            pat.accept(self)
        print(' = ', end='')
        funcDecl.body.accept(self)
        print()

    def visitFuncDeclWhere(self, funcDeclWhere):
        global tab
        print(blank(), funcDeclWhere.name, sep='', end='')
        for pat in funcDeclWhere.pats:
            print(' ', end='')
            pat.accept(self)
        print(' = ', end='')
        funcDeclWhere.body.accept(self)
        print()
        tab = tab + 4
        print(blank(), 'where', sep='')
        tab = tab + 4
        funcDeclWhere.where_decls.accept(self)
        tab = tab - 8

    def visitFuncDeclGuards(self, funcDeclGuards):
        print(blank(), funcDeclGuards.name, sep='', end='')
        for pat in funcDeclGuards.pats:
            print(' ', end='')
            pat.accept(self)
        print()
        funcDeclGuards.guards.accept(self)

    def visitDataDecl(self, dataDecl):
        print(blank(), 'data ', dataDecl.name, ' = ', sep='', end='')
        for i, ctor in enumerate(dataDecl.constructors):
            if i > 0:
                print(' | ', end='')
            ctor.accept(self)
        print()

    # TIPOS

    def visitSimpleType(self, simpleType):
        print(simpleType.name, end='')

    def visitArrowType(self, arrowType):
        arrowType.left.accept(self)
        print(' -> ', end='')
        arrowType.right.accept(self)

    def visitListType(self, listType):
        print('[', end='')
        listType.elem.accept(self)
        print(']', end='')

    def visitTupleType(self, tupleType):
        print('(', end='')
        for i, t in enumerate(tupleType.types):
            if i > 0:
                print(', ', end='')
            t.accept(self)
        print(')', end='')

    def visitUnitType(self, unitType):
        print('()', end='')

    # CONSTRUTORES DE DADOS

    def visitConstructor(self, constructor):
        print(constructor.name, end='')

    def visitConstructorArgs(self, constructorArgs):
        print(constructorArgs.name, end='')
        for item in constructorArgs.types:
            print(' ', end='')
            if isinstance(item, str):
                print(item, end='')
            else:
                item.accept(self)

    # GUARDAS

    def visitGuard(self, guard):
        global tab
        tab = tab + 4
        print(blank(), '| ', sep='', end='')
        tab = tab - 4
        guard.cond.accept(self)
        print(' = ', end='')
        guard.body.accept(self)
        print()

    def visitSingleGuards(self, singleGuards):
        singleGuards.guard.accept(self)

    def visitCompoundGuards(self, compoundGuards):
        compoundGuards.guards.accept(self)
        compoundGuards.guard.accept(self)

    # DECLARAÇÕES LOCAIS

    def visitSingleLocaldecl(self, singleLocaldecl):
        singleLocaldecl.decl.accept(self)

    def visitCompoundLocaldecl(self, compoundLocaldecl):
        compoundLocaldecl.decls.accept(self)
        compoundLocaldecl.decl.accept(self)

    # EXPRESSÕES

    def visitVarExp(self, varExp):
        print(varExp.name, end='')

    def visitConExp(self, conExp):
        print(conExp.name, end='')

    def visitIntExp(self, intExp):
        print(intExp.value, end='')

    def visitBoolExp(self, boolExp):
        print(boolExp.value, end='')

    def visitCharExp(self, charExp):
        print("'", charExp.value, "'", sep='', end='')

    def visitStringExp(self, stringExp):
        print('"', stringExp.value, '"', sep='', end='')

    def visitAppExp(self, appExp):
        appExp.func.accept(self)
        print(' ', end='')
        appExp.arg.accept(self)

    def visitInfixExp(self, infixExp):
        infixExp.left.accept(self)
        print(' ', infixExp.op, ' ', sep='', end='')
        infixExp.right.accept(self)

    def visitNegExp(self, negExp):
        print('-', end='')
        negExp.expr.accept(self)

    def visitNotExp(self, notExp):
        print('not ', end='')
        notExp.expr.accept(self)

    def visitIfExp(self, ifExp):
        print('if ', end='')
        ifExp.cond.accept(self)
        print(' then ', end='')
        ifExp.then_e.accept(self)
        print(' else ', end='')
        ifExp.else_e.accept(self)

    def visitCaseExp(self, caseExp):
        global tab
        print('case ', end='')
        caseExp.expr.accept(self)
        print(' of')
        tab = tab + 4
        caseExp.alts.accept(self)
        tab = tab - 4

    def visitLetExp(self, letExp):
        global tab
        print('let')
        tab = tab + 4
        letExp.decls.accept(self)
        tab = tab - 4
        print(blank(), 'in ', sep='', end='')
        letExp.body.accept(self)

    def visitDoExp(self, doExp):
        global tab
        print('do')
        tab = tab + 4
        doExp.stmts.accept(self)
        tab = tab - 4

    def visitLambdaExp(self, lambdaExp):
        print('\\', end='')
        for i, pat in enumerate(lambdaExp.pats):
            if i > 0:
                print(' ', end='')
            pat.accept(self)
        print(' -> ', end='')
        lambdaExp.body.accept(self)

    def visitListExp(self, listExp):
        print('[', end='')
        for i, elem in enumerate(listExp.elems):
            if i > 0:
                print(', ', end='')
            elem.accept(self)
        print(']', end='')

    def visitEmptyListExp(self, emptyListExp):
        print('[]', end='')

    def visitRangeExp(self, rangeExp):
        print('[', end='')
        rangeExp.start.accept(self)
        print('..', end='')
        if rangeExp.end is not None:
            rangeExp.end.accept(self)
        print(']', end='')

    def visitTupleExp(self, tupleExp):
        print('(', end='')
        for i, elem in enumerate(tupleExp.elems):
            if i > 0:
                print(', ', end='')
            elem.accept(self)
        print(')', end='')

    # ALTERNATIVAS DE CASE

    def visitSingleCaseAlts(self, singleCaseAlts):
        singleCaseAlts.alt.accept(self)

    def visitCompoundCaseAlts(self, compoundCaseAlts):
        compoundCaseAlts.alts.accept(self)
        compoundCaseAlts.alt.accept(self)

    def visitCaseAlt(self, caseAlt):
        print(blank(), sep='', end='')
        caseAlt.pat.accept(self)
        print(' -> ', end='')
        caseAlt.body.accept(self)
        print()

    # COMANDOS DO BLOCO DO

    def visitSingleDoStmts(self, singleDoStmts):
        singleDoStmts.stmt.accept(self)

    def visitCompoundDoStmts(self, compoundDoStmts):
        compoundDoStmts.stmts.accept(self)
        compoundDoStmts.stmt.accept(self)

    def visitBindStmt(self, bindStmt):
        print(blank(), bindStmt.var, ' <- ', sep='', end='')
        bindStmt.expr.accept(self)
        print()

    def visitLetDoStmt(self, letDoStmt):
        global tab
        print(blank(), 'let', sep='')
        tab = tab + 4
        letDoStmt.decls.accept(self)
        tab = tab - 4

    def visitExprDoStmt(self, exprDoStmt):
        print(blank(), sep='', end='')
        exprDoStmt.expr.accept(self)
        print()

    # PADRÕES

    def visitWildcardPat(self, wildcardPat):
        print('_', end='')

    def visitVarPat(self, varPat):
        print(varPat.name, end='')

    def visitConPat(self, conPat):
        print(conPat.name, end='')

    def visitIntPat(self, intPat):
        print(intPat.value, end='')

    def visitBoolPat(self, boolPat):
        print(boolPat.value, end='')

    def visitCharPat(self, charPat):
        print("'", charPat.value, "'", sep='', end='')

    def visitConsPat(self, consPat):
        print('(', end='')
        consPat.head.accept(self)
        print(':', end='')
        consPat.tail.accept(self)
        print(')', end='')

    def visitTuplePat(self, tuplePat):
        print('(', end='')
        for i, pat in enumerate(tuplePat.pats):
            if i > 0:
                print(', ', end='')
            pat.accept(self)
        print(')', end='')

    def visitListPat(self, listPat):
        print('[', end='')
        for i, pat in enumerate(listPat.pats):
            if i > 0:
                print(', ', end='')
            pat.accept(self)
        print(']', end='')

    def visitEmptyListPat(self, emptyListPat):
        print('[]', end='')


def main():
    f = open("input1.hs", "r")
    data = f.read()
    f.close()
    lexer = HaskellLexer()
    parser = yacc.yacc()
    result = parser.parse('\n' + data, lexer=lexer)
    print("# imprime o programa que foi passado como entrada")
    visitor = Visitor()
    result.accept(visitor)

if __name__ == "__main__":
    main()
