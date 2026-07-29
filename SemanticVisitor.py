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

    
    def visitFuncDecl(self, funcDecl):
        if self.em_escopo_local:
            st.addVar(funcDecl.name, st.UNKNOWN)
            for i in funcDecl.pats:
                i.accept(self)
            funcDecl.body.accept(self)
        else:
            if st.getBindable(funcDecl.name) is None:
                st.addFunction(funcDecl.name, [], st.UNKNOWN)
            st.beginScope(funcDecl.name)
            for i in funcDecl.pats:
                i.accept(self)
            funcDecl.body.accept(self)
            st.endScope()   
       

    def visitFuncDeclWhere(self, funcDeclWhere):
        if self.em_escopo_local:
            # Declaracao aninhada dentro de outro where/let: o nome entra no
            # escopo corrente e NENHUM escopo novo e aberto, logo tambem nao
            # pode haver endScope() ao final.
            st.addVar(funcDeclWhere.name, st.UNKNOWN)
            for i in funcDeclWhere.pats:
                i.accept(self)
            anterior = self.em_escopo_local
            self.em_escopo_local = True
            funcDeclWhere.where_decls.accept(self)
            self.em_escopo_local = anterior
            funcDeclWhere.body.accept(self)
        else:
            # Declaracao de alto nivel: abre escopo proprio e o fecha ao final.
            if st.getBindable(funcDeclWhere.name) is None:
                st.addFunction(funcDeclWhere.name, [], st.UNKNOWN)
            st.beginScope(funcDeclWhere.name)
            for i in funcDeclWhere.pats:
                i.accept(self)
            anterior = self.em_escopo_local
            self.em_escopo_local = True
            funcDeclWhere.where_decls.accept(self)
            self.em_escopo_local = anterior
            funcDeclWhere.body.accept(self)
            st.endScope()



    def visitFuncDeclGuards(self, funcDeclGuards):
        if self.em_escopo_local:
            st.addVar(funcDeclGuards.name, st.UNKNOWN)
            for i in funcDeclGuards.pats:
                i.accept(self)
            funcDeclGuards.guards.accept(self)
        else:
            if st.getBindable(funcDeclGuards.name) is None:
                st.addFunction(funcDeclGuards.name, [], st.UNKNOWN)
            st.beginScope(funcDeclGuards.name)
            for i in funcDeclGuards.pats:
                i.accept(self)
            funcDeclGuards.guards.accept(self)
            st.endScope()
        

    def visitDataDecl(self, dataDecl):
        for i in dataDecl.constructors:
            i.accept(self)
        

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

    def visitGuard(self, guard):
        tipoCond = guard.cond.accept(self)
        if tipoCond not in [st.BOOL, st.UNKNOWN]:
            self.n_errors += 1
            print('\t[Erro] Condicao da guarda deve ser booleana. Encontrado:', tipoCond)
        guard.body.accept(self)

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

    # Operadores agrupados por exigencia de tipo dos operandos
    OPS_ARITMETICOS  = ['+', '-', '*', '/', '^', 'div', 'mod']
    OPS_LOGICOS      = ['&&', '||']
    OPS_RELACIONAIS  = ['==', '/=', '<', '<=', '>', '>=']

    def _exigir(self, tipo, esperado, op, lado):
        """Reporta erro se 'tipo' nao for 'esperado' nem desconhecido."""
        if tipo in [esperado, st.UNKNOWN]:
            return True
        self.n_errors += 1
        print('\t[Erro] Operando ' + lado + ' de "' + op + '" deve ser '
              + esperado + '. Encontrado:', tipo)
        return False

    def visitInfixExp(self, infixExp):
        op = infixExp.op
        tipoEsq = infixExp.left.accept(self)
        tipoDir = infixExp.right.accept(self)

        if op in self.OPS_ARITMETICOS:
            self._exigir(tipoEsq, st.INT, op, 'esquerdo')
            self._exigir(tipoDir, st.INT, op, 'direito')
            return st.INT

        if op in self.OPS_LOGICOS:
            self._exigir(tipoEsq, st.BOOL, op, 'esquerdo')
            self._exigir(tipoDir, st.BOOL, op, 'direito')
            return st.BOOL

        if op in self.OPS_RELACIONAIS:
            # Nao exige um tipo fixo: exige que os dois lados sejam comparaveis
            if compativel(tipoEsq, tipoDir) is None:
                self.n_errors += 1
                print('\t[Erro] Comparacao invalida com "' + op + '": lado '
                      'esquerdo eh do tipo', tipoEsq, 'e o direito eh do tipo',
                      tipoDir)
            return st.BOOL

        if op == '++':
            # So consegue checar quando os dois lados tem tipo conhecido;
            # listas literais devolvem 'desconhecido' e passam sem erro.
            tipoResult = compativel(tipoEsq, tipoDir)
            if tipoResult is None:
                self.n_errors += 1
                print('\t[Erro] Concatenacao invalida: lado esquerdo eh do tipo',
                      tipoEsq, 'e o direito eh do tipo', tipoDir)
                return st.UNKNOWN
            return tipoResult

        # ':' (cons), '.' (composicao) e '$' (aplicacao) nao sao verificados:
        # exigiriam tipos de lista e de funcao, fora do escopo deste subconjunto.
        return st.UNKNOWN

    def visitNegExp(self, negExp):
        tipo = negExp.expr.accept(self)
        if tipo not in [st.INT, st.UNKNOWN]:
            self.n_errors += 1
            print('\t[Erro] Expressao negada deve ser numerica. Encontrado:', tipo)
        return st.INT

    def visitNotExp(self, notExp):
        tipo = notExp.expr.accept(self)
        if tipo not in [st.BOOL, st.UNKNOWN]:
            self.n_errors += 1
            print('\t[Erro] Expressao do NOT deve ser booleana. Encontrado:', tipo)
        return st.BOOL

    def visitIfExp(self, ifExp):
        tipoCond = ifExp.cond.accept(self)
        if tipoCond not in [st.BOOL, st.UNKNOWN]:
            self.n_errors += 1
            print('\t[Erro] Condicao do IF deve ser booleana. Encontrado:', tipoCond)
        tipoThen = ifExp.then_e.accept(self)
        tipoElse = ifExp.else_e.accept(self)
        tipoResult = compativel(tipoThen, tipoElse)
        if tipoResult is None:
            self.n_errors += 1
            print('\t[Erro] Tipos das ramificacoes THEN e ELSE sao incompativeis no IF.')
            return st.UNKNOWN
        return tipoResult

    def visitCaseExp(self, caseExp):
        caseExp.expr.accept(self)
        caseExp.alts.accept(self)
        return st.UNKNOWN

    def visitLetExp(self, letExp):
        st.beginScope('let')
        anterior = self.em_escopo_local
        self.em_escopo_local = True
        letExp.decls.accept(self)
        self.em_escopo_local = anterior
        tipoResult = letExp.body.accept(self)
        st.endScope()
        return tipoResult

    def visitDoExp(self, doExp):
        st.beginScope('do')
        doExp.stmts.accept(self)
        st.endScope()
        return st.UNKNOWN
        
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

    def pre_registrar(self, node):
        import SintaxeAbstrata as sa
        if isinstance(node, sa.SingleDecl):
            self.pre_registrar(node.decl)
        elif isinstance(node, sa.CompoundDecl):
            self.pre_registrar(node.decl)
            self.pre_registrar(node.program)
        elif isinstance(node, (sa.FuncDecl, sa.FuncDeclWhere, sa.FuncDeclGuards)):
            if st.getBindable(node.name) is None:
                st.addVar(node.name, st.UNKNOWN)

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
    svisitor.pre_registrar(result)
    result.accept(svisitor)
    print(f"\nForam encontrados {svisitor.getnerros()} erro(s) semantico(s)")

if __name__ == "__main__":
    main()