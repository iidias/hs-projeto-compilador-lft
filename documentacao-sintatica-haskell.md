# λ Documentação Sintática — Linguagem Haskell

## 1. Introdução

Este documento descreve a gramática do subconjunto da linguagem **Haskell** definido para fins didáticos na disciplina de Linguagens Formais e Tradutores.

A análise sintática (*parsing*) é a segunda etapa do processo de compilação. Ela recebe a sequência de tokens produzida pelo analisador léxico e verifica se eles formam uma estrutura gramaticalmente válida de acordo com as regras de produção da linguagem.

As regras abaixo utilizam a notação **BNF estendida** (EBNF):

- `→` separa o símbolo não-terminal de suas produções
- `|` indica alternativas de produção
- Símbolos em `"aspas"` representam terminais literais
- Símbolos em `MAIÚSCULAS` representam tokens léxicos (e.g., `ID`, `INT`, `FLOAT`)
- Símbolos em `minúsculas` representam não-terminais
- `[ x ]` indica que `x` é opcional (zero ou uma ocorrência)
- `{ x }` indica que `x` pode se repetir (zero ou mais ocorrências)

---

## 2. Estrutura Geral do Programa

Um programa válido neste subconjunto de Haskell é composto por uma sequência de declarações de alto nível. A função `main`, de tipo `IO ()`, é obrigatória como ponto de entrada.

```
program
    → { top_level_decl }

top_level_decl
    → type_signature
    | func_def
    | data_decl
    | type_alias
```

### Exemplo

```haskell
-- Assinatura de tipo
dobrar :: Int -> Int

-- Definição de função
dobrar x = x * 2

-- Ponto de entrada obrigatório
main :: IO ()
main = do
    let resultado = dobrar 5
    return ()
```

---

## 3. Assinaturas de Tipo

Assinaturas de tipo anotam explicitamente o tipo de uma função ou variável. São opcionais, mas fortemente recomendadas.

```
type_signature
    → ID "::" type_expr

type_expr
    → type_atom
    | type_atom "->" type_expr
    | "[" type_expr "]"
    | "(" type_expr { "," type_expr } ")"

type_atom
    → "Int"
    | "Float"
    | "Bool"
    | "Char"
    | "String"
    | "IO" type_atom
    | "(" ")"
    | UPPER_ID
```

### Exemplos

```haskell
soma        :: Int -> Int -> Int
ehPar       :: Int -> Bool
cabeca      :: [Int] -> Int
pares       :: [(Int, Bool)]
identidade  :: a -> a
main        :: IO ()
```

---

## 4. Declarações de Tipo Algébrico

```
data_decl
    → "data" UPPER_ID { LOWER_ID } "=" constructor_list

constructor_list
    → constructor { "|" constructor }

constructor
    → UPPER_ID { type_atom }

type_alias
    → "type" UPPER_ID "=" type_expr
```

### Exemplos

```haskell
data Cor    = Vermelho | Verde | Azul

data Forma  = Circulo Float
            | Retangulo Float Float

data Arvore = Folha
            | Nodo Int Arvore Arvore

type Nome   = String
type Ponto  = (Float, Float)
```

---

## 5. Definições de Função

Funções são definidas por uma ou mais equações. O compilador seleciona a equação correta por casamento de padrões, da primeira para a última.

```
func_def
    → ID { pattern } [ guards ] "=" expr [ where_clause ]
    | ID { pattern } [ guards ] "=" expr [ where_clause ]

guards
    → { "|" expr "=" expr }
```

### 5.1 Definição simples (sem padrões)

```haskell
pi :: Float
pi = 3.14159
```

### 5.2 Definição com parâmetros

```haskell
soma :: Int -> Int -> Int
soma x y = x + y
```

### 5.3 Definição com múltiplas equações (casamento de padrões)

```haskell
fatorial :: Int -> Int
fatorial 0 = 1
fatorial n = n * fatorial (n - 1)
```

### 5.4 Definição com guardas

```haskell
classificar :: Int -> String
classificar n
    | n < 0    = "negativo"
    | n == 0   = "zero"
    | otherwise = "positivo"
```

### 5.5 Cláusula `where`

```haskell
hipotenusa :: Float -> Float -> Float
hipotenusa a b = raiz
    where
        raiz     = sqrt quadSoma
        quadSoma = a^2 + b^2
```

---

## 6. Padrões (*Patterns*)

Padrões são usados em equações de funções, expressões `case` e `let`. O casamento é verificado de cima para baixo, da esquerda para a direita.

```
pattern
    → "_"
    | LOWER_ID
    | UPPER_ID { pattern }
    | INT
    | FLOAT
    | CHAR
    | "True"
    | "False"
    | "(" pattern { "," pattern } ")"
    | "[" [ pattern { "," pattern } ] "]"
    | pattern ":" pattern
    | LOWER_ID "@" pattern
    | "(" pattern ")"
```

### Exemplos de padrões

```haskell
-- Padrão coringa
f _ = 0

-- Padrão literal
ehZero 0 = True
ehZero _ = False

-- Padrão de construtor
area (Circulo r)       = pi * r^2
area (Retangulo l a)   = l * a

-- Padrão de lista (cons)
cabeca (x:_)  = x
cauda  (_:xs) = xs

-- Padrão as (@)
duplicarLista xs@(x:_) = xs ++ xs

-- Padrão de tupla
fst' (a, _) = a
snd' (_, b) = b
```

---

## 7. Expressões

Expressões são a unidade fundamental de computação em Haskell. Toda expressão possui um tipo e avalia para um valor.

```
expr
    → lambda_expr
    | let_expr
    | if_expr
    | case_expr
    | do_expr
    | infix_expr

infix_expr
    → infix_expr infix_op infix_expr
    | unary_expr

unary_expr
    → "-" app_expr
    | "not" app_expr
    | app_expr

app_expr
    → app_expr atom_expr
    | atom_expr

atom_expr
    → LOWER_ID
    | UPPER_ID
    | INT
    | FLOAT
    | CHAR
    | STRING
    | "True"
    | "False"
    | "(" expr ")"
    | "(" expr { "," expr } ")"
    | "[" list_body "]"
    | "[" expr ".." [ expr ] "]"
    | "[" expr "|" { qual { "," qual } } "]"

infix_op
    → "+" | "-" | "*" | "/" | "^"
    | "div" | "mod"
    | "++" | ":"
    | "==" | "/=" | "<" | ">" | "<=" | ">="
    | "&&" | "||"
    | "." | "$"
```

### 7.1 Precedência de expressões (resumo)

| Nível | Operadores                             | Associatividade       |
|:-----:|:---------------------------------------|:---------------------:|
| 10    | Aplicação de função (justaposição)      | Esquerda para direita |
| 9     | `.`                                    | Direita para esquerda |
| 8     | `^`                                    | Direita para esquerda |
| 7     | `*`, `/`, `div`, `mod`                 | Esquerda para direita |
| 6     | `+`, `-`                               | Esquerda para direita |
| 5     | `:`, `++`                              | Direita para esquerda |
| 4     | `==`, `/=`, `<`, `>`, `<=`, `>=`       | Sem associatividade   |
| 3     | `&&`                                   | Direita para esquerda |
| 2     | `\|\|`                                 | Direita para esquerda |
| 0     | `$`                                    | Direita para esquerda |

---

## 8. Expressão Lambda

Expressões lambda definem funções anônimas.

```
lambda_expr
    → "\" { pattern }+ "->" expr
```

### Exemplos

```haskell
-- Lambda com um argumento
\x -> x + 1

-- Lambda com dois argumentos
\x y -> x * y

-- Lambda com padrão de tupla
\(a, b) -> a + b

-- Uso em contexto
map (\x -> x^2) [1..5]
```

---

## 9. Expressão `let-in`

A expressão `let-in` introduz definições locais dentro de uma expressão. Diferentemente da cláusula `where`, o `let-in` é uma **expressão** e pode aparecer em qualquer posição onde uma expressão é esperada.

```
let_expr
    → "let" { local_def }+ "in" expr

local_def
    → func_def
    | type_signature
```

### Exemplos

```haskell
-- let-in simples
resultado = let x = 10
                y = 20
            in x + y

-- let-in aninhado
calc = let a = 2
           b = let c = 3
               in c + 1
       in a * b
```

---

## 10. Expressão `if-then-else`

Em Haskell, `if-then-else` é uma **expressão** (não um comando), portanto o ramo `else` é **obrigatório** e ambos os ramos devem ter o mesmo tipo.

```
if_expr
    → "if" expr "then" expr "else" expr
```

### Exemplos

```haskell
-- if-then-else simples
absoluto x = if x < 0 then -x else x

-- if-then-else aninhado
sinal x = if x > 0
          then "positivo"
          else if x < 0
               then "negativo"
               else "zero"
```

---

## 11. Expressão `case-of`

A expressão `case-of` realiza casamento de padrões explícito sobre um valor. É a forma mais geral de desestruturação em Haskell.

```
case_expr
    → "case" expr "of" "{" { case_alt }+ "}"

case_alt
    → pattern [ case_guards ] "->" expr [ where_clause ]

case_guards
    → { "|" expr "->" expr }
```

> **Nota de layout:** As alternativas do `case` são delimitadas por indentação (regra do *offside*). O `{` e `}` acima representam a indentação inferida pelo léxico.

### Exemplos

```haskell
-- case-of sobre Int
descrever n = case n of
    0 -> "zero"
    1 -> "um"
    _ -> "outro"

-- case-of sobre lista
tamanho lista = case lista of
    []     -> 0
    (_:xs) -> 1 + tamanho xs

-- case-of sobre tipo algébrico
exibir forma = case forma of
    Circulo r       -> "Círculo de raio " ++ show r
    Retangulo l a   -> "Retângulo " ++ show l ++ "x" ++ show a
```

---

## 12. Notação `do`

A notação `do` é uma sintaxe especial para sequenciar operações monádicas, usada principalmente para entrada/saída (`IO`).

```
do_expr
    → "do" "{" { do_stmt }+ "}"

do_stmt
    → LOWER_ID "<-" expr
    | "let" { local_def }+
    | expr
```

> **Nota:** Assim como o `case-of`, o bloco `do` usa indentação para delimitar comandos. O símbolo `<-` extrai o valor de dentro de um contexto monádico (e.g., lê da entrada padrão).

### Exemplo

```haskell
main :: IO ()
main = do
    let x = soma 3 4
    let resultado = fatorial x
    return ()
```

---

## 13. Listas

### 13.1 Lista literal

```
list_body
    → [ expr { "," expr } ]
```

```haskell
[]              -- lista vazia
[1, 2, 3]       -- lista de inteiros
['a', 'b', 'c'] -- lista de caracteres (String)
```

### 13.2 Intervalo (Range)

```
range_expr
    → "[" expr ".." [ expr ] "]"
    | "[" expr "," expr ".." [ expr ] "]"
```

```haskell
[1..5]       -- [1, 2, 3, 4, 5]
[1, 3..10]   -- [1, 3, 5, 7, 9]
[5, 4..1]    -- [5, 4, 3, 2, 1]
[1..]        -- lista infinita (avaliação preguiçosa)
```

### 13.3 Compreensão de Lista

```
list_comp
    → "[" expr "|" qual { "," qual } "]"

qual
    → LOWER_ID "<-" expr
    | expr
```

```haskell
quadrados   = [x^2 | x <- [1..10]]
pares       = [x   | x <- [1..20], even x]
produto     = [(x, y) | x <- [1..3], y <- [1..3], x /= y]
```

---

## 14. Tuplas

```
tuple_expr
    → "(" expr "," expr { "," expr } ")"
```

```haskell
ponto    = (3.0, 4.0)          -- (Float, Float)
pessoa   = ("Ana", 25, True)   -- (String, Int, Bool)
```

---

## 15. Cláusula `where`

A cláusula `where` introduz definições locais ao final de uma equação de função. As definições são visíveis em toda a equação, incluindo as guardas.

```
where_clause
    → "where" "{" { local_def }+ "}"

local_def
    → func_def
    | type_signature
```

### Exemplo

```haskell
bmi :: Float -> Float -> String
bmi peso altura
    | indice < 18.5 = "Abaixo do peso"
    | indice < 25.0 = "Normal"
    | indice < 30.0 = "Sobrepeso"
    | otherwise     = "Obesidade"
    where
        indice = peso / altura^2
```

---

## 16. Exemplo de Programa Completo

O programa abaixo demonstra a maioria das construções sintáticas deste subconjunto:

```haskell
-- Declaração de tipo algébrico
data Forma = Circulo Float
           | Retangulo Float Float

-- Sinônimo de tipo
type Area = Float

-- Funções com guardas e where
bmi :: Float -> Float -> String
bmi peso altura
    | indice <= 18.5 = "Abaixo do peso"
    | indice <= 25.0 = "Peso normal"
    | otherwise      = "Acima do peso"
    where indice = peso / altura ^ 2

-- Função com casamento de padrões e case-of
calcArea :: Forma -> Area
calcArea forma = case forma of
    Circulo r      -> pi * r ^ 2
    Retangulo l a  -> l * a

-- Função recursiva com múltiplas equações
fatorial :: Int -> Int
fatorial 0 = 1
fatorial n = n * fatorial (n - 1)

-- Função com lambda e compreensão de lista
quadradosDosImpares :: [Int] -> [Int]
quadradosDosImpares xs = map (\x -> x ^ 2) impares
    where impares = [x | x <- xs, odd x]

-- Definição local com let-in
raizesDaEquacao :: Float -> Float -> Float -> (Float, Float)
raizesDaEquacao a b c =
    let delta = b^2 - 4*a*c
        r1    = (-b + sqrt delta) / (2*a)
        r2    = (-b - sqrt delta) / (2*a)
    in (r1, r2)

-- Ponto de entrada
main :: IO ()
main = do
    let c1     = Circulo 5.0
    let r1     = Retangulo 3.0 4.0
    let area1  = calcArea c1
    let area2  = calcArea r1
    let fat7   = fatorial 7
    let impqs  = quadradosDosImpares [1..10]
    return ()
```

---

## 17. Gramática Consolidada (Referência Rápida)

```
program          → { top_level_decl }

top_level_decl   → type_signature | func_def | data_decl | type_alias

type_signature   → ID "::" type_expr
type_expr        → type_atom | type_atom "->" type_expr
                 | "[" type_expr "]" | "(" type_expr { "," type_expr } ")"
type_atom        → "Int" | "Float" | "Bool" | "Char" | "String"
                 | "IO" type_atom | "(" ")" | UPPER_ID | LOWER_ID

data_decl        → "data" UPPER_ID { LOWER_ID } "=" constructor_list
constructor_list → constructor { "|" constructor }
constructor      → UPPER_ID { type_atom }
type_alias       → "type" UPPER_ID "=" type_expr

func_def         → ID { pattern } [ guards ] "=" expr [ where_clause ]
guards           → { "|" expr "=" expr }
where_clause     → "where" { local_def }

pattern          → "_" | LOWER_ID | UPPER_ID { pattern } | INT | FLOAT
                 | CHAR | "True" | "False"
                 | "(" pattern { "," pattern } ")"
                 | "[" [ pattern { "," pattern } ] "]"
                 | pattern ":" pattern
                 | LOWER_ID "@" pattern

expr             → lambda_expr | let_expr | if_expr | case_expr | do_expr
                 | infix_expr
lambda_expr      → "\" { pattern }+ "->" expr
let_expr         → "let" { local_def }+ "in" expr
if_expr          → "if" expr "then" expr "else" expr
case_expr        → "case" expr "of" { case_alt }
case_alt         → pattern "->" expr [ where_clause ]
do_expr          → "do" { do_stmt }
do_stmt          → LOWER_ID "<-" expr | "let" { local_def } | expr

infix_expr       → infix_expr infix_op infix_expr | unary_expr
unary_expr       → "-" app_expr | "not" app_expr | app_expr
app_expr         → app_expr atom_expr | atom_expr
atom_expr        → LOWER_ID | UPPER_ID | INT | FLOAT | CHAR | STRING
                 | "True" | "False"
                 | "(" expr ")" | "(" expr { "," expr } ")"
                 | "[" list_body "]"
                 | "[" expr ".." [ expr ] "]"
                 | "[" expr "|" qual { "," qual } "]"

list_body        → [ expr { "," expr } ]
qual             → LOWER_ID "<-" expr | expr

infix_op         → "+" | "-" | "*" | "/" | "^" | "div" | "mod"
                 | "++" | ":" | "==" | "/=" | "<" | ">" | "<=" | ">="
                 | "&&" | "||" | "." | "$"
```
