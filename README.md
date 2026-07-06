# λ Compilador Haskell - Linguagens Formais e Tradutores

---

## 📋 Sobre o Projeto

Este repositório contém a implementação de um **mini-compilador** para um subconjunto da linguagem **Haskell**, cobrindo todas as etapas clássicas do processo de compilação: análise léxica, análise sintática, construção da árvore sintática abstrata, análise semântica e geração de código.

Haskell é uma linguagem puramente funcional, de tipagem estática e forte, com avaliação preguiçosa (*lazy evaluation*). A escolha da linguagem torna o projeto especialmente interessante por suas particularidades: imutabilidade por padrão, casamento de padrões, ausência de laços imperativos e a regra do *offside* para delimitação de blocos por indentação.

---

## 🔤 O Subconjunto da Linguagem

O compilador cobre um subconjunto expressivo de Haskell, incluindo:

- **Funções** com múltiplas equações e casamento de padrões
- **Assinaturas de tipo** com `::` e tipos algébricos com `data`
- **Expressões** aritméticas, relacionais e lógicas
- **Estruturas de controle** funcionais: `if-then-else`, `case-of`
- **Definições locais** com `let-in` e `where`
- **Listas**: literais, ranges (`[1..10]`) e compreensões
- **Lambdas** (`\x -> expr`) e composição de funções (`.`)
- **Notação `do`** para sequenciamento de operações de IO

---

## 🛠️ Tecnologias

| Ferramenta | Uso |
|:----------:|:----|
| Python 3   | Linguagem de implementação do compilador |
| PLY (Python Lex-Yacc) | Geração do analisador léxico e sintático |

---

## ⚙️ Como Executar

### Pré-requisitos

```bash
pip install -r requirements.txt
```

### Executando o compilador

```bash
python src/main.py <arquivo.hs>
```

---

## 👥 Equipe

* Guilhereme Seixas ([@guilheeme1108-prog](https://github.com/guilheeme1108-prog/))
* Igor Dias ([@iidias](https://github.com/iidias/))
* Igor Lemos ([@IgorLemos01](https://github.com/IgorLemos01))
* Yasmim Passos ([@yasmim-passos](https://github.com/yasmim-passos/))
  
---

## 📄 Licença

Este projeto é de uso acadêmico.
