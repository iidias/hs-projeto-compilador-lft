import ply.lex as lex

reservadas = {
   'if'     : 'IF',
   'then'   : 'THEN',
   'else'   : 'ELSE',
   'case'   : 'CASE',
   'of'     : 'OF',
   'where'  : 'WHERE',
   'let'    : 'LET',
   'in'     : 'IN',
   'do'     : 'DO',
   'return' : 'RETURN',
   'data'   : 'DATA',
   'type'   : 'TYPE',
   'not'    : 'NOT',
   'div'    : 'DIV',
   'mod'    : 'MOD',
   'True'   : 'TRUE',
   'False'  : 'FALSE',
}

tokens = [
   # Identificadores
   'LOWER_ID', 'UPPER_ID',
   # Literais
   'INT', 'CHAR', 'STRING',
   # Operadores aritméticos
   'SOMA', 'SUB', 'VEZES', 'BARRA', 'POT',
   # Operadores de lista
   'CONCAT', 'CONS',
   # Operadores relacionais
   'EQ', 'NEQ', 'LT', 'GT', 'LE', 'GE',
   # Operadores lógicos
   'AND', 'OR',
   # Operadores funcionais
   'COMPOSE', 'DOLLAR', 'LAMBDA',
   # Símbolos de tipo e definição
   'DCOLON', 'IGUAL', 'ARROW', 'BIND',
   # Delimitadores
   'LPAREN', 'RPAREN', 'LCOLCH', 'RCOLCH', 'LCHAV', 'RCHAV',
   'VIRGULA', 'PV', 'PIPE', 'DOTDOT', 'AT', 'UNDERSCORE',
] + list(reservadas.values())

# Operadores e delimitadores
# Operadores de dois caracteres devem vir antes dos de um caractere.
# O PLY ordena as regras de string por tamanho (maior primeiro),
# garantindo que '==' seja reconhecido antes de '=', '::' antes de ':', etc.

t_CONCAT  = r'\+\+'
t_SOMA    = r'\+'
t_ARROW   = r'->'
t_SUB     = r'-'
t_VEZES   = r'\*'
t_POT     = r'\^'
t_DCOLON  = r'::'
t_CONS    = r':'
t_DOTDOT  = r'\.\.'
t_COMPOSE = r'\.'
t_DOLLAR  = r'\$'
t_LAMBDA  = r'\\'
t_EQ      = r'=='
t_NEQ     = r'/='
t_BARRA   = r'/'
t_LE      = r'<='
t_BIND    = r'<-'
t_LT      = r'<'
t_GE      = r'>='
t_GT      = r'>'
t_AND     = r'&&'
t_OR      = r'\|\|'
t_IGUAL   = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCOLCH  = r'\['
t_RCOLCH  = r'\]'
t_LCHAV   = r'\{'
t_RCHAV   = r'\}'
t_VIRGULA = r','
t_PV      = r';'
t_PIPE    = r'\|'
t_AT      = r'@'

# Identificadores
# Haskell distingue identificadores pelo primeiro caractere:
# minúsculo/_ -  variáveis e funções (LOWER_ID)
# maiúsculo - tipos e construtores (UPPER_ID)

def t_LOWER_ID(t):
   r"[a-z_][a-zA-Z_0-9']*"
   if t.value == '_':
      t.type = 'UNDERSCORE'
   else:
      t.type = reservadas.get(t.value, 'LOWER_ID')
   return t

def t_UPPER_ID(t):
   r"[A-Z][a-zA-Z_0-9']*"
   t.type = reservadas.get(t.value, 'UPPER_ID')
   return t

# Literais

def t_INT(t):
   r'\d+'
   t.value = int(t.value)
   return t

def t_CHAR(t):
   r"'(\\.|[^\\'])'"
   t.value = t.value[1:-1]  # remove as aspas simples
   return t

def t_STRING(t):
   r'"(\\.|[^\\"])*"'
   t.value = t.value[1:-1]  # remove as aspas duplas
   return t

# Comentários
# pass - ignora

def t_COMENTARIO_LINHA(t):
   r'--[^\n]*'
   pass

def t_COMENTARIO_BLOCO(t):
   r'\{-(.|\n)*?-\}'
   t.lexer.lineno += t.value.count('\n')
   pass 

# Controle de linha

def t_newline(t):
   r'\n+'
   t.lexer.lineno += len(t.value)

t_ignore = ' \t'

# Erro léxico

def t_error(t):
   print("Erro léxico: caractere inválido '%s' na linha %d" % (t.value[0], t.lexer.lineno))
   t.lexer.skip(1)


def main():
   f = open("input1.hs", "r")
   lexer = lex.lex()
   lexer.input(f.read())
   print('\n\n# lexer output:')
   for tok in lexer:
      print('type:', tok.type, ', value:', tok.value)


if __name__ == "__main__":
   main()
