# GLC do Subconjunto Haskell

Terminais são representados pelos elementos cuja grafia está em maiúsculo, bem como pelos símbolos que estão entre aspas duplas (").

Os tokens em maiúsculo reconhecidos pelo léxico são:

| Token      | Descrição                                  |
|:----------:|:-------------------------------------------|
| `LOWER_ID` | Identificador iniciado com letra minúscula ou `_` |
| `UPPER_ID` | Identificador iniciado com letra maiúscula  |
| `INT`      | Literal inteiro                            |
| `FLOAT`    | Literal de ponto flutuante                 |
| `CHAR`     | Literal de caractere (`'a'`)               |
| `STRING`   | Literal de string (`"texto"`)              |

---

## Programa

```
program → topdecl
        | topdecl program

topdecl → typesig
        | funcdecl
        | datadecl
        | typealias
```

---

## Assinaturas de Tipo

```
typesig → LOWER_ID "::" typeexpr

typeexpr → typeatom
         | typeatom "->" typeexpr
         | "[" typeexpr "]"
         | "(" typeexprlist ")"
         | "(" ")"

typeexprlist → typeexpr
             | typeexpr "," typeexprlist

typeatom → "Int"
         | "Float"
         | "Bool"
         | "Char"
         | "String"
         | "IO" typeatom
         | "(" ")"
         | UPPER_ID
         | LOWER_ID
```

---

## Declarações de Tipo Algébrico e Sinônimo

```
datadecl → "data" UPPER_ID "=" constructorlist

constructorlist → constructor
                | constructor "|" constructorlist

constructor → UPPER_ID
            | UPPER_ID typeatoms

typeatoms → typeatom
          | typeatom typeatoms

typealias → "type" UPPER_ID "=" typeexpr
```

---

## Definições de Função

```
funcdecl → LOWER_ID patternlist "=" expr
          | LOWER_ID patternlist "=" expr whereclause
          | LOWER_ID patternlist guards
          | LOWER_ID patternlist guards whereclause
          | LOWER_ID "=" expr
          | LOWER_ID "=" expr whereclause

patternlist → pattern
            | pattern patternlist

guards → guard
       | guard guards

guard → "|" expr "=" expr

whereclause → "where" localdecls

localdecls → localdecl
           | localdecl localdecls

localdecl → funcdecl
           | typesig
```

---

## Padrões

```
pattern → "_"
        | LOWER_ID
        | UPPER_ID
        | UPPER_ID patternlist
        | INT
        | FLOAT
        | CHAR
        | "True"
        | "False"
        | "(" pattern ")"
        | "(" pattern "," patterntuplelist ")"
        | "[" "]"
        | "[" patterncommalist "]"
        | pattern ":" pattern
        | LOWER_ID "@" pattern

patterntuplelist → pattern
                 | pattern "," patterntuplelist

patterncommalist → pattern
                 | pattern "," patterncommalist
```

---

## Expressões

```
expr → lambdaexpr
     | letexpr
     | ifexpr
     | caseexpr
     | doexpr
     | infixexpr

lambdaexpr → "\" patternlist "->" expr

letexpr → "let" localdecls "in" expr

ifexpr → "if" expr "then" expr "else" expr

caseexpr → "case" expr "of" casealts

casealts → casealt
          | casealt casealts

casealt → pattern "->" expr
         | pattern "->" expr whereclause

doexpr → "do" dostmts

dostmts → dostmt
         | dostmt dostmts

dostmt → LOWER_ID "<-" expr
        | "let" localdecls
        | expr
```

---

## Expressões Infixas

```
infixexpr → infixexpr "+"   infixexpr
          | infixexpr "-"   infixexpr
          | infixexpr "*"   infixexpr
          | infixexpr "/"   infixexpr
          | infixexpr "^"   infixexpr
          | infixexpr "div" infixexpr
          | infixexpr "mod" infixexpr
          | infixexpr "++"  infixexpr
          | infixexpr ":"   infixexpr
          | infixexpr "=="  infixexpr
          | infixexpr "/="  infixexpr
          | infixexpr "<"   infixexpr
          | infixexpr ">"   infixexpr
          | infixexpr "<="  infixexpr
          | infixexpr ">="  infixexpr
          | infixexpr "&&"  infixexpr
          | infixexpr "||"  infixexpr
          | infixexpr "."   infixexpr
          | infixexpr "$"   infixexpr
          | unaryexpr

unaryexpr → "-" appexpr
           | "not" appexpr
           | appexpr

appexpr → appexpr atomexpr
         | atomexpr
```

---

## Expressões Atômicas

```
atomexpr → LOWER_ID
          | UPPER_ID
          | INT
          | FLOAT
          | CHAR
          | STRING
          | "True"
          | "False"
          | "(" expr ")"
          | "(" expr "," exprtuplelist ")"
          | "[" "]"
          | "[" exprlist "]"
          | "[" expr ".." "]"
          | "[" expr ".." expr "]"
          | "[" expr "," expr ".." "]"
          | "[" expr "," expr ".." expr "]"
          | "[" expr "|" quallist "]"

exprtuplelist → expr
              | expr "," exprtuplelist

exprlist → expr
          | expr "," exprlist

quallist → qual
          | qual "," quallist

qual → LOWER_ID "<-" expr
      | expr
```

---

## Exemplo de Programa

```haskell
data Forma = Circulo Float
           | Retangulo Float Float

calcArea :: Forma -> Float
calcArea forma = case forma of
    Circulo r     -> 3.14 * r ^ 2
    Retangulo l a -> l * a

fatorial :: Int -> Int
fatorial 0 = 1
fatorial n = n * fatorial (n - 1)

classificar :: Int -> String
classificar n
    | n < 0     = "negativo"
    | n == 0    = "zero"
    | otherwise = "positivo"

main :: IO ()
main = do
    let area = calcArea (Circulo 5.0)
    let fat  = fatorial 6
    return ()
```
