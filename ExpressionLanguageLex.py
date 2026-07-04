import ply.lex as lex
from collections import deque

# PALAVRAS RESERVADAS
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

# LISTA DE TOKENS
tokens = [
   # Identificadores
   'ID_MIN', 'ID_MAI',
   # Literais
   'INT', 'CARACTERE', 'STRING',
   # Operadores aritméticos
   'SOMA', 'SUB', 'VEZES', 'BARRA', 'POT',
   # Operadores de lista
   'CONCATENA', 'CONS',
   # Operadores relacionais
   'IGUALDADE', 'DIFERENTE', 'MENOR', 'MAIOR', 'MENOR_EQ', 'MAIOR_EQ',
   # Operadores lógicos
   'E_LOG', 'OU_LOG',
   # Operadores funcionais
   'COMPOSICAO', 'DOLAR', 'LAMBDA',
   # Símbolos de tipo e definição
   'ANOTACAO', 'IGUAL', 'SETA', 'EXTRAI',
   # Delimitadores
   'LPAREN', 'RPAREN', 'LCOLCH', 'RCOLCH', 'LCHAV', 'RCHAV',
   'VIRGULA', 'PV', 'BARRA_VERT', 'PONTOPONTO', 'ARROBA', 'SUBLINHADO',
   # Token interno: quebra de linha com nível de indentação
   'NOVA_LINHA',
   # Tokens virtuais emitidos pela FSM + Pilha (consumidos pelo parser)
   'VABRE', 'VFECHA', 'VSEP',
] + list(reservadas.values())

# OPERADORES E DELIMITADORES (regras de string)
t_CONCATENA  = r'\+\+'
t_SOMA    = r'\+'
t_SETA   = r'->'
t_SUB     = r'-'
t_VEZES   = r'\*'
t_POT     = r'\^'
t_ANOTACAO  = r'::'
t_CONS    = r':'
t_PONTOPONTO  = r'\.\.'
t_COMPOSICAO = r'\.'
t_DOLAR  = r'\$'
t_LAMBDA  = r'\\'
t_IGUALDADE      = r'=='
t_DIFERENTE     = r'/='
t_BARRA   = r'/'
t_MENOR_EQ      = r'<='
t_EXTRAI    = r'<-'
t_MENOR      = r'<'
t_MAIOR_EQ      = r'>='
t_MAIOR      = r'>'
t_E_LOG     = r'&&'
t_OU_LOG      = r'\|\|'
t_IGUAL   = r'='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LCOLCH  = r'\['
t_RCOLCH  = r'\]'
t_LCHAV   = r'\{'
t_RCHAV   = r'\}'
t_VIRGULA = r','
t_PV      = r';'
t_BARRA_VERT    = r'\|'
t_ARROBA      = r'@'

# IDENTIFICADORES
#   minúsculo / _ - variáveis e funções  (ID_MIN)
#   maiúsculo - tipos e construtores (ID_MAI)
def t_ID_MIN(t):
   r"[a-z_][a-zA-Z_0-9']*"
   if t.value == '_':
      t.type = 'SUBLINHADO'
   else:
      t.type = reservadas.get(t.value, 'ID_MIN')
   return t

def t_ID_MAI(t):
   r"[A-Z][a-zA-Z_0-9']*"
   t.type = reservadas.get(t.value, 'ID_MAI')
   return t

# LITERAIS
def t_INT(t):
   r'\d+'
   t.value = int(t.value)
   return t

def t_CARACTERE(t):
   r"'(\\.|[^\\'])'"
   t.value = t.value[1:-1]   # remove as aspas simples
   return t

def t_STRING(t):
   r'"(\\.|[^\\"])*"'
   t.value = t.value[1:-1]   # remove as aspas duplas
   return t

# COMENTÁRIOS
def t_COMENTARIO_LINHA(t):
   r'--[^\n]*'
   pass

def t_COMENTARIO_BLOCO(t):
   r'\{-(.|\n)*?-\}'
   t.lexer.lineno += t.value.count('\n')
   pass

# QUEBRA DE LINHA (token interno para controle de indentação)
# O valor do token é o número de espaços após o \n,
# representando o nível de indentação da próxima linha.
# Este token NÃO é repassado ao parser — a FSM o consome
# e emite VABRE / VSEP / VFECHA conforme necessário.
def t_NOVA_LINHA(t):
   r'\n[ \t]*'
   t.lexer.lineno += 1
   t.lexer.line_start = t.lexpos + 1  # posição absoluta do início da linha
   t.value = len(t.value) - 1         # nível de indentação (nº de espaços)
   return t

t_ignore = ' \t'

# ERRO LÉXICO
def t_error(t):
   print("Erro léxico: caractere inválido '%s' na linha %d" % (t.value[0], t.lexer.lineno))
   t.lexer.skip(1)

# FSM + PILHA DE INDENTAÇÃO
#
# O HaskellLexer encapsula o léxico PLY e implementa a regra
# do offside de Haskell usando uma Máquina de Estados Finita
# (FSM) e uma Pilha de níveis de indentação.
#
# Estados da FSM:
#   NORMAL          → processamento regular
#   BLOCO_PENDENTE  → viu WHERE/LET/DO/OF; aguarda próximo
#                     NOVA_LINHA para abrir o bloco no nível certo
#
# Pilha:
#   Armazena inteiros representando colunas de indentação.
#   Topo da pilha = indentação do bloco atual.
#   Começa com [0] (nível raiz do programa).
#
# Tokens virtuais produzidos:
#   VABRE  → abre bloco  (equivale a '{' implícito)
#   VSEP  → separa itens (equivale a ';' implícito)
#   VFECHA → fecha bloco (equivale a '}' implícito)

ESTADO_NORMAL         = 'NORMAL'
ESTADO_BLOCO_PENDENTE = 'BLOCO_PENDENTE'

# Palavras-chave que abrem um novo bloco de indentação
BLOCK_OPENERS = {'WHERE', 'LET', 'DO', 'OF'}


class HaskellLexer:

   def __init__(self):
      self._lexer     = lex.lex()
      self._lexer.line_start = 0  # posição absoluta do início da primeira linha
      self._buffer    = deque()          # fila de tokens virtuais a emitir
      self._pilha     = [0]              # pilha de indentação
      self._estado    = ESTADO_NORMAL    # estado inicial da FSM
      self._last_type = None             # tipo do último token retornado (evita VSEP duplicado)

   def input(self, data):
      self._lexer.input(data)

   # Criação de um token virtual
   def _token_virtual(self, tipo, valor, lineno):
      tok        = lex.LexToken()
      tok.type   = tipo
      tok.value  = valor
      tok.lineno = lineno
      tok.lexpos = -1
      return tok

   # Lógica da FSM + Pilha: chamada a cada NOVA_LINHA recebido
   def _processar_newline(self, col, lineno):
      if self._estado == ESTADO_BLOCO_PENDENTE:
         # Transição BLOCO_PENDENTE → NORMAL:
         # empilha o novo nível e abre o bloco
         self._estado = ESTADO_NORMAL
         self._pilha.append(col)
         self._buffer.append(self._token_virtual('VABRE', '{', lineno))

      elif col == self._pilha[-1]:
         # Mesmo nível de indentação → separa dois itens do bloco
         # Ignora VSEP duplicado (linhas em branco geram múltiplos NEWLINEs)
         if self._last_type != 'VSEP':
            self._buffer.append(self._token_virtual('VSEP', ';', lineno))

      elif col < self._pilha[-1]:
         # Menos indentado → fecha bloco(s) até atingir o nível correspondente
         while len(self._pilha) > 1 and col < self._pilha[-1]:
            self._pilha.pop()
            self._buffer.append(self._token_virtual('VFECHA', '}', lineno))
         self._buffer.append(self._token_virtual('VSEP', ';', lineno))

      # col > self._pilha[-1]: continuação de linha → nenhum token emitido

   def _fechar_todos_os_blocos(self, lineno):
      """Fecha todos os blocos abertos ao atingir o fim do arquivo."""
      while len(self._pilha) > 1:
         self._pilha.pop()
         self._buffer.append(self._token_virtual('VFECHA', '}', lineno))

   # Interface pública usada pelo parser PLY:
   #   parser = yacc.yacc()
   #   lexer  = HaskellLexer()
   #   parser.parse(input, lexer=lexer)
   def token(self):
      while True:
         # 1. Drena o buffer de tokens virtuais primeiro
         if self._buffer:
            tok = self._buffer.popleft()
            self._last_type = tok.type
            return tok

         # 2. Pede o próximo token ao léxico PLY
         tok = self._lexer.token()

         # 3. Fim de arquivo: fecha todos os blocos pendentes
         if tok is None:
            self._fechar_todos_os_blocos(self._lexer.lineno)
            if self._buffer:
               tok = self._buffer.popleft()
               self._last_type = tok.type
               return tok
            return None

         # 4. NOVA_LINHA: processa indentação via FSM + pilha
         #    e NÃO repassa o token ao parser
         if tok.type == 'NOVA_LINHA':
            self._processar_newline(tok.value, tok.lineno)
            continue   # volta ao topo do loop para verificar o buffer

         # 5. Bloco inline: keyword e primeiro token na mesma linha (sem NOVA_LINHA entre eles)
         #    Ex: "let x = 42", "where f = 1" — abre VABRE usando a coluna do token atual
         if self._estado == ESTADO_BLOCO_PENDENTE:
            col = tok.lexpos - self._lexer.line_start
            self._estado = ESTADO_NORMAL
            self._pilha.append(col)
            self._buffer.append(self._token_virtual('VABRE', '{', tok.lineno))
            self._buffer.append(tok)
            continue   # drena o buffer: VABRE primeiro, depois o token real

         # 6. Transição de estado: palavra-chave que abre bloco
         if tok.type in BLOCK_OPENERS:
            self._estado = ESTADO_BLOCO_PENDENTE

         self._last_type = tok.type
         return tok


def main():
   f     = open("input1.hs", "r")
   lexer = HaskellLexer()
   lexer.input(f.read())
   print('\n\n# lexer output:')
   tok = lexer.token()
   while tok is not None:
      print('type:', tok.type, ', value:', tok.value)
      tok = lexer.token()

if __name__ == "__main__":
   main()