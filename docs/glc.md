# GLC do Subconjunto Haskell

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos entre aspas duplas (").

Os tokens virtuais `VABRE`, `VSEP` e `VFECHA` são emitidos automaticamente pela FSM + Pilha do analisador léxico com base na indentação do código-fonte (regra do *offside*). Eles substituem os delimitadores explícitos `{`, `;` e `}` que seriam necessários em linguagens como C.

| Token virtual | Equivale a | Quando é emitido |
|:---:|:---:|:---|
| `VABRE` | `{` | Após `where`, `let`, `do`, `of`, ao abrir um novo nível de indentação |
| `VSEP` | `;` | Quando uma linha começa no mesmo nível de indentação do bloco atual |
| `VFECHA` | `}` | Quando uma linha começa em nível inferior ao do bloco atual |

---

## Programa

```
program → topdecl
        | program VSEP topdecl
        | program VSEP
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
typesig → ID_MIN "::" typeexpr

typeexpr → typeterm
         | typeterm "->" typeexpr

typeterm → ID_MAI
         | ID_MIN
         | "(" typeexpr ")"
         | "(" ")"
         | "[" typeexpr "]"
```

---

## Declarações de Tipo Algébrico

```
datadecl → "data" ID_MAI "=" constructorlist

constructorlist → constructor
                | constructorlist "|" constructor

constructor → ID_MAI
            | ID_MAI typeatoms

typeatoms → ID_MAI
           | typeatoms ID_MAI
```

---

## Definições de Função

```
funcdecl → ID_MIN "=" expr
          | ID_MIN simplepats "=" expr
          | ID_MIN "=" expr "where" VABRE localdecls VFECHA
          | ID_MIN simplepats "=" expr "where" VABRE localdecls VFECHA
          | ID_MIN guards
          | ID_MIN simplepats guards

simplepats → simplepat
           | simplepats simplepat

simplepat → ID_MIN
          | "_"
          | INT
          | TRUE
          | FALSE
          | CARACTERE
          | ID_MAI
          | "(" pattern ")"

guards → guard
       | guards guard

guard → "|" expr "=" expr

localdecls → localdecl
           | localdecls VSEP localdecl

localdecl → funcdecl
           | typesig
```

---

## Padrões

```
pattern → ID_MIN
        | "_"
        | ID_MAI
        | ID_MAI simplepats
        | INT
        | TRUE
        | FALSE
        | CARACTERE
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

atom → ID_MIN
     | ID_MAI
     | INT
     | TRUE
     | FALSE
     | CARACTERE
     | STRING
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

caseexpr → "case" expr "of" VABRE casealts VFECHA

casealts → casealt
         | casealts VSEP casealt

casealt → pattern "->" expr
```

---

## Let-in e Do

```
letexpr → "let" VABRE localdecls VFECHA "in" expr

doexpr → "do" VABRE dostmts VFECHA

dostmts → dostmt
        | dostmts VSEP dostmt

dostmt → ID_MIN "<-" expr
       | "let" VABRE localdecls VFECHA
       | "return" atom
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
