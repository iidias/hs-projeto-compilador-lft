import ply.yacc as yacc
from ExpressionLanguageLex import *
import SintaxeAbstrata as sa

# PRECEDÊNCIA (menor para maior)
precedence = (
    ('right', 'LAMBDA_PREC'),
    ('right', 'DOLAR'),
    ('right', 'OU_LOG'),
    ('right', 'E_LOG'),
    ('nonassoc', 'IGUALDADE', 'DIFERENTE', 'MENOR', 'MAIOR', 'MENOR_EQ', 'MAIOR_EQ'),
    ('right', 'CONS', 'CONCATENA'),
    ('left',  'SOMA', 'SUB'),
    ('left',  'VEZES', 'BARRA', 'DIV', 'MOD'),
    ('right', 'POT'),
    ('right', 'COMPOSICAO'),
    ('right', 'MENOS_UN', 'NAO_UN'),
    ('left',  'APLIC'),
)

# PROGRAMA
def p_program1(p):
    '''program : topdecl'''
    p[0] = sa.SingleDecl(p[1])

def p_program2(p):
    '''program : program VSEP topdecl'''
    p[0] = sa.CompoundDecl(p[1], p[3])

def p_program_trailing(p):
    '''program : program VSEP'''
    p[0] = p[1]

# DECLARAÇÕES DE ALTO NÍVEL
def p_topdecl_typesig(p):
    '''topdecl : typesig'''
    p[0] = p[1]

def p_topdecl_funcdecl(p):
    '''topdecl : funcdecl'''
    p[0] = p[1]

def p_topdecl_datadecl(p):
    '''topdecl : datadecl'''
    p[0] = p[1]

# ASSINATURAS DE TIPO
def p_typesig(p):
    '''typesig : ID_MIN ANOTACAO typeexpr'''
    p[0] = sa.TypeSig(p[1], p[3])

def p_typeexpr_arrow(p):
    '''typeexpr : typeterm SETA typeexpr'''
    p[0] = sa.ArrowType(p[1], p[3])

def p_typeexpr_term(p):
    '''typeexpr : typeterm'''
    p[0] = p[1]

def p_typeterm_upper(p):
    '''typeterm : ID_MAI'''
    p[0] = sa.SimpleType(p[1])

def p_typeterm_lower(p):
    '''typeterm : ID_MIN'''
    p[0] = sa.SimpleType(p[1])

def p_typeterm_paren(p):
    '''typeterm : LPAREN typeexpr RPAREN'''
    p[0] = p[2]

def p_typeterm_unit(p):
    '''typeterm : LPAREN RPAREN'''
    p[0] = sa.UnitType()

def p_typeterm_list(p):
    '''typeterm : LCOLCH typeexpr RCOLCH'''
    p[0] = sa.ListType(p[2])

def p_typeterm_app(p):
    '''typeterm : ID_MAI typeterm'''
    p[0] = sa.SimpleType(p[1] + ' ' + str(p[2]))

# DECLARAÇÕES DE TIPO ALGÉBRICO
def p_datadecl(p):
    '''datadecl : DATA ID_MAI IGUAL constructorlist'''
    p[0] = sa.DataDecl(p[2], p[4])

def p_constructorlist1(p):
    '''constructorlist : constructor'''
    p[0] = [p[1]]

def p_constructorlist2(p):
    '''constructorlist : constructorlist BARRA_VERT constructor'''
    p[0] = p[1] + [p[3]]

def p_constructor1(p):
    '''constructor : ID_MAI'''
    p[0] = sa.Constructor(p[1])

def p_constructor2(p):
    '''constructor : ID_MAI typeatoms'''
    p[0] = sa.ConstructorArgs(p[1], p[2])

def p_typeatoms1(p):
    '''typeatoms : ID_MAI'''
    p[0] = [p[1]]

def p_typeatoms2(p):
    '''typeatoms : typeatoms ID_MAI'''
    p[0] = p[1] + [p[2]]

# DEFINIÇÕES DE FUNÇÃO
def p_funcdecl1(p):
    '''funcdecl : ID_MIN IGUAL expr'''
    p[0] = sa.FuncDecl(p[1], [], p[3])

def p_funcdecl2(p):
    '''funcdecl : ID_MIN simplepats IGUAL expr'''
    p[0] = sa.FuncDecl(p[1], p[2], p[4])

def p_funcdecl3(p):
    '''funcdecl : ID_MIN IGUAL expr WHERE VABRE localdecls VFECHA'''
    p[0] = sa.FuncDeclWhere(p[1], [], p[3], p[6])

def p_funcdecl4(p):
    '''funcdecl : ID_MIN simplepats IGUAL expr WHERE VABRE localdecls VFECHA'''
    p[0] = sa.FuncDeclWhere(p[1], p[2], p[4], p[7])

def p_funcdecl5(p):
    '''funcdecl : ID_MIN guards'''
    p[0] = sa.FuncDeclGuards(p[1], [], p[2])

def p_funcdecl6(p):
    '''funcdecl : ID_MIN simplepats guards'''
    p[0] = sa.FuncDeclGuards(p[1], p[2], p[3])

# PADRÕES SIMPLES (argumentos de função e lambda)
# Construtores com argumentos devem ser envolvidos em parênteses:
#   f (Circulo r) = ...   em vez de   f Circulo r = ...
def p_simplepats1(p):
    '''simplepats : simplepat'''
    p[0] = [p[1]]

def p_simplepats2(p):
    '''simplepats : simplepats simplepat'''
    p[0] = p[1] + [p[2]]

def p_simplepat_lower(p):
    '''simplepat : ID_MIN'''
    p[0] = sa.VarPat(p[1])

def p_simplepat_underscore(p):
    '''simplepat : SUBLINHADO'''
    p[0] = sa.WildcardPat()

def p_simplepat_int(p):
    '''simplepat : INT'''
    p[0] = sa.IntPat(p[1])

def p_simplepat_true(p):
    '''simplepat : TRUE'''
    p[0] = sa.BoolPat(True)

def p_simplepat_false(p):
    '''simplepat : FALSE'''
    p[0] = sa.BoolPat(False)

def p_simplepat_char(p):
    '''simplepat : CARACTERE'''
    p[0] = sa.CharPat(p[1])

def p_simplepat_upper(p):
    '''simplepat : ID_MAI'''
    p[0] = sa.ConPat(p[1])

def p_simplepat_paren(p):
    '''simplepat : LPAREN pattern RPAREN'''
    p[0] = p[2]

# GUARDAS
def p_guards1(p):
    '''guards : guard'''
    p[0] = sa.SingleGuards(p[1])

def p_guards2(p):
    '''guards : guards guard'''
    p[0] = sa.CompoundGuards(p[1], p[2])

def p_guard(p):
    '''guard : BARRA_VERT expr IGUAL expr'''
    p[0] = sa.Guard(p[2], p[4])

# DECLARAÇÕES LOCAIS (where / let)
def p_localdecls1(p):
    '''localdecls : localdecl'''
    p[0] = sa.SingleLocaldecl(p[1])

def p_localdecls2(p):
    '''localdecls : localdecls VSEP localdecl'''
    p[0] = sa.CompoundLocaldecl(p[1], p[3])

def p_localdecl_func(p):
    '''localdecl : funcdecl'''
    p[0] = p[1]

def p_localdecl_type(p):
    '''localdecl : typesig'''
    p[0] = p[1]

# PADRÕES COMPLETOS (case-of)
def p_pattern_lower(p):
    '''pattern : ID_MIN'''
    p[0] = sa.VarPat(p[1])

def p_pattern_underscore(p):
    '''pattern : SUBLINHADO'''
    p[0] = sa.WildcardPat()

def p_pattern_upper(p):
    '''pattern : ID_MAI'''
    p[0] = sa.ConPat(p[1])

def p_pattern_upper_args(p):
    '''pattern : ID_MAI simplepats'''
    p[0] = sa.ConstructorArgs(p[1], p[2])

def p_pattern_int(p):
    '''pattern : INT'''
    p[0] = sa.IntPat(p[1])

def p_pattern_true(p):
    '''pattern : TRUE'''
    p[0] = sa.BoolPat(True)

def p_pattern_false(p):
    '''pattern : FALSE'''
    p[0] = sa.BoolPat(False)

def p_pattern_char(p):
    '''pattern : CARACTERE'''
    p[0] = sa.CharPat(p[1])

def p_pattern_paren(p):
    '''pattern : LPAREN pattern RPAREN'''
    p[0] = p[2]

def p_pattern_tuple(p):
    '''pattern : LPAREN pattern VIRGULA patterntuple RPAREN'''
    p[0] = sa.TuplePat([p[2]] + p[4])

def p_pattern_emptylist(p):
    '''pattern : LCOLCH RCOLCH'''
    p[0] = sa.EmptyListPat()

def p_pattern_list(p):
    '''pattern : LCOLCH patternlist RCOLCH'''
    p[0] = sa.ListPat(p[2])

def p_pattern_cons(p):
    '''pattern : pattern CONS pattern'''
    p[0] = sa.ConsPat(p[1], p[3])

def p_patterntuple1(p):
    '''patterntuple : pattern'''
    p[0] = [p[1]]

def p_patterntuple2(p):
    '''patterntuple : patterntuple VIRGULA pattern'''
    p[0] = p[1] + [p[3]]

def p_patternlist1(p):
    '''patternlist : pattern'''
    p[0] = [p[1]]

def p_patternlist2(p):
    '''patternlist : patternlist VIRGULA pattern'''
    p[0] = p[1] + [p[3]]

# EXPRESSÕES (ambiguidade resolvida pela tabela de precedência)
def p_expr_soma(p):
    '''expr : expr SOMA expr'''
    p[0] = sa.InfixExp('+', p[1], p[3])

def p_expr_sub(p):
    '''expr : expr SUB expr'''
    p[0] = sa.InfixExp('-', p[1], p[3])

def p_expr_mul(p):
    '''expr : expr VEZES expr'''
    p[0] = sa.InfixExp('*', p[1], p[3])

def p_expr_div(p):
    '''expr : expr BARRA expr'''
    p[0] = sa.InfixExp('/', p[1], p[3])

def p_expr_pot(p):
    '''expr : expr POT expr'''
    p[0] = sa.InfixExp('^', p[1], p[3])

def p_expr_intdiv(p):
    '''expr : expr DIV expr'''
    p[0] = sa.InfixExp('div', p[1], p[3])

def p_expr_mod(p):
    '''expr : expr MOD expr'''
    p[0] = sa.InfixExp('mod', p[1], p[3])

def p_expr_concat(p):
    '''expr : expr CONCATENA expr'''
    p[0] = sa.InfixExp('++', p[1], p[3])

def p_expr_cons(p):
    '''expr : expr CONS expr'''
    p[0] = sa.InfixExp(':', p[1], p[3])

def p_expr_eq(p):
    '''expr : expr IGUALDADE expr'''
    p[0] = sa.InfixExp('==', p[1], p[3])

def p_expr_neq(p):
    '''expr : expr DIFERENTE expr'''
    p[0] = sa.InfixExp('/=', p[1], p[3])

def p_expr_lt(p):
    '''expr : expr MENOR expr'''
    p[0] = sa.InfixExp('<', p[1], p[3])

def p_expr_gt(p):
    '''expr : expr MAIOR expr'''
    p[0] = sa.InfixExp('>', p[1], p[3])

def p_expr_le(p):
    '''expr : expr MENOR_EQ expr'''
    p[0] = sa.InfixExp('<=', p[1], p[3])

def p_expr_ge(p):
    '''expr : expr MAIOR_EQ expr'''
    p[0] = sa.InfixExp('>=', p[1], p[3])

def p_expr_and(p):
    '''expr : expr E_LOG expr'''
    p[0] = sa.InfixExp('&&', p[1], p[3])

def p_expr_or(p):
    '''expr : expr OU_LOG expr'''
    p[0] = sa.InfixExp('||', p[1], p[3])

def p_expr_compose(p):
    '''expr : expr COMPOSICAO expr'''
    p[0] = sa.InfixExp('.', p[1], p[3])

def p_expr_dollar(p):
    '''expr : expr DOLAR expr'''
    p[0] = sa.InfixExp('$', p[1], p[3])

def p_expr_neg(p):
    '''expr : SUB expr %prec MENOS_UN'''
    p[0] = sa.NegExp(p[2])

def p_expr_not(p):
    '''expr : NOT expr %prec NAO_UN'''
    p[0] = sa.NotExp(p[2])

def p_expr_if(p):
    '''expr : ifexpr'''
    p[0] = p[1]

def p_expr_case(p):
    '''expr : caseexpr'''
    p[0] = p[1]

def p_expr_let(p):
    '''expr : letexpr'''
    p[0] = p[1]

def p_expr_do(p):
    '''expr : doexpr'''
    p[0] = p[1]

def p_expr_lambda(p):
    '''expr : lambdaexpr'''
    p[0] = p[1]

def p_expr_app(p):
    '''expr : appexpr'''
    p[0] = p[1]

# APLICAÇÃO DE FUNÇÃO (justaposição, maior precedência binária)
def p_appexpr_app(p):
    '''appexpr : appexpr atom %prec APLIC'''
    p[0] = sa.AppExp(p[1], p[2])

def p_appexpr_atom(p):
    '''appexpr : atom'''
    p[0] = p[1]

# ÁTOMOS
def p_atom_lower(p):
    '''atom : ID_MIN'''
    p[0] = sa.VarExp(p[1])

def p_atom_upper(p):
    '''atom : ID_MAI'''
    p[0] = sa.ConExp(p[1])

def p_atom_int(p):
    '''atom : INT'''
    p[0] = sa.IntExp(p[1])

def p_atom_true(p):
    '''atom : TRUE'''
    p[0] = sa.BoolExp(True)

def p_atom_false(p):
    '''atom : FALSE'''
    p[0] = sa.BoolExp(False)

def p_atom_char(p):
    '''atom : CARACTERE'''
    p[0] = sa.CharExp(p[1])

def p_atom_string(p):
    '''atom : STRING'''
    p[0] = sa.StringExp(p[1])


def p_atom_paren(p):
    '''atom : LPAREN expr RPAREN'''
    p[0] = p[2]

def p_atom_tuple(p):
    '''atom : LPAREN expr VIRGULA exprtuple RPAREN'''
    p[0] = sa.TupleExp([p[2]] + p[4])

def p_atom_emptylist(p):
    '''atom : LCOLCH RCOLCH'''
    p[0] = sa.EmptyListExp()

def p_atom_list(p):
    '''atom : LCOLCH exprlist RCOLCH'''
    p[0] = sa.ListExp(p[2])

def p_atom_range_open(p):
    '''atom : LCOLCH expr PONTOPONTO RCOLCH'''
    p[0] = sa.RangeExp(p[2], None)

def p_atom_range(p):
    '''atom : LCOLCH expr PONTOPONTO expr RCOLCH'''
    p[0] = sa.RangeExp(p[2], p[4])

# IF-THEN-ELSE
def p_ifexpr(p):
    '''ifexpr : IF expr THEN expr ELSE expr %prec LAMBDA_PREC'''
    p[0] = sa.IfExp(p[2], p[4], p[6])

# CASE-OF
def p_caseexpr(p):
    '''caseexpr : CASE expr OF VABRE casealts VFECHA'''
    p[0] = sa.CaseExp(p[2], p[5])

def p_casealts1(p):
    '''casealts : casealt'''
    p[0] = sa.SingleCaseAlts(p[1])

def p_casealts2(p):
    '''casealts : casealts VSEP casealt'''
    p[0] = sa.CompoundCaseAlts(p[1], p[3])

def p_casealt(p):
    '''casealt : pattern SETA expr'''
    p[0] = sa.CaseAlt(p[1], p[3])

# LET-IN
def p_letexpr(p):
    '''letexpr : LET VABRE localdecls VFECHA IN expr %prec LAMBDA_PREC'''
    p[0] = sa.LetExp(p[3], p[6])

# DO
def p_doexpr(p):
    '''doexpr : DO VABRE dostmts VFECHA'''
    p[0] = sa.DoExp(p[3])

def p_dostmts1(p):
    '''dostmts : dostmt'''
    p[0] = sa.SingleDoStmts(p[1])

def p_dostmts2(p):
    '''dostmts : dostmts VSEP dostmt'''
    p[0] = sa.CompoundDoStmts(p[1], p[3])

def p_dostmt_bind(p):
    '''dostmt : ID_MIN EXTRAI expr'''
    p[0] = sa.BindStmt(p[1], p[3])

def p_dostmt_let(p):
    '''dostmt : LET VABRE localdecls VFECHA'''
    p[0] = sa.LetDoStmt(p[3])

def p_dostmt_return(p):
    '''dostmt : RETURN atom'''
    p[0] = sa.ExprDoStmt(sa.AppExp(sa.VarExp('return'), p[2]))

def p_dostmt_expr(p):
    '''dostmt : expr'''
    p[0] = sa.ExprDoStmt(p[1])

# LAMBDA
def p_lambdaexpr(p):
    '''lambdaexpr : LAMBDA simplepats SETA expr %prec LAMBDA_PREC'''
    p[0] = sa.LambdaExp(p[2], p[4])

# LISTAS AUXILIARES
def p_exprtuple1(p):
    '''exprtuple : expr'''
    p[0] = [p[1]]

def p_exprtuple2(p):
    '''exprtuple : exprtuple VIRGULA expr'''
    p[0] = p[1] + [p[3]]

def p_exprlist1(p):
    '''exprlist : expr'''
    p[0] = [p[1]]

def p_exprlist2(p):
    '''exprlist : exprlist VIRGULA expr'''
    p[0] = p[1] + [p[3]]

# ERRO SINTÁTICO
def p_error(p):
    if p:
        descricoes = {
            'VABRE'  : 'inicio de bloco indentado',
            'VFECHA' : 'fim de bloco indentado',
            'VSEP'   : 'nova linha no mesmo nivel de indentacao',
        }
        descricao = descricoes.get(p.type, "'%s'" % p.value)
        print("Erro sintatico na linha %d: %s inesperado" % (p.lineno, descricao))
    else:
        print("Erro sintatico: fim de arquivo inesperado — verifique se todos os blocos estao corretamente indentados")

# MAIN
def main():
    f = open("input1.hs", "r")
    data = f.read()
    f.close()
    lexer  = HaskellLexer()
    parser = yacc.yacc()
    result = parser.parse('\n' + data, lexer=lexer)
    print("Parse concluído:", result)

if __name__ == "__main__":
    main()