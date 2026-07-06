# λ Documentação Sintática — Linguagem Haskell

## 1. Introdução

Este documento descreve a sintaxe do subconjunto de **Haskell** definido para a disciplina de Linguagens Formais e Tradutores.

A análise sintática recebe os tokens produzidos pelo analisador léxico e verifica se eles formam uma estrutura gramaticalmente válida. O parser é implementado em PLY (Python Lex-Yacc).

**Nota sobre blocos:** Haskell utiliza indentação para delimitar blocos. O analisador léxico (via FSM + Pilha) converte automaticamente a indentação em três tokens virtuais — `VOPEN`, `VSEMI` e `VCLOSE` — que o parser consome como se fossem `{`, `;` e `}` explícitos.

---

## 2. Estrutura Geral do Programa

Um programa é uma sequência de declarações de alto nível. A função `main` é o ponto de entrada obrigatório.

```
program → topdecl
        | program VSEMI topdecl

topdecl → typesig | funcdecl | datadecl
```

---

## 3. Assinaturas de Tipo

Anotam o tipo de uma função ou variável. São opcionais mas recomendadas.

```
typesig → LOWER_ID "::" typeexpr
```

Tipos são construídos com a seta `->` (associativa à direita), listas `[T]` e tuplas `(T1, T2)`.

```haskell
soma       :: Int -> Int -> Int
cabeca     :: [Int] -> Int
identidade :: a -> a
main       :: IO ()
```

---

## 4. Tipos Algébricos

Permitem criar tipos com múltiplos construtores.

```
datadecl → "data" UPPER_ID "=" constructorlist
constructorlist → constructor | constructorlist "|" constructor
constructor → UPPER_ID | UPPER_ID typeatoms
```

```haskell
data Forma = Circulo Int
           | Retangulo Int Int

data Arvore = Folha
            | Nodo Int Arvore Arvore
```

---

## 5. Definições de Função

Funções podem ter parâmetros, guardas e cláusula `where`. O compilador testa cada equação de cima para baixo pelo casamento de padrões.

**Sem parâmetros:**
```haskell
pi = 3
```

**Com parâmetros:**
```haskell
soma x y = x + y
```

**Com guardas** (condições testadas em sequência):
```haskell
classificar n
    | n < 0     = "negativo"
    | n == 0    = "zero"
    | otherwise = "positivo"
```

**Com `where`** (definições locais):
```haskell
hipotenusa a b = result
    where
        result = a + b
```

---

## 6. Padrões

Padrões aparecem nos argumentos de função, em `case-of` e em lambdas.

| Padrão | Exemplo | Significado |
|:---|:---|:---|
| Coringa | `_` | Aceita qualquer valor, não vincula |
| Variável | `x` | Vincula o valor ao nome `x` |
| Construtor | `Circulo` | Construtor sem argumentos |
| Literal inteiro | `0` | Aceita apenas o valor 0 |
| Literal booleano | `True` | Aceita apenas True |
| Literal char | `'a'` | Aceita apenas 'a' |
| Cons | `(x:xs)` | Separa cabeça da cauda de uma lista |
| Tupla | `(a, b)` | Desestrutura uma tupla |
| Lista | `[a, b]` | Lista com dois elementos exatos |
| Lista vazia | `[]` | Aceita apenas lista vazia |

> **Construtores com argumentos exigem parênteses** nos argumentos de função: `area (Circulo r) = ...`

---

## 7. Expressões

Toda computação em Haskell é uma expressão com um tipo e um valor.

### 7.1 Operadores infixos

A precedência e associatividade dos operadores são declaradas diretamente no PLY (não por estratificação da gramática):

| Prec. | Assoc. | Operadores |
|:---:|:---:|:---|
| 10 | Esq. | Aplicação de função (justaposição) |
| 9 | Dir. | `.` (composição) |
| 9 | Dir. | `-` unário, `not` |
| 8 | Dir. | `^` |
| 7 | Esq. | `*` `/` `div` `mod` |
| 6 | Esq. | `+` `-` |
| 5 | Dir. | `:` `++` |
| 4 | Sem | `==` `/=` `<` `>` `<=` `>=` |
| 3 | Dir. | `&&` |
| 2 | Dir. | `\|\|` |
| 0 | Dir. | `$` |

### 7.2 Aplicação de função

Funções são chamadas por justaposição — sem parênteses nem símbolo especial:

```haskell
dobrar 5       -- aplica dobrar a 5
map f [1,2,3]  -- aplica map a f e à lista
```

### 7.3 if-then-else

Em Haskell, `if-then-else` é uma **expressão** — o `else` é obrigatório e ambos os ramos devem ter o mesmo tipo:

```haskell
absoluto x = if x > 0 then x else 0 - x
```

### 7.4 case-of

Casamento de padrões explícito sobre um valor:

```haskell
descrever n = case n of
    0 -> "zero"
    1 -> "um"
    _ -> "outro"
```

### 7.5 let-in

Define nomes locais dentro de uma expressão:

```haskell
calc = let a = 2
           b = 3
       in a + b
```

### 7.6 Lambda

Define funções anônimas com `\`:

```haskell
dobrar = \x -> x + x
somar  = \x y -> x + y
```

### 7.7 Listas

```haskell
[]           -- lista vazia
[1, 2, 3]    -- lista literal
[1..10]      -- range fechado
[1..]        -- range aberto (lista infinita)
```

### 7.8 Tuplas

```haskell
ponto = (3, 4)
trio  = (1, True, 'a')
```

---

## 8. Notação `do`

Sequencia operações de IO de forma legível:

```haskell
main :: IO ()
main = do
    let x = 42
    return x
```

Dentro do `do`, cada linha é um comando:
- `var <- expr` — extrai valor de uma ação IO
- `let x = expr` — define valor local (sem `in`)
- `expr` — executa ação descartando resultado

---

## 9. Exemplo de Programa Completo

```haskell
data Forma = Circulo Int
           | Retangulo Int Int

area :: Forma -> Int
area f = case f of
    Circulo r     -> r * r
    Retangulo l a -> l * a

classificar :: Int -> String
classificar n
    | n < 0     = "negativo"
    | n == 0    = "zero"
    | otherwise = "positivo"

fatorial :: Int -> Int
fatorial 0 = 1
fatorial n = n * fatorial n

dobrar :: Int -> Int
dobrar = \x -> x + x

main = do
    let r = area (Circulo 5)
    return r
```
