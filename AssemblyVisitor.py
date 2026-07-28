from Visitor import AbstractVisitor
import AssemblyST as st
import SintaxeAbstrata as sa
import ply.yacc as yacc
import ExpressionLanguageParser as p
from ExpressionLanguageLex import HaskellLexer

# Rótulo único de destino quando nenhuma equação/alternativa 
# bate com o valor em tempo de execução
# aborta o programa em vez de emitir uma mensagem de erro
ERRO_PADRAO_LABEL = "__erro_padrao_nao_exaustivo__"

class AssemblyVisitor(AbstractVisitor):

    def __init__(self):
        st.beginScope(st.SCOPE_MAIN)
        self.text = [] # código do main (fica solto no .text)
        self.text.append(".text")
        self.text.append("main:") # ponto de entrada exigido pelo spim/MARS
        self.text.append("    move $fp, $sp")
        self.funcs = [] # código de todas as outras funções
        self.data = [] # constantes .data (só strings, por enquanto)
        self._rotulos = {} # contador de sufixo por prefixo de rótulo
        self._decls = [] # populada por visitSingleDecl/visitCompoundDecl
        self._destino = self.funcs # reapontado em _gerar_main / _gerar_funcao
        self._menor_sp = 0

    # Utilidades gerais
    def novo_rotulo(self, prefixo):
        n = self._rotulos.get(prefixo, 0)
        self._rotulos[prefixo] = n + 1
        return f"{prefixo}_{n}"

    def getList(self):
        return self._destino

    def novo_rotulo_string(self, valor):
        rotulo = self.novo_rotulo("str")
        escapado = valor.replace('\\', '\\\\').replace('"', '\\"')
        self.data.append(f'    {rotulo}: .asciiz "{escapado}"')
        return rotulo

    # Programa / declarações de topo — só coleta; agrupamento e geração
    # de fato acontecem em generate()
    def visitSingleDecl(self, singleDecl):
        self._decls.append(singleDecl.decl)

    def visitCompoundDecl(self, compoundDecl):
        compoundDecl.decl.accept(self)  # processa a cadeia anterior
        self._decls.append(compoundDecl.program)  # anexa a declaração nova

    def visitTypeSig(self, typeSig):
        pass  # sem efeito em Assembly; só interessava ao semântico

    def visitDataDecl(self, dataDecl):
        raise NotImplementedError(
            "geracao de Assembly para 'data' esta fora do escopo combinado "
            "com o professor (enum e com argumento)."
        )

    # Tipos e construtores: implementados só para satisfazer o AbstractVisitor.
    def visitSimpleType(self, simpleType): pass
    def visitArrowType(self, arrowType): pass
    def visitListType(self, listType): pass
    def visitTupleType(self, tupleType): pass
    def visitUnitType(self, unitType): pass
    def visitConstructor(self, constructor): pass
    def visitConstructorArgs(self, constructorArgs): pass

    # Expressões literais
    def visitIntExp(self, intExp):
        self.getList().append(f"    li $v0, {intExp.value}")

    def visitBoolExp(self, boolExp):
        valor = 1 if boolExp.value in (True, 'True', 'true') else 0
        self.getList().append(f"    li $v0, {valor}")

    def visitCharExp(self, charExp):
        self.getList().append(f"    li $v0, {ord(charExp.value)}")

    def visitStringExp(self, stringExp):
        # String literal: sem heap, mora inteira e estaticamente em .data
        # O "valor" de uma string é o endereço do seu primeiro caractere
        rotulo = self.novo_rotulo_string(stringExp.value)
        self.getList().append(f"    la $v0, {rotulo}")

    # Variável: lê o offset registrado em AssemblyST (parâmetro ou local)
    def visitVarExp(self, varExp):
        offset = st.getOffset(varExp.name)
        if offset is None:
            self._gerar_chamada(varExp.name, [])
        else:
            self.getList().append(f"    lw $v0, {offset}($fp)")

    def visitConExp(self, conExp):
        raise NotImplementedError(
            "geracao de Assembly para construtores de 'data' esta fora do "
            "escopo combinado com o professor."
        )

    # Operadores binários e unários
    _INSTR_ARITMETICA = {
        '+': 'add', '-': 'sub', '*': 'mul',
        '/': 'div', 'div': 'div', 'mod': 'rem',
    }
    _INSTR_RELACIONAL = {
        '<': ('slt', False), '>': ('slt', True),
        # a > b  ==  b < a, então reaproveitamos slt trocando os operandos
        '<=': ('sle', False), '>=': ('sle', True),
        '==': ('seq', False), '/=': ('sne', False),
    }

    def _empilhar_backup(self, exp):
        code = self.getList()
        exp.accept(self)
        code.append("    addi $sp, $sp, -4")
        code.append("    sw $v0, 0($sp)")

    def _recuperar_backup(self):
        code = self.getList()
        code.append("    lw $t0, 0($sp)")
        code.append("    addi $sp, $sp, 4")

    def visitInfixExp(self, infixExp):
        op = infixExp.op
        code = self.getList()

        if op in ('&&', '||'):
            self._gerar_infixo_logico(infixExp)
            return
        if op == '^':
            self._gerar_potencia(infixExp)
            return

        self._empilhar_backup(infixExp.left)  # esquerda -> pilha
        infixExp.right.accept(self)  # direita -> $v0
        self._recuperar_backup()  # esquerda -> $t0

        if op in self._INSTR_ARITMETICA:
            instr = self._INSTR_ARITMETICA[op]
            code.append(f"    {instr} $v0, $t0, $v0")
        elif op in self._INSTR_RELACIONAL:
            instr, inverte = self._INSTR_RELACIONAL[op]
            a, b = ('$v0', '$t0') if inverte else ('$t0', '$v0')
            if instr == 'slt':
                code.append(f"    slt $v0, {a}, {b}")
            elif instr == 'sle':
                # a <= b  ==  !(b < a)
                code.append(f"    slt $v0, {b}, {a}")
                code.append("    xori $v0, $v0, 1")
            elif instr == 'seq':
                code.append(f"    seq $v0, {a}, {b}")
            elif instr == 'sne':
                code.append(f"    sne $v0, {a}, {b}")
        else:
            raise NotImplementedError(
                f"operador '{op}' fora do escopo combinado (cons/composicao/"
                f"aplicacao com $ nao geram Assembly binario direto)."
            )

    def _gerar_infixo_logico(self, infixExp):
        code = self.getList()
        rotulo_fim = self.novo_rotulo("logico_fim")
        infixExp.left.accept(self)  # esquerda -> $v0
        if infixExp.op == '&&':
            # se esquerda == 0 (False), resultado já é False, pula pro fim
            code.append(f"    beq $v0, $zero, {rotulo_fim}")
        else:  # '||'
            # se esquerda != 0 (True), resultado já é True, pula pro fim
            code.append(f"    bne $v0, $zero, {rotulo_fim}")
        infixExp.right.accept(self)  # só avalia se precisar -> $v0
        code.append(f"{rotulo_fim}:")

    def _gerar_potencia(self, infixExp):
        code = self.getList()
        self._empilhar_backup(infixExp.left) # base -> pilha
        infixExp.right.accept(self) # expoente -> $v0
        self._recuperar_backup() # base -> $t0
        code.append("    move $t1, $v0") # $t1 = expoente
        code.append("    li $v0, 1") # $v0 = acumulador = 1
        rotulo_laco = self.novo_rotulo("potencia")
        rotulo_fim = self.novo_rotulo("fim_potencia")
        code.append(f"{rotulo_laco}:")
        code.append(f"    beq $t1, $zero, {rotulo_fim}")
        code.append("    mul $v0, $v0, $t0")
        code.append("    addi $t1, $t1, -1")
        code.append(f"    j {rotulo_laco}")
        code.append(f"{rotulo_fim}:")

    def visitNegExp(self, negExp):
        negExp.expr.accept(self)
        self.getList().append("    sub $v0, $zero, $v0")

    def visitNotExp(self, notExp):
        notExp.expr.accept(self)
        self.getList().append("    xori $v0, $v0, 1")

    def visitAppExp(self, appExp):
        cabeca, args = self._achatar_aplicacao(appExp)
        if isinstance(cabeca, sa.VarExp) and cabeca.name == 'return':
            if len(args) != 1:
                raise NotImplementedError("'return' fora do padrao esperado (1 argumento)")
            args[0].accept(self)  # 'return' e identidade: so avalia o argumento
            return
        if not isinstance(cabeca, sa.VarExp):
            raise NotImplementedError(
                "chamada indireta / funcao de ordem superior fora do escopo "
                "combinado com o professor nesta etapa."
            )
        self._gerar_chamada(cabeca.name, args)

    def _achatar_aplicacao(self, appExp):
        args = []
        node = appExp
        while isinstance(node, sa.AppExp):
            args.insert(0, node.arg)
            node = node.func
        return node, args

    def _gerar_chamada(self, nome, arg_exprs):
        code = self.getList()
        n = len(arg_exprs)
        for arg_exp in arg_exprs:
            arg_exp.accept(self) # valor -> $v0
            code.append("    addi $sp, $sp, -4")
            code.append("    sw $v0, 0($sp)")
        code.append(f"    jal {nome}")
        if n:
            code.append(f"    addi $sp, $sp, {4 * n}")

    # if-then-else: EXPRESSÃO (não comando)
    def visitIfExp(self, ifExp):
        code = self.getList()
        rotulo_else = self.novo_rotulo("if_else")
        rotulo_fim = self.novo_rotulo("if_fim")
        ifExp.cond.accept(self)
        code.append(f"    beq $v0, $zero, {rotulo_else}")
        ifExp.then_e.accept(self)
        code.append(f"    j {rotulo_fim}")
        code.append(f"{rotulo_else}:")
        ifExp.else_e.accept(self)
        code.append(f"{rotulo_fim}:")

    # Escopos aninhados (let / case / do): usam beginNestedScope porque
    # convivem, na mesma execução, com locais já alocados por fora
    def _fechar_escopo(self):
        self._menor_sp = min(self._menor_sp, st.getSP())
        st.endScope()

    # where / let
    def visitSingleLocaldecl(self, singleLocaldecl):
        self._gerar_um_local(singleLocaldecl.decl)

    def visitCompoundLocaldecl(self, compoundLocaldecl):
        compoundLocaldecl.decls.accept(self)   # os anteriores, em ordem
        self._gerar_um_local(compoundLocaldecl.decl)  # o mais novo, por ultimo

    def _gerar_um_local(self, decl):
        if isinstance(decl, sa.TypeSig):
            return
        if not isinstance(decl, (sa.FuncDecl, sa.FuncDeclWhere, sa.FuncDeclGuards)):
            raise NotImplementedError(f"declaracao local nao suportada: {type(decl).__name__}")
        if decl.pats:
            raise NotImplementedError(
                f"'{decl.name}': funcao local com parametro dentro de "
                "where/let exigiria closure (static link), que ficou fora "
                "do escopo combinado nesta etapa."
            )
        self._gerar_corpo_equacao(decl) # deixa o valor em $v0
        st.addVar(decl.name)
        offset = st.getOffset(decl.name)
        self.getList().append(f"    sw $v0, {offset}($fp)")

    def visitLetExp(self, letExp):
        st.beginNestedScope(self.novo_rotulo("let"))
        letExp.decls.accept(self)
        letExp.body.accept(self) # valor final -> $v0
        self._fechar_escopo()

    # do: sequência de comandos. Só o valor do ÚLTIMO importa 
    # Sem syscall de E/S 
    def visitDoExp(self, doExp):
        st.beginNestedScope(self.novo_rotulo("do"))
        doExp.stmts.accept(self)
        self._fechar_escopo()

    def visitSingleDoStmts(self, singleDoStmts):
        singleDoStmts.stmt.accept(self)

    def visitCompoundDoStmts(self, compoundDoStmts):
        compoundDoStmts.stmts.accept(self)
        compoundDoStmts.stmt.accept(self)

    def visitLetDoStmt(self, letDoStmt):
        letDoStmt.decls.accept(self)

    def visitBindStmt(self, bindStmt):
        bindStmt.expr.accept(self)
        st.addVar(bindStmt.var)
        offset = st.getOffset(bindStmt.var)
        self.getList().append(f"    sw $v0, {offset}($fp)")

    def visitExprDoStmt(self, exprDoStmt):
        exprDoStmt.expr.accept(self)

    # guardas: cascata de testes, cada um pulando pro próximo se a
    # condição for falsa; 'otherwise' é tratado como sempre-verdadeiro,
    # sem gerar teste
    def _lista_guardas(self, node):
        if isinstance(node, sa.SingleGuards):
            return [node.guard]
        return self._lista_guardas(node.guards) + [node.guard]

    def _gerar_guardas(self, guards_node):
        code = self.getList()
        guardas = self._lista_guardas(guards_node)
        rotulo_fim = self.novo_rotulo("guarda_fim")
        for i, g in enumerate(guardas):
            eh_ultima = (i == len(guardas) - 1)
            eh_otherwise = isinstance(g.cond, sa.VarExp) and g.cond.name == 'otherwise'
            rotulo_prox = None if (eh_ultima or eh_otherwise) else self.novo_rotulo("guarda_prox")
            if not eh_otherwise:
                g.cond.accept(self)
                alvo_falha = rotulo_prox if rotulo_prox else ERRO_PADRAO_LABEL
                code.append(f"    beq $v0, $zero, {alvo_falha}")
            g.body.accept(self)
            code.append(f"    j {rotulo_fim}")
            if rotulo_prox:
                code.append(f"{rotulo_prox}:")
        code.append(f"{rotulo_fim}:")

    # Métodos exigidos pelo AbstractVisitor, mas não usados via accept()
    def visitGuard(self, guard): pass
    def visitSingleGuards(self, singleGuards): pass
    def visitCompoundGuards(self, compoundGuards): pass

    # case-of: mesma lógica de cascata das guardas/equações, 
    # só que testando padrão em vez de condição.
    def _lista_alts(self, node):
        if isinstance(node, sa.SingleCaseAlts):
            return [node.alt]
        return self._lista_alts(node.alts) + [node.alt]

    def visitCaseExp(self, caseExp):
        code = self.getList()
        caseExp.expr.accept(self) # escrutinado -> $v0
        rotulo_tmp = self.novo_rotulo("case_tmp")
        st.addVar(rotulo_tmp)
        offset_escrutinado = st.getOffset(rotulo_tmp)
        code.append(f"    sw $v0, {offset_escrutinado}($fp)")

        alts = self._lista_alts(caseExp.alts)
        rotulo_fim = self.novo_rotulo("case_fim")
        for i, alt in enumerate(alts):
            eh_ultima = (i == len(alts) - 1)
            rotulo_prox = None if eh_ultima else self.novo_rotulo("case_alt")
            st.beginNestedScope(self.novo_rotulo("case_corpo"))
            self._testar_padrao(alt.pat, offset_escrutinado, rotulo_prox)
            alt.body.accept(self)
            code.append(f"    j {rotulo_fim}")
            self._fechar_escopo()
            if rotulo_prox:
                code.append(f"{rotulo_prox}:")
        code.append(f"{rotulo_fim}:")

    # Métodos exigidos pelo AbstractVisitor, mas não usados via accept()
    def visitSingleCaseAlts(self, singleCaseAlts): pass
    def visitCompoundCaseAlts(self, compoundCaseAlts): pass
    def visitCaseAlt(self, caseAlt): pass

    # Padrões: usados tanto pelas alternativas de 'case' quanto pelos
    # argumentos posicionais de uma equação de função (_gerar_testes_
    # padroes_equacao)
    def _testar_padrao(self, pat, offset, rotulo_falha):
        self._offset_padrao_atual = offset
        self._rotulo_falha_atual = rotulo_falha if rotulo_falha else ERRO_PADRAO_LABEL
        pat.accept(self)

    def visitWildcardPat(self, wildcardPat):
        pass  # sempre bate, sem teste, sem binding

    def visitVarPat(self, varPat):
        # alias direto pro mesmo slot do valor -- sem copiar nada
        st.addVar(varPat.name, self._offset_padrao_atual)

    def _testar_literal(self, valor):
        code = self.getList()
        code.append(f"    lw $t0, {self._offset_padrao_atual}($fp)")
        code.append(f"    li $t1, {valor}")
        code.append(f"    bne $t0, $t1, {self._rotulo_falha_atual}")

    def visitIntPat(self, intPat):
        self._testar_literal(intPat.value)

    def visitBoolPat(self, boolPat):
        valor = 1 if boolPat.value in (True, 'True', 'true') else 0
        self._testar_literal(valor)

    def visitCharPat(self, charPat):
        self._testar_literal(ord(charPat.value))

    def visitConPat(self, conPat):
        raise NotImplementedError("padrao de construtor fora do escopo combinado (data)")

    def visitConsPat(self, consPat):
        raise NotImplementedError("padrao (x:xs) fora do escopo combinado (lista)")

    def visitTuplePat(self, tuplePat):
        raise NotImplementedError("padrao de tupla fora do escopo combinado")

    def visitListPat(self, listPat):
        raise NotImplementedError("padrao de lista fora do escopo combinado")

    def visitEmptyListPat(self, emptyListPat):
        raise NotImplementedError("padrao de lista vazia fora do escopo combinado")

    # Construções fora do escopo combinado com o professor (lista, tupla,
    # range, lambda/closure)
    # Implementadas só pra satisfazer o AbstractVisitor

    def visitLambdaExp(self, lambdaExp):
        raise NotImplementedError(
            "funcao anonima/closure fora do escopo combinado com o "
            "professor nesta etapa."
        )

    def visitListExp(self, listExp):
        raise NotImplementedError("lista fora do escopo combinado")

    def visitEmptyListExp(self, emptyListExp):
        raise NotImplementedError("lista fora do escopo combinado")

    def visitRangeExp(self, rangeExp):
        raise NotImplementedError("range/lista fora do escopo combinado")

    def visitTupleExp(self, tupleExp):
        raise NotImplementedError("tupla fora do escopo combinado")

    # Equações de função
    def _offsets_posicionais(self, aridade):
        return [8 + 4 * (aridade - 1 - i) for i in range(aridade)]

    def _gerar_corpo_equacao(self, eq):
        if isinstance(eq, sa.FuncDecl):
            eq.body.accept(self)
        elif isinstance(eq, sa.FuncDeclWhere):
            eq.where_decls.accept(self) # entra no MESMO escopo corrente
            eq.body.accept(self)
        elif isinstance(eq, sa.FuncDeclGuards):
            self._gerar_guardas(eq.guards)
        else:
            raise NotImplementedError(f"tipo de equacao nao suportado: {type(eq).__name__}")

    # Métodos exigidos pelo AbstractVisitor, mas não usados via accept()
    # driver generate() agrupa as equações por nome e as processa
    # manualmente em _gerar_funcao/_gerar_main 
    def visitFuncDecl(self, funcDecl): pass
    def visitFuncDeclWhere(self, funcDeclWhere): pass
    def visitFuncDeclGuards(self, funcDeclGuards): pass

    def _gerar_epilogo_funcao(self):
        code = self.funcs
        code.append("    move $sp, $fp")   # libera os locais
        code.append("    lw $ra, 4($fp)")  # nosso proprio $ra
        code.append("    lw $fp, 0($fp)")  # $fp do chamador (por ultimo)
        code.append("    addi $sp, $sp, 8")  # libera so o NOSSO backup de ra/fp;
        code.append("    jr $ra")

    def _gerar_funcao(self, nome, equacoes):
        aridade = len(equacoes[0].pats)
        offsets = self._offsets_posicionais(aridade)

        self._destino = self.funcs
        self.funcs.append(f"{nome}:")
        # PRÓLOGO: salva o $ra fresco (que o 'jal' que nos chamou acabou
        # de ajustar) e o $fp do chamador, SÓ ENTÃO estabelece nosso
        # próprio $fp
        self.funcs.append("    addi $sp, $sp, -8")
        self.funcs.append("    sw $ra, 4($sp)")
        self.funcs.append("    sw $fp, 0($sp)")
        self.funcs.append("    move $fp, $sp")
        idx_placeholder = len(self.funcs)
        self.funcs.append(None)  # retrocesso mais abaixo
        self._menor_sp = 0

        for i, eq in enumerate(equacoes):
            eh_ultima = (i == len(equacoes) - 1)
            rotulo_prox = None if eh_ultima else self.novo_rotulo(f"{nome}_eq")
            st.beginScope(f"{nome}_eq{i}")
            for pat, offset in zip(eq.pats, offsets):
                self._testar_padrao(pat, offset, rotulo_prox)
            self._gerar_corpo_equacao(eq)
            self._gerar_epilogo_funcao()
            self._fechar_escopo()
            if rotulo_prox:
                self.funcs.append(f"{rotulo_prox}:")

        self.funcs[idx_placeholder] = f"    addi $sp, $sp, {self._menor_sp}"

    def _gerar_main(self, equacoes):
        # 'main' não é uma função chamável: seu código fica direto no
        # .text, executado a partir do topo do programa
        self._destino = self.text
        idx_placeholder = len(self.text)
        self.text.append(None)
        self._menor_sp = 0
        self._gerar_corpo_equacao(equacoes[0])
        self.text[idx_placeholder] = f"    addi $sp, $sp, {self._menor_sp}"

    # Driver principal
    def generate(self, ast):
        ast.accept(self)  # popula self._decls, na ordem do arquivo

        grupos = {}
        ordem = []
        for decl in self._decls:
            if isinstance(decl, (sa.TypeSig, sa.DataDecl)):
                continue
            if decl.name not in grupos:
                grupos[decl.name] = []
                ordem.append(decl.name)
            grupos[decl.name].append(decl)

        for nome in ordem:
            if nome == 'main':
                self._gerar_main(grupos[nome])
            else:
                self._gerar_funcao(nome, grupos[nome])

        return self.get_code()

    def get_code(self):
        linhas = []
        if self.data:
            linhas.append(".data")
            linhas.extend(self.data)
        linhas.extend(self.text)
        linhas.append("    j end")
        linhas.extend(self.funcs)
        linhas.append(f"{ERRO_PADRAO_LABEL}:")
        linhas.append("    li $v0, 10")
        linhas.append("    syscall")
        linhas.append("end:")
        linhas.append("    li $v0, 10")
        linhas.append("    syscall")
        return "\n".join(linhas)

def main():
    f = open("input_assembly.hs", "r")
    data = f.read()
    f.close()
    lexer = HaskellLexer()
    parser = yacc.yacc(module=p)
    result = parser.parse('\n' + data, lexer=lexer)
    print("# Gera Assembly")
    assemblyvisitor = AssemblyVisitor()
    print(assemblyvisitor.generate(result))

if __name__ == '__main__':
    main()