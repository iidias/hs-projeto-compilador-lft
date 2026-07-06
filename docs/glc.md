# GLC do Subconjunto Haskell

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos entre aspas duplas (").

Os tokens virtuais `VOPEN`, `VSEMI` e `VCLOSE` são emitidos automaticamente pela FSM + Pilha do analisador léxico com base na indentação do código-fonte (regra do *offside*). Eles substituem os delimitadores explícitos `{`, `;` e `}` que seriam necessários em linguagens como C.

| Token virtual | Equivale a | Quando é emitido |
|:---:|:---:|:---|
| `VOPEN` | `{` | Após `where`, `let`, `do`, `of`, ao abrir um novo nível de indentação |
| `VSEMI` | `;` | Quando uma linha começa no mesmo nível de indentação do bloco atual |
| `VCLOSE` | `}` | Quando uma linha começa em nível inferior ao do bloco atual |

---

## Programa

```
program → topdecl
        | program VSEMI topdecl
        | program VSEMI
```

---

## Declarações de Alto Nível

```
topdecl → typesig
        | funcdecl
        | datadecl
```

---

## Assinaturas de Tipo

```
typesig → LOWER_ID "::" typeexpr

typeexpr → typeterm
         | typeterm "->" typeexpr

typeterm → UPPER_ID
         | LOWER_ID
         | "(" typeexpr ")"
         | "(" ")"
         | "[" typeexpr "]"
```

---

## Declarações de Tipo Algébrico

```
datadecl → "data" UPPER_ID "=" constructorlist

constructorlist → constructor
                | constructorlist "|" constructor

constructor → UPPER_ID
            | UPPER_ID typeatoms

typeatoms → UPPER_ID
           | typeatoms UPPER_ID
```

---

## Definições de Função

```
funcdecl → LOWER_ID "=" expr
          | LOWER_ID simplepats "=" expr
          | LOWER_ID "=" expr "where" VOPEN localdecls VCLOSE
          | LOWER_ID simplepats "=" expr "where" VOPEN localdecls VCLOSE
          | LOWER_ID guards
          | LOWER_ID simplepats guards

simplepats → simplepat
           | simplepats simplepat

simplepat → LOWER_ID
          | "_"
          | INT
          | TRUE
          | FALSE
          | CHAR
          | UPPER_ID
          | "(" pattern ")"

guards → guard
       | guards guard

guard → "|" expr "=" expr

localdecls → localdecl
           | localdecls VSEMI localdecl

localdecl → funcdecl
           | typesig
```

---

## Padrões

```
pattern → LOWER_ID
        | "_"
        | UPPER_ID
        | INT
        | TRUE
        | FALSE
        | CHAR
        | "(" pattern ")"
        | "(" pattern "," patterntuple ")"
        | "[" "]"
        | "[" patternlist "]"
        | pattern ":" pattern

patterntuple → pattern
             | patterntuple "," pattern

patternlist → pattern
            | patternlist "," pattern
```

---

## Expressões

A ambiguidade dos operadores infixos é resolvida pela tabela de precedência do PLY, não por estratificação da gramática.

```
expr → expr "+" expr
     | expr "-" expr
     | expr "*" expr
     | expr "/" expr
     | expr "^" expr
     | expr "div" expr
     | expr "mod" expr
     | expr "++" expr
     | expr ":" expr
     | expr "==" expr
     | expr "/=" expr
     | expr "<" expr
     | expr ">" expr
     | expr "<=" expr
     | expr ">=" expr
     | expr "&&" expr
     | expr "||" expr
     | expr "." expr
     | expr "$" expr
     | "-" expr
     | "not" expr
     | ifexpr
     | caseexpr
     | letexpr
     | doexpr
     | lambdaexpr
     | appexpr

appexpr → appexpr atom
        | atom

atom → LOWER_ID
     | UPPER_ID
     | INT
     | TRUE
     | FALSE
     | CHAR
     | STRING
     | "return"
     | "(" expr ")"
     | "(" expr "," exprtuple ")"
     | "[" "]"
     | "[" exprlist "]"
     | "[" expr ".." "]"
     | "[" expr ".." expr "]"

exprtuple → expr
          | exprtuple "," expr

exprlist → expr
         | exprlist "," expr
```

---

## Estruturas de Controle

```
ifexpr → "if" expr "then" expr "else" expr

caseexpr → "case" expr "of" VOPEN casealts VCLOSE

casealts → casealt
         | casealts VSEMI casealt

casealt → pattern "->" expr
```

---

## Let-in e Do

```
letexpr → "let" VOPEN localdecls VCLOSE "in" expr

doexpr → "do" VOPEN dostmts VCLOSE

dostmts → dostmt
        | dostmts VSEMI dostmt

dostmt → LOWER_ID "<-" expr
       | "let" VOPEN localdecls VCLOSE
       | expr
```

---

## Lambda

```
lambdaexpr → "\" simplepats "->" expr
```

---

## Tabela de Precedência

| Nível | Associatividade | Operadores |
|:---:|:---:|:---|
| 0 (menor) | Direita | `$` |
| 1 | Direita | `\|\|` |
| 2 | Direita | `&&` |
| 3 | Sem assoc. | `==` `/=` `<` `>` `<=` `>=` |
| 4 | Direita | `:` `++` |
| 5 | Esquerda | `+` `-` |
| 6 | Esquerda | `*` `/` `div` `mod` |
| 7 | Direita | `^` |
| 8 | Direita | `.` |
| 9 | Direita | `-` unário, `not` |
| 10 (maior) | Esquerda | Aplicação de função |

---

## Exemplo de Programa

```haskell
data Forma = Circulo Int
           | Retangulo Int Int

area :: Forma -> Int
area f = case f of
    Circulo r      -> r * r
    Retangulo l a  -> l * a

classificar :: Int -> String
classificar n
    | n < 0     = "negativo"
    | n == 0    = "zero"
    | otherwise = "positivo"

dobrar :: Int -> Int
dobrar = \x -> x + x

main = do
    let r = area (Circulo 5)
    return r
```
