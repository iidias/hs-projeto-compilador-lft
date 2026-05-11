# λ Documentação Léxica — Linguagem Haskell

## 1. Introdução

Este documento descreve os elementos léxicos do subconjunto da linguagem **Haskell** definido para fins didáticos na disciplina de Linguagens Formais e Tradutores.

Haskell é uma linguagem puramente funcional, de tipagem estática e forte, com avaliação preguiçosa (*lazy evaluation*). Para viabilizar a implementação de um compilador completo dentro do escopo da disciplina, foi definido um subconjunto da linguagem original que preserva suas principais características: funções puras, imutabilidade por padrão, casamento de padrões e expressões *let/where*.

> **Nota sobre layout (regra do *offside*):** Haskell utiliza indentação para delimitar blocos, dispensando chaves e ponto e vírgula na maioria dos contextos. O analisador léxico é responsável por rastrear os níveis de indentação e emitir os tokens virtuais `{`, `}` e `;` conforme a regra do *offside*, compatível com o padrão Haskell 2010.

---

## 2. Palavras Reservadas

Palavras reservadas são identificadores com significado especial na linguagem e **não podem** ser utilizadas como nomes de variáveis, funções ou outros símbolos definidos pelo programador. São sempre escritas em letras minúsculas, exceto os literais booleanos.

### 2.1 Literais Booleanos

| Token   | Descrição                      |
|:-------:|:-------------------------------|
| `True`  | Representa o valor booleano verdadeiro |
| `False` | Representa o valor booleano falso      |

> **Atenção:** Em Haskell, `True` e `False` iniciam com letra **maiúscula**, pois são construtores de dados do tipo `Bool`. Tratá-los como identificadores comuns é um erro léxico.

### 2.2 Controle de Fluxo

| Token    | Descrição |
|:--------:|:----------|
| `if`     | Inicia uma expressão condicional |
| `then`   | Define o ramo verdadeiro do `if` |
| `else`   | Define o ramo falso do `if` (obrigatório em Haskell) |
| `case`   | Inicia uma expressão de casamento de padrões |
| `of`     | Acompanha o `case`, introduzindo as alternativas de padrão |
| `where`  | Introduz definições locais ao final de uma declaração |
| `let`    | Introduz definições locais dentro de uma expressão |
| `in`     | Delimita o escopo das definições introduzidas por `let` |

### 2.3 Definição de Funções e Tipos

| Token    | Descrição |
|:--------:|:----------|
| `do`     | Introduz um bloco de notação monádica (para IO e similares) |
| `return` | Envolve um valor puro no contexto monádico |
| `data`   | Declara um novo tipo de dado algébrico |
| `type`   | Declara um sinônimo de tipo |

---

## 3. Operadores

Os operadores definem as operações que podem ser realizadas sobre valores e expressões. A tabela de precedência abaixo segue o padrão **Haskell 2010**, em ordem **decrescente** de precedência (quanto maior o número, maior a precedência).

### 3.1 Operadores Aritméticos

| Operador | Descrição            | Precedência | Associatividade       |
|:--------:|:---------------------|:-----------:|:---------------------:|
| `^`      | Exponenciação inteira | 8           | Direita para esquerda |
| `*`      | Multiplicação         | 7           | Esquerda para direita |
| `/`      | Divisão real          | 7           | Esquerda para direita |
| `div`    | Divisão inteira       | 7           | Esquerda para direita |
| `mod`    | Módulo / resto        | 7           | Esquerda para direita |
| `+`      | Adição                | 6           | Esquerda para direita |
| `-`      | Subtração             | 6           | Esquerda para direita |

> **Nota:** `div` e `mod` são funções infixas escritas sem backticks na gramática deste subconjunto. Quando usadas como operadores infix com backticks (`` `div` ``), mantêm a mesma precedência.

### 3.2 Operadores de Lista

| Operador | Descrição                         | Precedência | Associatividade       |
|:--------:|:----------------------------------|:-----------:|:---------------------:|
| `:`      | Construção de lista (*cons*)       | 5           | Direita para esquerda |
| `++`     | Concatenação de listas             | 5           | Direita para esquerda |

### 3.3 Operadores Relacionais e de Igualdade

| Operador | Descrição          | Precedência | Associatividade     |
|:--------:|:-------------------|:-----------:|:-------------------:|
| `==`     | Igualdade          | 4           | Sem associatividade |
| `/=`     | Diferença          | 4           | Sem associatividade |
| `<`      | Menor que          | 4           | Sem associatividade |
| `>`      | Maior que          | 4           | Sem associatividade |
| `<=`     | Menor ou igual     | 4           | Sem associatividade |
| `>=`     | Maior ou igual     | 4           | Sem associatividade |

> **Nota:** Operadores relacionais não são associativos em Haskell. Expressões como `1 < x < 10` são inválidas e constituem um erro sintático.

### 3.4 Operadores Lógicos

| Operador | Descrição      | Precedência | Associatividade       |
|:--------:|:---------------|:-----------:|:---------------------:|
| `&&`     | E lógico        | 3           | Direita para esquerda |
| `\|\|`   | OU lógico       | 2           | Direita para esquerda |

> **Nota:** A negação lógica (`not`) é uma **função**, não um operador simbólico. Portanto, é reconhecida como identificador reservado no léxico: `not True` → `False`.

### 3.5 Operadores Funcionais e de Tipo

| Operador | Descrição                                      | Precedência | Associatividade       |
|:--------:|:-----------------------------------------------|:-----------:|:---------------------:|
| `$`      | Aplicação de função com baixa precedência       | 0           | Direita para esquerda |
| `.`      | Composição de funções                          | 9           | Direita para esquerda |
| `->`     | Seta de tipo (em assinaturas e lambdas)        | —           | —                     |
| `::`     | Anotação de tipo                               | —           | —                     |
| `=`      | Definição de função/variável                   | —           | —                     |
| `\`      | Introdução de expressão lambda (*backslash*)   | —           | —                     |

Exemplos de uso de cada operador funcional:

```haskell
-- (::) anotação de tipo: informa ao compilador o tipo esperado
soma :: Int -> Int -> Int

-- (->) seta de tipo: separa tipos de entrada e saída em assinaturas e lambdas
multiplicar :: Int -> Int -> Int   -- dois Ints de entrada, um Int de saída

-- (\) lambda: define uma função anônima sem precisar nomeá-la
dobrar = \x -> x * 2              -- equivale a: dobrar x = x * 2

-- (.) composição: encadeia funções da direita para a esquerda
dobrarEAbs = abs . (*2)           -- aplica (*2) primeiro, depois abs

-- ($) aplicação: evita parênteses, tudo à direita é avaliado antes
resultado = dobrar $ 3 + 2        -- equivale a: dobrar (3 + 2) = 10
-- sem ($) seria necessário: dobrar (3 + 2)
```

### 3.6 Tabela Consolidada de Precedência

| Precedência | Associatividade       | Operadores                            |
|:-----------:|:---------------------:|:--------------------------------------|
| 9           | Direita para esquerda | `.`                                   |
| 8           | Direita para esquerda | `^`                                   |
| 7           | Esquerda para direita | `*`, `/`, `div`, `mod`                |
| 6           | Esquerda para direita | `+`, `-`                              |
| 5           | Direita para esquerda | `:`, `++`                             |
| 4           | Sem associatividade   | `==`, `/=`, `<`, `>`, `<=`, `>=`      |
| 3           | Direita para esquerda | `&&`                                  |
| 2           | Direita para esquerda | `\|\|`                                |
| 0           | Direita para esquerda | `$`                                   |

> A **aplicação de função** (por justaposição, sem símbolo) possui a maior precedência de todas (nível 10 implícito).

---

## 4. Delimitadores

Os delimitadores são símbolos utilizados para estruturar o código-fonte, organizar expressões e definir blocos.

| Delimitador | Descrição |
|:-----------:|:----------|
| `(`  `)`    | Agrupamento de expressões, tuplas e chamadas de função |
| `[`  `]`    | Listas literais e compreensões de lista |
| `{`  `}`    | Blocos explícitos (alternativa à indentação) |
| `,`          | Separação de elementos em tuplas e listas |
| `;`          | Separação de comandos em blocos explícitos |
| `_`          | Padrão coringa (*wildcard*) em casamento de padrões |
| `..`         | Intervalo em listas (`[1..10]`) |
| `|`          | Separador de guardas e alternativas de tipo algébrico |
| `@`          | Padrão *as* em casamento de padrões (`xs@(x:_)`) |

---

## 5. Identificadores

Haskell distingue dois tipos de identificadores com regras de formação distintas, determinadas pela **letra inicial**.

### 5.1 Identificadores de Variáveis e Funções (minúsculos)

Devem iniciar com **letra minúscula** (a–z) ou **sublinhado** (`_`). Após o primeiro caractere, podem conter letras (maiúsculas ou minúsculas), dígitos (0–9), sublinhados (`_`) e apóstrofos (`'`).

```
-- Exemplos válidos
x
contador
minhaFuncao
somaLista'
valor_1
_auxiliar
calcular'resultado
```

### 5.2 Identificadores de Tipos e Construtores (maiúsculos)

Devem iniciar com **letra maiúscula** (A–Z). Após o primeiro caractere, seguem as mesmas regras dos identificadores minúsculos.

```
-- Exemplos válidos (tipos e construtores)
Bool
Int
MeuTipo
Nodo
ListaVazia
```

### 5.3 Regras Gerais

- Identificadores são **sensíveis a maiúsculas e minúsculas** (*case-sensitive*): `valor` e `Valor` são dois identificadores distintos.
- Identificadores **não podem** coincidir com palavras reservadas da linguagem.
- O apóstrofo (`'`) é permitido no meio ou no final de um identificador (e.g., `x'`, `go'`), mas **não** no início.
- O sublinhado simples `_` sozinho é o padrão coringa e não é um identificador de variável.

---

## 6. Literais Numéricos

O subconjunto suporta literais numéricos inteiros e de ponto flutuante, entretanto esse último não será utilzado agora.

### 6.1 Inteiros

Sequência de um ou mais dígitos decimais (0–9), sem separadores.

```
0   42   1000   99
```

> **Nota:** Números negativos **não são literais** em Haskell; são a aplicação do operador de negação unária (`negate`) a um literal positivo. Portanto, `-5` é tokenizado como dois tokens: `-` e `5`.

---

## 7. Literais de Caractere e String

### 7.1 Caracteres

Um único caractere entre aspas simples (`'`).

```haskell
'a'   'Z'   '3'   ' '
```

Sequências de escape reconhecidas:

| Sequência | Descrição       |
|:---------:|:----------------|
| `\n`      | Nova linha       |
| `\t`      | Tabulação        |
| `\\`      | Barra invertida  |
| `\'`      | Aspas simples    |
| `\"`      | Aspas duplas     |
| `\0`      | Caractere nulo   |

### 7.2 Strings

Sequência de zero ou mais caracteres entre aspas duplas (`"`). Em Haskell, `String` é equivalente a `[Char]`.

```haskell
"Olá, mundo!"
"Linguagens Formais"
""
"linha1\nlinha2"
```

---

## 8. Comentários

Comentários são ignorados pelo compilador e servem apenas para documentação do código. Dois estilos são suportados:

### 8.1 Comentário de Linha

Inicia com `--` e se estende até o fim da linha.

```haskell
-- Isso é um comentário de linha
x = 10  -- comentário ao final de uma instrução
```

### 8.2 Comentário de Bloco

Delimitado por `{-` e `-}`. Pode se estender por múltiplas linhas e suporta **aninhamento**.

```haskell
{- Isso é um
   comentário de bloco
   {- e pode ser aninhado -}
-}
```

---

## 9. Erros Léxicos

Um erro léxico ocorre quando o analisador encontra uma sequência de caracteres que não corresponde a nenhum token válido da linguagem.

Exemplos de erros léxicos no subconjunto definido:

| Entrada         | Motivo do Erro |
|:----------------|:---------------|
| `2nome`         | Identificador iniciado por dígito |
| `@variavel`     | `@` fora de contexto de padrão *as* |
| `#define`       | Símbolo `#` não pertence ao léxico |
| `'ab'`          | Literal de caractere com mais de um símbolo |
| `3.`            | Literal de ponto flutuante sem parte fracionária |
| `` `123` ``     | Backtick aplicado a literal, não a identificador |

---

## 10. Espaços em Branco e Quebras de Linha

Espaços em branco (` `), tabulações (`\t`) e quebras de linha (`\n`) são **ignorados** como tokens, mas cumprem dois papéis fundamentais:

1. **Separadores de tokens:** `let x=1` e `let x = 1` produzem a mesma sequência de tokens.
2. **Indentação (regra do *offside*):** A posição da coluna do primeiro token de cada linha é usada para inferir a estrutura de blocos. O analisador léxico mantém uma pilha de níveis de indentação e emite tokens virtuais `{`, `}` e `;` conforme necessário. A variável `lineno` rastreia a linha corrente para mensagens de erro.

### Regra do *Offside* — Como Funciona

Quando o léxico encontra as palavras-chave `where`, `let`, `do` ou `of`, ele registra a coluna do **próximo token** como o nível de indentação do bloco. A partir daí:

- Uma linha que começa na **mesma coluna** → novo item do bloco (token virtual `;`)
- Uma linha que começa **mais à direita** → continuação do item atual
- Uma linha que começa **mais à esquerda** → fim do bloco (token virtual `}`)

```haskell
-- ✅ Indentação VÁLIDA: x, y e z estão alinhados na mesma coluna,
--    sendo interpretados como três definições separadas do where.
hipotenusa a b = raiz
    where
        raiz  = sqrt soma  -- coluna 9 → abre o bloco
        soma  = a^2 + b^2  -- coluna 9 → mesmo nível, novo item (`;` virtual)
        msg   = "ok"       -- coluna 9 → mesmo nível, novo item (`;` virtual)
--  ↑ fim do where pois a próxima linha voltará à coluna 1 (`}` virtual)

-- ❌ Indentação INVÁLIDA: y está menos indentado que x,
--    fazendo o léxico fechar o bloco do where prematuramente.
hipotenusa a b = raiz
    where
        raiz = sqrt soma   -- coluna 9 → abre o bloco
      soma = a^2 + b^2     -- coluna 7 → ERRO: fecha o bloco antes de soma ser definida
```

> **Importante:** misturar espaços e tabulações para indentação pode causar erros difíceis de diagnosticar. O subconjunto adota a convenção de usar **apenas espaços**.

---

## 11. Resumo dos Tokens

| Categoria             | Exemplos                                      |
|:----------------------|:----------------------------------------------|
| Palavras reservadas   | `if`, `then`, `else`, `let`, `in`, `where`, `case`, `of`, `do`, `return`, `data`, `type`, `True`, `False` |
| Operadores aritméticos| `+`, `-`, `*`, `/`, `^`, `div`, `mod`         |
| Operadores de lista   | `:`, `++`                                     |
| Operadores relacionais| `==`, `/=`, `<`, `>`, `<=`, `>=`              |
| Operadores lógicos    | `&&`, `\|\|`                                  |
| Operadores funcionais | `.`, `$`, `->`, `::`, `=`, `\`               |
| Delimitadores         | `(`, `)`, `[`, `]`, `{`, `}`, `,`, `;`, `_`, `\|`, `..`, `@` |
| Identificadores var.  | `x`, `minhaFuncao`, `somaLista'`, `_aux`      |
| Identificadores tipo  | `Int`, `Bool`, `MeuTipo`                      |
| Inteiros              | `0`, `42`, `1000`                             |
| Caracteres            | `'a'`, `'\n'`                                 |
| Strings               | `"Olá"`, `""`                                 |
| Comentários           | `-- ...`, `{- ... -}`                         |
