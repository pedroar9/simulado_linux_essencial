import streamlit as st
import random
import time
import re
import json
import os
import pandas as pd
from datetime import date, datetime
import pytz

# --- Configuracoes de hora     ---  
fuso_brasilia = pytz.timezone("America/Sao_Paulo")
agora = datetime.now(fuso_brasilia)
data_atual = agora.today().strftime("%d/%m/%Y")


# --- Questoes ---
questions_data = [
  {
    "question": "O que será exibido pelo código:\n```python\nprint(2 + 3 * 4)\n```\n?",
    "options": [
      "20",
      "14",
      "15",
      "24"
    ],
    "answer": "14",
    "explanation": "Em Python, a multiplicação (`*`) tem maior precedência que a adição (`+`). Assim, `3 * 4` é calculado primeiro (12), e depois `2 + 12` resulta em `14`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = 8\nx //= 3\nprint(x)\n```\n?",
    "options": [
      "2",
      "3",
      "2.66",
      "8"
    ],
    "answer": "2",
    "explanation": "O operador `//=` realiza divisão inteira e atribui o resultado à variável. `8 // 3` resulta em `2`, pois a parte decimal é descartada."
  },
  {
    "question": "Qual é o resultado de `list('abc')`?",
    "options": [
      "['a', 'b', 'c']",
      "['abc']",
      "'abc'",
      "Erro"
    ],
    "answer": "['a', 'b', 'c']",
    "explanation": "A função `list()` converte uma string em uma lista, onde cada caractere da string se torna um elemento da lista."
  },
  {
    "question": "O que faz o comando `continue` em um loop?",
    "options": [
      "Para o programa",
      "Sai do loop imediatamente",
      "Pula para a próxima iteração",
      "Reinicia o loop"
    ],
    "answer": "Pula para a próxima iteração",
    "explanation": "O comando `continue` faz o loop pular o restante do código na iteração atual e ir para a próxima iteração."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = [1, 2, 3]\nprint(x[-1])\n```\n?",
    "options": [
      "1",
      "2",
      "3",
      "Erro"
    ],
    "answer": "3",
    "explanation": "O índice `-1` acessa o último elemento de uma lista. Para `x = [1, 2, 3]`, `x[-1]` é `3`."
  },
  {
    "question": "Qual é o resultado de `str(123)`?",
    "options": [
      "123",
      "'123'",
      "[1, 2, 3]",
      "Erro"
    ],
    "answer": "'123'",
    "explanation": "A função `str()` converte um número (ou outro objeto) em uma string. Assim, `123` se torna `'123'`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nfor i in range(1, 4, 2):\n    print(i, end=' ')\n```\n?",
    "options": [
      "1 2 3",
      "1 3",
      "1 2",
      "2 4"
    ],
    "answer": "1 3",
    "explanation": "`range(1, 4, 2)` gera números de 1 até (mas não incluindo) 4, com passo 2. Assim, os números são `1` e `3`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = False\nx = x or True\nprint(x)\n```\n?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "True",
    "explanation": "O operador `or` retorna `True` se pelo menos uma das operandos for `True`. `False or True` resulta em `True`."
  },
  {
    "question": "Qual método adiciona um elemento no início de uma lista?",
    "options": [
      "append()",
      "insert()",
      "add()",
      "extend()"
    ],
    "answer": "insert()",
    "explanation": "O método `insert(index, elemento)` adiciona um elemento na posição especificada. Para o início, usa-se `insert(0, elemento)`."
  },
  {
    "question": "Qual é o resultado de `5 == '5'`?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "False",
    "explanation": "O operador `==` compara valores e tipos. `5` (inteiro) é diferente de `'5'` (string), então o resultado é `False`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nd = {'x': 10}\nprint(d.get('y', 0))\n```\n?",
    "options": [
      "10",
      "0",
      "None",
      "KeyError"
    ],
    "answer": "0",
    "explanation": "O método `get(chave, default)` retorna o valor da chave se ela existir, caso contrário, retorna o valor padrão. Como `'y'` não existe, retorna `0`."
  },
  {
    "question": "O que faz o método `upper()` em uma string?",
    "options": [
      "Converte para minúsculas",
      "Converte para maiúsculas",
      "Remove espaços",
      "Inverte a string"
    ],
    "answer": "Converte para maiúsculas",
    "explanation": "O método `upper()` converte todos os caracteres de uma string para letras maiúsculas."
  },
  {
    "question": "Qual é o resultado de `bool([0])`?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "True",
    "explanation": "Uma lista não vazia, mesmo contendo `0`, é considerada `True` em um contexto booleano."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = 4\nprint(x / 2)\n```\n?",
    "options": [
      "2",
      "2.0",
      "4",
      "Erro"
    ],
    "answer": "2.0",
    "explanation": "O operador `/` realiza divisão com resultado em ponto flutuante. `4 / 2` resulta em `2.0`."
  },
  {
    "question": "Qual palavra-chave é usada para capturar uma exceção em Python?",
    "options": [
      "try",
      "except",
      "catch",
      "finally"
    ],
    "answer": "except",
    "explanation": "A palavra-chave `except` é usada para capturar e tratar exceções levantadas em um bloco `try`."
  },
  {
    "question": "Qual é o resultado de `(1, 2, 3)[1]`?",
    "options": [
      "1",
      "2",
      "3",
      "Erro"
    ],
    "answer": "2",
    "explanation": "O índice `[1]` acessa o segundo elemento da tupla `(1, 2, 3)`, que é `2`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = {1, 2, 2}\nprint(len(x))\n```\n?",
    "options": [
      "2",
      "3",
      "1",
      "Erro"
    ],
    "answer": "2",
    "explanation": "Um conjunto (`set`) não permite elementos duplicados. `{1, 2, 2}` é reduzido a `{1, 2}`, e `len()` retorna `2`."
  },
  {
    "question": "Qual operador realiza divisão inteira em Python?",
    "options": [
      "/",
      "//",
      "%",
      "**"
    ],
    "answer": "//",
    "explanation": "O operador `//` realiza divisão inteira, retornando o quociente sem a parte decimal."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = 'hello'\nprint(x[1:3])\n```\n?",
    "options": [
      "he",
      "el",
      "ll",
      "lo"
    ],
    "answer": "el",
    "explanation": "O fatiamento `[1:3]` extrai os caracteres do índice 1 até (mas não incluindo) o índice 3, resultando em `'el'`."
  },  
  {
    "question": "Qual é o resultado de `max([3, 1, 4, 1, 5])`?",
    "options": [
      "3",
      "4",
      "5",
      "Erro"
    ],
    "answer": "5",
    "explanation": "A função `max()` retorna o maior valor em um iterável. Para `[3, 1, 4, 1, 5]`, o maior valor é `5`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = 0\nwhile x < 2:\n    print(x, end=' ')\n    x += 1\n```\n?",
    "options": [
      "0 1",
      "0 1 2",
      "1 2",
      "Erro"
    ],
    "answer": "0 1",
    "explanation": "O loop `while` executa enquanto `x < 2`, imprimindo `0` e `1`. O `end=' '` adiciona um espaço após cada número."
  },
  {
    "question": "Qual é o tipo de dado retornado por `range(5)`?",
    "options": [
      "list",
      "tuple",
      "range",
      "set"
    ],
    "answer": "range",
    "explanation": "Em Python 3, `range(5)` retorna um objeto do tipo `range`, não uma lista. Pode ser convertido em lista com `list(range(5))`."
  },
  {
    "question": "Qual é o resultado de `'a' in 'cat'`?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "True",
    "explanation": "O operador `in` verifica se `'a'` está na string `'cat'`. Como `'a'` está presente, o resultado é `True`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = [1, 2]\nx.extend([3, 4])\nprint(x)\n```\n?",
    "options": [
      "[1, 2, 3, 4]",
      "[1, 2, [3, 4]]",
      "[1, 2]",
      "Erro"
    ],
    "answer": "[1, 2, 3, 4]",
    "explanation": "O método `extend()` adiciona cada elemento do iterável fornecido ao final da lista."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = 3\nx *= 2\nprint(x)\n```\n?",
    "options": [
      "5",
      "6",
      "9",
      "Erro"
    ],
    "answer": "6",
    "explanation": "O operador `*=` multiplica a variável pelo valor à direita. `x *= 2` é equivalente a `x = x * 2`, então `3 * 2 = 6`."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = None\nprint(x)\n```\n?",
    "options": [
      "None",
      "'None'",
      "0",
      "Erro"
    ],
    "answer": "None",
    "explanation": "A variável `x` contém o valor `None`, que é impresso como `None`."
  },
  {
    "question": "Qual método retorna o número de ocorrências de um elemento em uma lista?",
    "options": [
      "count()",
      "len()",
      "find()",
      "index()"
    ],
    "answer": "count()",
    "explanation": "O método `count()` retorna quantas vezes um elemento aparece em uma lista."
  },
  {
    "question": "Qual é o resultado de `int('123')`?",
    "options": [
      "'123'",
      "123",
      "123.0",
      "Erro"
    ],
    "answer": "123",
    "explanation": "A função `int()` converte uma string que representa um número inteiro em um valor inteiro."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nif 5 > 3:\n    print('Sim')\n```\n?",
    "options": [
      "Sim",
      "Não",
      "None",
      "Erro"
    ],
    "answer": "Sim",
    "explanation": "A condição `5 > 3` é `True`, então o bloco `if` é executado, imprimindo `'Sim'`."
  },
  {
    "question": "Qual é o resultado de `{1: 'a', 2: 'b'}[2]`?",
    "options": [
      "'a'",
      "'b'",
      "2",
      "KeyError"
    ],
    "answer": "'b'",
    "explanation": "O acesso `[2]` retorna o valor associado à chave `2` no dicionário, que é `'b'`."
  },    
  {
    "question": "Qual é o resultado da seguinte expressão: `3 * 'ab'`?",
    "options": [
      "ababab",
      "ab3",
      "Error",
      "aba"
    ],
    "answer": "ababab",
    "explanation": "O operador `*` com uma string e um inteiro realiza a repetição da string."
  },
  {
    "question": "Qual dos seguintes nomes de variáveis é inválido em Python?",
    "options": [
      "_valor",
      "valor_2",
      "2valor",
      "valorTotal"
    ],
    "answer": "2valor",
    "explanation": "Nomes de variáveis em Python não podem começar com um número."
  },
  {
    "question": "O que será exibido pelo código:\n```python\nx = 5\nx += 3\nprint(x)\n```\n?",
    "options": [
      "8",
      "5",
      "3",
      "Erro de sintaxe"
    ],
    "answer": "8",
    "explanation": "`x += 3` é o mesmo que `x = x + 3`. Então, `x` se torna `5 + 3 = 8`."
  },
  {
    "question": "Qual operador é usado para divisão inteira (sem casas decimais) em Python?",
    "options": [
      "/",
      "//",
      "%",
      "div"
    ],
    "answer": "//",
    "explanation": "O operador `//` realiza a divisão inteira, descartando a parte fracionária."
  },
  {
    "question": "Qual função é usada para converter uma string em um número inteiro em Python?",
    "options": [
      "int()",
      "str()",
      "float()",
      "chr()"
    ],
    "answer": "int()",
    "explanation": "A função `int()` converte um valor para o tipo inteiro, se possível."
  },
  {
    "question": "O que a seguinte função retorna quando chamada com `print(f())`?\n```python\ndef f():\n    return 4 + 3\n```\n",
    "options": [
      "7",
      "43",
      "f()",
      "Nada"
    ],
    "answer": "7",
    "explanation": "A função `f` retorna a soma de 4 e 3, que é 7."
  },
  {
    "question": "Qual das seguintes estruturas de controle repete um bloco de código enquanto uma condição é verdadeira?",
    "options": [
      "if",
      "for",
      "while",
      "break"
    ],
    "answer": "while",
    "explanation": "O loop `while` executa um bloco de código repetidamente enquanto sua condição permanecer verdadeira."
  },
  {
    "question": "O que será exibido pelo código: `x = \"abc\"; print(len(x))` ?",
    "options": [
      "2",
      "3",
      "abc",
      "Erro"
    ],
    "answer": "3",
    "explanation": "A função `len()` retorna o número de itens em um container, como o número de caracteres em uma string."
  },
  {
    "question": "Qual é o índice do caractere 'o' na string \"Python\"?",
    "options": [
      "5",
      "4",
      "3",
      "2"
    ],
    "answer": "4",
    "explanation": "Em Python, a indexação de strings começa em 0. 'P' é 0, 'y' é 1, 't' é 2, 'h' é 3, 'o' é 4, 'n' é 5."
  },
  {
    "question": "O que este código imprime: `for i in range(2, 5): print(i, end=' ')` ?",
    "options": [
      "2 3 4 ",
      "2 3 4 5 ",
      "3 4 5 ",
      "1 2 3 4 "
    ],
    "answer": "2 3 4 ",
    "explanation": "`range(2, 5)` gera números de 2 até (mas não incluindo) 5. O `end=' '` imprime um espaço em vez de uma nova linha."
  },
  {
    "question": "Qual é o valor de `x` após esta operação: `x = 10; x %= 4`?",
    "options": [
      "2",
      "0",
      "4",
      "1"
    ],
    "answer": "2",
    "explanation": "O operador `%=` (módulo e atribuição) calcula o resto da divisão de `x` por 4. `10 % 4` é 2."
  },
  {
    "question": "Qual comando finaliza um loop (como `for` ou `while`) imediatamente?",
    "options": [
      "stop",
      "exit",
      "break",
      "continue"
    ],
    "answer": "break",
    "explanation": "O comando `break` é usado para sair de um loop prematuramente."
  },
  {
    "question": "O que a função `input()` retorna em Python?",
    "options": [
      "Sempre um número",
      "Sempre uma string",
      "Nada",
      "Um booleano"
    ],
    "answer": "Sempre uma string",
    "explanation": "A função `input()` lê a entrada do usuário e a retorna como uma string, mesmo que números sejam digitados."
  },
  {
    "question": "Como converter o número de ponto flutuante `5.67` em um inteiro em Python?",
    "options": [
      "float(5.67)",
      "str(5.67)",
      "int(5.67)",
      "bool(5.67)"
    ],
    "answer": "int(5.67)",
    "explanation": "A função `int()` trunca a parte decimal de um número de ponto flutuante, convertendo `5.67` para `5`."
  },
  {
    "question": "Qual é o valor da expressão booleana: `True and False`?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "False",
    "explanation": "O operador `and` retorna `True` somente se ambas as operandas forem `True`. Caso contrário, retorna `False`."
  },
  {
    "question": "Qual destas expressões é booleana e retorna `True`?",
    "options": [
      "5",
      "\"True\"",
      "3 < 5",
      "None"
    ],
    "answer": "3 < 5",
    "explanation": "A expressão `3 < 5` é uma comparação que avalia como `True` porque 3 é de fato menor que 5."
  },
  {
    "question": "Qual é a saída deste código: `x = [1, 2, 3]; x.append(4); print(x)`?",
    "options": [
      "[1, 2, 3]",
      "[1, 2, 3, 4]",
      "[4, 1, 2, 3]",
      "[1, 2, 4]"
    ],
    "answer": "[1, 2, 3, 4]",
    "explanation": "O método `append()` adiciona um elemento ao final de uma lista."
  },
  {
    "question": "Qual função retorna o menor valor de uma lista?",
    "options": [
      "min()",
      "low()",
      "smallest()",
      "bottom()"
    ],
    "answer": "min()",
    "explanation": "A função embutida `min()` retorna o menor item em um iterável ou o menor de dois ou mais argumentos."
  },
  {
    "question": "O que será exibido pelo código:\n```python\na = 5\nb = 2\nprint(a // b)\n```\n?",
    "options": [
      "2.5",
      "2",
      "3",
      "2.0"
    ],
    "answer": "2",
    "explanation": "A divisão inteira `//` de 5 por 2 resulta em 2, pois a parte decimal é descartada."
  },
  {
    "question": "Quais são os possíveis valores de uma variável booleana em Python?",
    "options": [
      "1 e 0",
      "Yes e No",
      "True e False",
      "\"True\" e \"False\""
    ],
    "answer": "True e False",
    "explanation": "Variáveis booleanas em Python podem assumir os valores literais `True` ou `False`."
  },
  {
    "question": "Qual é o resultado de `bool(0)`?",
    "options": [
      "True",
      "False",
      "0",
      "None"
    ],
    "answer": "False",
    "explanation": "Em Python, o valor numérico 0 é considerado `False` em um contexto booleano. Outros valores 'falsy' incluem `None`, listas vazias, strings vazias, etc."
  },
  {
    "question": "O que acontece se você tentar acessar um índice inexistente de uma lista?",
    "options": [
      "Retorna None",
      "Retorna 0",
      "Levanta um erro IndexError",
      "Ignora a operação"
    ],
    "answer": "Levanta um erro IndexError",
    "explanation": "Acessar um índice fora dos limites de uma lista resulta em uma exceção `IndexError`."
  },
  {
    "question": "Qual é o resultado de `type(\"10\")`?",
    "options": [
      "<class 'int'>",
      "<class 'float'>",
      "<class 'str'>",
      "\"str\""
    ],
    "answer": "<class 'str'>",
    "explanation": "A função `type()` retorna o tipo de um objeto. `\"10\"` é uma literal string, então seu tipo é `str`."
  },
  {
    "question": "Qual método é usado para obter todos os pares chave-valor de um dicionário `my_dict`?",
    "options": [
      "my_dict.keys()",
      "my_dict.values()",
      "my_dict.items()",
      "my_dict.pairs()"
    ],
    "answer": "my_dict.items()",
    "explanation": "O método `items()` retorna uma view dos pares (chave, valor) do dicionário."
  },
  {
    "question": "Qual das seguintes afirmações sobre tuplas em Python é VERDADEIRA?",
    "options": [
      "Tuplas são mutáveis.",
      "Tuplas são definidas usando chaves `{}`.",
      "Tuplas podem ser modificadas após a criação usando o método `append()`.",
      "Tuplas são imutáveis."
    ],
    "answer": "Tuplas são imutáveis.",
    "explanation": "Tuplas são sequências ordenadas e imutáveis, o que significa que não podem ser alteradas após sua criação."
  },
  {
    "question": "Qual será a saída do seguinte código?\n```python\nx = 10\ndef my_func():\n    x = 5\n    print(f\"Dentro da função: {x}\")\nmy_func()\nprint(f\"Fora da função: {x}\")\n```",
    "options": [
      "Dentro da função: 5\nFora da função: 10",
      "Dentro da função: 10\nFora da função: 5",
      "Dentro da função: 5\nFora da função: 5",
      "Dentro da função: 10\nFora da função: 10"
    ],
    "answer": "Dentro da função: 5\nFora da função: 10",
    "explanation": "A variável `x` dentro de `my_func` é local para a função (shadowing). A variável `x` global permanece 10."
  },
  {
    "question": "Qual palavra-chave é usada para levantar uma exceção manualmente em Python?",
    "options": [
      "try",
      "except",
      "raise",
      "throw"
    ],
    "answer": "raise",
    "explanation": "A instrução `raise` é usada para forçar a ocorrência de uma exceção específica."
  },
  {
    "question": "Qual é a saída de `'python'.upper()`?",
    "options": [
      "'python'",
      "'PYTHON'",
      "'Python'",
      "Erro"
    ],
    "answer": "'PYTHON'",
    "explanation": "O método de string `upper()` retorna uma cópia da string com todos os caracteres em maiúsculas."
  },
  {
    "question": "Qual bloco de código é executado se uma exceção ocorrer em um bloco `try` e for capturada por um `except` correspondente, antes do bloco `finally`?",
    "options": [
      "O restante do bloco `try`",
      "O bloco `else` associado ao `try-except`",
      "O bloco `except`",
      "Nenhum, o programa encerra"
    ],
    "answer": "O bloco `except`",
    "explanation": "Se uma exceção ocorre no bloco `try`, o restante do bloco `try` é ignorado e o Python procura um bloco `except` correspondente para tratar a exceção. O bloco `finally` é executado depois, independentemente de ter ocorrido exceção ou não."
  },
  {
    "question": "Como você pode adicionar o elemento `7` ao final de uma lista chamada `my_list`?",
    "options": [
      "my_list.add(7)",
      "my_list.push(7)",
      "my_list.insert_end(7)",
      "my_list.append(7)"
    ],
    "answer": "my_list.append(7)",
    "explanation": "O método `append()` é usado para adicionar um item ao final de uma lista."
  },
  {
    "question": "Como você declara uma função em Python?",
    "options": [
      "function nome_da_funcao():",
      "def nome_da_funcao():",
      "nome_da_funcao = function():",
      "nome_da_funcao():"
    ],
    "answer": "def nome_da_funcao():",
    "explanation": "A palavra-chave `def` é usada para definir uma função em Python, seguida pelo nome da função e parênteses."
  },
  {
    "question": "Qual é o resultado de `2 ** 3` em Python?",
    "options": [
      "6",
      "8",
      "9",
      "12"
    ],
    "answer": "8",
    "explanation": "O operador `**` realiza a exponenciação. `2 ** 3` calcula 2 elevado à potência de 3, que é 2 * 2 * 2 = 8."
  },
  {
    "question": "Qual destes tipos de dados é imutável em Python?",
    "options": [
      "list",
      "dictionary",
      "set",
      "tuple"
    ],
    "answer": "tuple",
    "explanation": "Tuplas são imutáveis, o que significa que seus elementos não podem ser alterados após a criação. Listas, dicionários e conjuntos são mutáveis."
  },
  {
    "question": "O que o método `pop()` faz em uma lista?",
    "options": [
      "Adiciona um elemento ao final",
      "Remove um elemento pelo índice",
      "Retorna o comprimento da lista",
      "Inverte a ordem dos elementos"
    ],
    "answer": "Remove um elemento pelo índice",
    "explanation": "O método `pop(index)` remove e retorna o elemento no índice especificado. Se nenhum índice for fornecido, remove e retorna o último elemento."
  },
  {
    "question": "Como você acessa o primeiro elemento de uma lista `my_list`?",
    "options": [
      "my_list[1]",
      "my_list.first()",
      "my_list[0]",
      "my_list.get(0)"
    ],
    "answer": "my_list[0]",
    "explanation": "Em Python, os índices das listas começam em 0. Portanto, o primeiro elemento é acessado com `my_list[0]`."
  },
  {
    "question": "Qual é a saída de `print(type([1, 2, 3]))`?",
    "options": [
      "list",
      "<class 'list'>",
      "array",
      "<type 'list'>"
    ],
    "answer": "<class 'list'>",
    "explanation": "A função `type()` retorna o tipo do objeto passado como argumento. Para uma lista, ela retorna `<class 'list'>`."
  },
  {
    "question": "O que o operador `in` verifica?",
    "options": [
      "Igualdade entre dois valores",
      "Se um valor está contido em uma sequência",
      "Se dois objetos são idênticos",
      "O tipo de um objeto"
    ],
    "answer": "Se um valor está contido em uma sequência",
    "explanation": "O operador `in` verifica se um valor está presente em uma sequência (como uma lista, tupla ou string) e retorna `True` ou `False`."
  },
  {
    "question": "Qual método de string remove espaços em branco do início e do fim de uma string?",
    "options": [
      "strip()",
      "trim()",
      "remove()",
      "whitespace()"
    ],
    "answer": "strip()",
    "explanation": "O método `strip()` remove espaços em branco (e outros caracteres especificados) do início e do fim de uma string."
  },
  {
    "question": "O que a função `range(1, 5)` gera?",
    "options": [
      "Números de 1 a 5 (inclusive)",
      "Números de 1 a 4",
      "Números de 0 a 4",
      "Números de 0 a 5"
    ],
    "answer": "Números de 1 a 4",
    "explanation": "A função `range(start, stop)` gera uma sequência de números do `start` até `stop - 1`. Então, `range(1, 5)` gera 1, 2, 3, 4."
  },
  {
    "question": "Como você itera sobre os pares chave-valor de um dicionário em um loop `for`?",
    "options": [
      "for key, value in my_dict:",
      "for item in my_dict.items():",
      "for key in my_dict.keys(): for value in my_dict.values():",
      "for (key, value) in my_dict:"
    ],
    "answer": "for item in my_dict.items():",
    "explanation": "O método `items()` retorna uma view dos pares (chave, valor) do dicionário, que pode ser iterada com um loop `for`."
  },
  {
    "question": "Qual palavra-chave é usada para definir uma classe em Python?",
    "options": [
      "object",
      "class",
      "def",
      "type"
    ],
    "answer": "class",
    "explanation": "A palavra-chave `class` é usada para definir uma nova classe em Python, que serve como um modelo para criar objetos."
  },
  {
    "question": "O que um construtor (`__init__`) faz em uma classe?",
    "options": [
      "Define um método estático",
      "Inicializa um objeto da classe",
      "Declara variáveis globais",
      "Cria uma subclasse"
    ],
    "answer": "Inicializa um objeto da classe",
    "explanation": "O método construtor `__init__` é chamado quando um objeto da classe é criado e é usado para inicializar os atributos do objeto."
  },
  {
    "question": "Qual é a finalidade da palavra-chave `self` em métodos de classe?",
    "options": [
      "Referencia a classe em si",
      "Referencia a instância atual da classe",
      "Cria uma nova instância da classe",
      "Acessa atributos de uma superclasse"
    ],
    "answer": "Referencia a instância atual da classe",
    "explanation": "O parâmetro `self` é uma convenção que referencia a instância atual do objeto, permitindo que você acesse seus atributos e métodos."
  },
  {
    "question": "Como você importa um módulo chamado `math` em Python?",
    "options": [
      "include math",
      "import module math",
      "import math",
      "using math"
    ],
    "answer": "import math",
    "explanation": "A instrução `import math` importa o módulo `math`, permitindo que você use suas funções e constantes."
  },
  {
    "question": "Qual é a função de `try`, `except` e `finally`?",
    "options": [
      "Gerenciamento de loops",
      "Definição de funções recursivas",
      "Gerenciamento de exceções",
      "Trabalhar com arquivos"
    ],
    "answer": "Gerenciamento de exceções",
    "explanation": "`try` tenta executar um bloco de código, `except` captura e trata exceções, e `finally` executa um bloco de código independentemente de exceções ocorrerem ou não."
  },
  {
    "question": "O que o método `keys()` retorna em um dicionário?",
    "options": [
      "Uma lista de valores",
      "Uma lista de chaves",
      "Uma lista de pares (chave, valor)",
      "O número de itens no dicionário"
    ],
    "answer": "Uma lista de chaves",
    "explanation": "O método `keys()` retorna uma view das chaves do dicionário."
  },
  {
    "question": "Como você cria uma cópia de uma lista `my_list`?",
    "options": [
      "new_list = my_list",
      "new_list = my_list.copy()",
      "new_list = copy(my_list)",
      "new_list = my_list[:]"
    ],
    "answer": "new_list = my_list[:]",
    "explanation": "A fatia `[:]` cria uma cópia superficial da lista.  `new_list = my_list` apenas cria outra referência à mesma lista."
  },
  {
    "question": "Qual é o resultado de `print(10 == \"10\")`?",
    "options": [
      "True",
      "False",
      "Erro",
      "None"
    ],
    "answer": "False",
    "explanation": "O operador `==` compara valores para igualdade. Ele retorna `False` porque 10 (um inteiro) não é igual a \"10\" (uma string)."
  },
  {
    "question": "O que o operador `is` verifica?",
    "options": [
      "Igualdade de valor",
      "Identidade de objeto",
      "Tipo de dado",
      "Se um objeto é None"
    ],
    "answer": "Identidade de objeto",
    "explanation": "O operador `is` verifica se duas variáveis referenciam o mesmo objeto na memória, não apenas se têm o mesmo valor."
  },
  {
    "question": "Como você converte um valor para o tipo booleano em Python?",
    "options": [
      "bool()",
      "boolean()",
      "to_bool()",
      "as_bool()"
    ],
    "answer": "bool()",
    "explanation": "A função `bool()` converte um valor para o tipo booleano. Valores como 0, `None`, e sequências vazias se tornam `False`; outros se tornam `True`."
  },
  {
    "question": "Qual é o resultado de `print(True or False)`?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "True",
    "explanation": "O operador `or` retorna `True` se pelo menos uma das operandas for `True`."
  },
  {
    "question": "O que o operador `not` faz?",
    "options": [
      "Nega um valor booleano",
      "Compara dois valores",
      "Realiza uma operação bit a bit",
      "Calcula o módulo de um número"
    ],
    "answer": "Nega um valor booleano",
    "explanation": "O operador `not` inverte o valor de um booleano. Se a operanda for `True`, retorna `False`, e vice-versa."
  },
  {
    "question": "O que o método `insert(index, value)` faz em uma lista?",
    "options": [
      "Adiciona um elemento ao final",
      "Insere um elemento no índice especificado",
      "Substitui um elemento no índice",
      "Remove um elemento no índice"
    ],
    "answer": "Insere um elemento no índice especificado",
    "explanation": "O método `insert(index, value)` insere o `value` na lista no `index` fornecido, deslocando os elementos existentes para a direita."
  },
  {
    "question": "Qual método retorna o índice da primeira ocorrência de um valor em uma lista?",
    "options": [
      "get_index()",
      "search()",
      "index()",
      "find()"
    ],
    "answer": "index()",
    "explanation": "O método `index(value)` retorna o índice da primeira ocorrência do `value` na lista. Levanta um erro se o valor não for encontrado."
  },
  {
    "question": "Como você adiciona vários elementos de uma vez a uma lista?",
    "options": [
      "append() com uma lista",
      "extend() com uma lista",
      "insert() com uma lista",
      "update() com uma lista"
    ],
    "answer": "extend() com uma lista",
    "explanation": "O método `extend()` adiciona todos os elementos de um iterável (como outra lista) ao final da lista."
  },
  {
    "question": "O que o método `count(value)` faz em uma lista?",
    "options": [
      "Retorna o número de elementos na lista",
      "Retorna o número de ocorrências de um valor",
      "Retorna a soma dos elementos",
      "Retorna o índice de um valor"
    ],
    "answer": "Retorna o número de ocorrências de um valor",
    "explanation": "O método `count(value)` retorna o número de vezes que o `value` aparece na lista."
  },
  {
    "question": "Qual método remove a primeira ocorrência de um valor em uma lista?",
    "options": [
      "remove_at()",
      "delete()",
      "remove()",
      "pop()"
    ],
    "answer": "remove()",
    "explanation": "O método `remove(value)` remove a primeira ocorrência do `value` da lista. Levanta um erro se o valor não for encontrado."
  },
  {
    "question": "Qual destas opções NÃO é um tipo de dado de coleção embutido em Python?",
    "options": [
      "string",
      "list",
      "array",
      "dictionary"
    ],
    "answer": "array",
    "explanation": "Strings, listas e dicionários são coleções embutidas em Python. Arrays requerem o módulo `array` ou `numpy`."
  },
  {
    "question": "Como você cria um conjunto (set) vazio em Python?",
    "options": [
      "{}",
      "set()",
      "[]",
      "set.empty()"
    ],
    "answer": "set()",
    "explanation": "Para criar um conjunto vazio, você usa `set()`. `{}` cria um dicionário vazio."
  },
  {
    "question": "Qual operador é usado para verificar se dois valores NÃO são iguais?",
    "options": [
      "<>",
      "!=",
      "not ==",
      "is not"
    ],
    "answer": "!=",
    "explanation": "O operador `!=` é usado para verificar a desigualdade entre dois valores."
  },
  {
    "question": "O que o método `split()` faz em uma string?",
    "options": [
      "Junta uma lista de strings em uma única string",
      "Divide uma string em uma lista de substrings",
      "Remove caracteres específicos de uma string",
      "Converte uma string para minúsculas"
    ],
    "answer": "Divide uma string em uma lista de substrings",
    "explanation": "O método `split()` divide uma string em uma lista de substrings com base em um delimitador (por padrão, espaços em branco)."
  },
  {
    "question": "Qual é a saída de `print(\"Hello\" + \" \" + \"World\")`?",
    "options": [
      "HelloWorld",
      "Hello World",
      "Hello   world",
      "Erro"
    ],
    "answer": "Hello World",
    "explanation": "O operador `+` é usado para concatenar strings em Python."
  },
  {
    "question": "Como você define um comentário de múltiplas linhas em Python?",
    "options": [
      "// Comentário //",
      "/* Comentário */",
      "'''Comentário''' ou \"\"\"Comentário\"\"\"",
      "# Comentário #"
    ],
    "answer": "'''Comentário''' ou \"\"\"Comentário\"\"\"",
    "explanation": "Comentários de múltiplas linhas (docstrings) são criados usando três aspas simples ou duplas no início e no fim."
  },
  {
    "question": "Qual é o valor de `bool([])` (lista vazia)?",
    "options": [
      "True",
      "False",
      "None",
      "Erro"
    ],
    "answer": "False",
    "explanation": "Em Python, coleções vazias como listas, tuplas, dicionários e strings vazias são consideradas `False` em um contexto booleano."
  },
  {
    "question": "Qual função é usada para obter a entrada do usuário no console?",
    "options": [
      "get_input()",
      "read()",
      "input()",
      "console.read()"
    ],
    "answer": "input()",
    "explanation": "A função `input()` lê uma linha de texto do console e a retorna como uma string."
  },
  {
    "question": "O que o comando `pass` faz em Python?",
    "options": [
      "Termina o programa",
      "Pula a iteração atual de um loop",
      "É um placeholder, não faz nada",
      "Levanta uma exceção"
    ],
    "answer": "É um placeholder, não faz nada",
    "explanation": "A instrução `pass` é uma operação nula. Ela é usada quando uma instrução é sintaticamente necessária, mas nenhum código precisa ser executado."
  },
  {
    "question": "Qual é o resultado de `list(range(3))`?",
    "options": [
      "[0, 1, 2, 3]",
      "[1, 2, 3]",
      "[0, 1, 2]",
      "[1, 2]"
    ],
    "answer": "[0, 1, 2]",
    "explanation": "`range(3)` gera números de 0 a 2. `list()` converte o objeto range em uma lista."
  },
  {
    "question": "Como você verifica o tipo de uma variável `x`?",
    "options": [
      "typeof(x)",
      "x.type()",
      "type(x)",
      "isinstance(x)"
    ],
    "answer": "type(x)",
    "explanation": "A função `type()` retorna o tipo de um objeto. `isinstance()` também pode ser usado para verificar se um objeto é de um tipo específico."
  },
  {
    "question": "Qual é a principal diferença entre uma lista e uma tupla?",
    "options": [
      "Listas são ordenadas, tuplas não",
      "Listas são mutáveis, tuplas são imutáveis",
      "Listas só podem conter números, tuplas podem conter qualquer tipo",
      "Listas usam `[]`, tuplas usam `{}`"
    ],
    "answer": "Listas são mutáveis, tuplas são imutáveis",
    "explanation": "Listas podem ser modificadas após a criação (adicionar, remover, alterar elementos), enquanto tuplas não podem."
  },
  {
    "question": "O que o método `join()` faz com uma lista de strings?",
    "options": [
      "Divide uma string em uma lista",
      "Junta os elementos de uma lista de strings em uma única string usando um separador",
      "Remove elementos duplicados da lista",
      "Ordena a lista de strings"
    ],
    "answer": "Junta os elementos de uma lista de strings em uma única string usando um separador",
    "explanation": "Por exemplo, `' '.join(['a', 'b', 'c'])` retorna `'a b c'`."
  },
  {
    "question": "Qual é a saída de `print(f\"Valor: {10 / 3:.2f}\")`?",
    "options": [
      "Valor: 3.333",
      "Valor: 3.33",
      "Valor: 3.3",
      "Valor: 3"
    ],
    "answer": "Valor: 3.33",
    "explanation": "A f-string formata o resultado da divisão `10 / 3` para duas casas decimais (`.2f`)."
  },
  {
    "question": "Em um loop `for item in minha_lista:`, o que `item` representa?",
    "options": [
      "O índice do elemento atual",
      "O elemento atual da lista",
      "O comprimento da lista",
      "A lista inteira"
    ],
    "answer": "O elemento atual da lista",
    "explanation": "Em cada iteração do loop, `item` assume o valor do próximo elemento na `minha_lista`."
  },
  {
    "question": "Qual o resultado da expressão `5 > 3 and 10 < 20`?",
    "options": [
      "True",
      "False",
      "Erro",
      "None"
    ],
    "answer": "True",
    "explanation": "`5 > 3` é True, `10 < 20` é True. `True and True` resulta em `True`."
  },
  {
    "question": "Qual o resultado da expressão `not (5 > 10)`?",
    "options": [
      "True",
      "False",
      "Erro",
      "None"
    ],
    "answer": "True",
    "explanation": "`5 > 10` é False. `not False` resulta em `True`."
  },
  {
    "question": "O que o método `get(key, default)` faz em um dicionário?",
    "options": [
      "Remove a chave e retorna seu valor",
      "Retorna o valor associado à chave, ou `default` se a chave não existir",
      "Adiciona uma nova chave-valor ao dicionário",
      "Verifica se uma chave existe no dicionário"
    ],
    "answer": "Retorna o valor associado à chave, ou `default` se a chave não existir",
    "explanation": "Isso evita um `KeyError` se a chave não estiver presente no dicionário."
  },
  {
    "question": "Qual a forma correta de abrir um arquivo chamado `dados.txt` para leitura em Python?",
    "options": [
      "file = open(\"dados.txt\", \"r\")",
      "file = read(\"dados.txt\")",
      "file.open(\"dados.txt\", \"read\")",
      "open(\"dados.txt\", mode=\"read\")"
    ],
    "answer": "file = open(\"dados.txt\", \"r\")",
    "explanation": "A função `open()` é usada para abrir arquivos. O modo `'r'` especifica leitura."
  },
  {
    "question": "Qual método é usado para fechar um arquivo aberto em Python?",
    "options": [
      "file.end()",
      "file.close()",
      "file.exit()",
      "close(file)"
    ],
    "answer": "file.close()",
    "explanation": "É importante fechar arquivos após o uso para liberar recursos e garantir que os dados sejam gravados corretamente."
  },
  {
    "question": "O que a instrução `with open(...) as f:` garante?",
    "options": [
      "Que o arquivo será aberto apenas para escrita",
      "Que o arquivo será fechado automaticamente, mesmo se ocorrerem erros",
      "Que o arquivo será lido linha por linha",
      "Que o arquivo será criado se não existir"
    ],
    "answer": "Que o arquivo será fechado automaticamente, mesmo se ocorrerem erros",
    "explanation": "O gerenciador de contexto `with` garante que o método `__exit__` do objeto arquivo (que inclui `close()`) seja chamado."
  },
  {
    "question": "Qual é o valor de `x` após o código: \n```python\nx = 1; x = x + 1.0\n```\n?",
    "options": [
      "1",
      "2",
      "1.0",
      "2.0"
    ],
    "answer": "2.0",
    "explanation": "Quando um inteiro é somado a um float, o resultado é um float para manter a precisão."
  },
  {
    "question": "Qual dos seguintes é um operador de atribuição composto?",
    "options": [
      "=",
      "==",
      "+=",
      "=>"
    ],
    "answer": "+=",
    "explanation": "Operadores de atribuição compostos como `+=`, `-=`, `*=`, `/=` combinam uma operação aritmética com atribuição."
  },
  {
    "question": "O que a função `chr(65)` retorna?",
    "options": [
      "\"65\"",
      "\"A\"",
      "65",
      "Erro"
    ],
    "answer": "\"A\"",
    "explanation": "A função `chr()` retorna o caractere correspondente a um código Unicode. 65 é o código Unicode para 'A'."
  },
  {
    "question": "O que a função `ord('B')` retorna?",
    "options": [
      "\"B\"",
      "66",
      "2",
      "Erro"
    ],
    "answer": "66",
    "explanation": "A função `ord()` retorna o código Unicode de um caractere. 'B' tem o código Unicode 66."
  },
  {
    "question": "Qual é a forma correta de definir um valor padrão para um parâmetro de função como em `def func(a, b=10):`?",
    "options": [
      "`def func(a, b==10):`",
      "`def func(a, b is 10):`",
      "`def func(a, b=10):`",
      "`def func(a, b:10):`"
    ],
    "answer": "`def func(a, b=10):`",
    "explanation": "Valores padrão para parâmetros são definidos usando `=` na assinatura da função."
  },
  {
    "question": "Se uma função não possui uma instrução `return` explícita, o que ela retorna por padrão?",
    "options": [
      "0",
      "None",
      "True",
      "Erro"
    ],
    "answer": "None",
    "explanation": "Se uma função Python não retorna um valor explicitamente, ela retorna `None` implicitamente."
  },
  {
    "question": "Qual o escopo de uma variável definida dentro de uma função?",
    "options": [
      "Global",
      "Local para a função",
      "Local para o módulo",
      "Persistente entre chamadas de função"
    ],
    "answer": "Local para a função",
    "explanation": "Variáveis definidas dentro de uma função são locais e só existem durante a execução daquela função, a menos que declaradas como `global` ou `nonlocal`."
  },
  {
    "question": "O que o método `isdigit()` verifica em uma string?",
    "options": [
      "Se a string contém apenas letras",
      "Se a string contém apenas dígitos numéricos",
      "Se a string está vazia",
      "Se a string contém apenas espaços"
    ],
    "answer": "Se a string contém apenas dígitos numéricos",
    "explanation": "Retorna `True` se todos os caracteres na string são dígitos e há pelo menos um caractere, `False` caso contrário."
  },
  {
    "question": "Qual o resultado de `\"Python\".find(\"th\")`?",
    "options": [
      "2",
      "3",
      "-1",
      "True"
    ],
    "answer": "2",
    "explanation": "O método `find()` retorna o índice da primeira ocorrência da substring. Se não encontrada, retorna -1. 'th' começa no índice 2."
  },
  {
    "question": "Qual o resultado de `\"Python\".replace(\"P\", \"J\")`?",
    "options": [
      "\"Jython\"",
      "\"python\"",
      "\"PJython\"",
      "Erro"
    ],
    "answer": "\"Jython\"",
    "explanation": "O método `replace()` retorna uma nova string com todas as ocorrências de uma substring substituídas por outra."
  },
  {
    "question": "Qual das seguintes opções cria uma tupla com um único elemento?",
    "options": [
      "(1)",
      "[1,]",
      "{1}",
      "(1,)"
    ],
    "answer": "(1,)",
    "explanation": "Para criar uma tupla de um único elemento, é necessário usar uma vírgula após o elemento, como em `(1,)`. `(1)` é apenas o inteiro 1 entre parênteses."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\nprint(\"Olá, Mundo!\")\n```\n",
    "options": [
      "a) Olá, Mundo!",
      "b) \"Olá, Mundo!\"",
      "c) print(\"Olá, Mundo!\")",
      "d) Erro"
    ],
    "answer": "a) Olá, Mundo!",
    "explanation": "A função `print()` exibe o conteúdo da string que lhe é passada como argumento."
  },
  {
    "question": "Qual das seguintes opções é um nome de variável Python válido?",
    "options": [
      "a) 1nome",
      "b) nome-completo",
      "c) _nome",
      "d) nome completo"
    ],
    "answer": "c) _nome",
    "explanation": "Nomes de variáveis em Python devem começar com uma letra ou um sublinhado (`_`). Não podem começar com números nem conter espaços ou hífens."
  },
  {
    "question": "Qual é o tipo de dado de `5` em Python?",
    "options": [
      "a) float",
      "b) str",
      "c) int",
      "d) bool"
    ],
    "answer": "c) int",
    "explanation": "`5` é um número inteiro, e em Python, números inteiros são do tipo `int`."
  },
  {
    "question": "Qual operador é usado para exponenciação em Python?",
    "options": [
      "a) ^",
      "b) **",
      "c) //",
      "d) %"
    ],
    "answer": "b) **",
    "explanation": "O operador `**` é usado para exponenciação em Python (e.g., `2 ** 3` resulta em 8)."
  },
  {
    "question": "Qual é a saída de `type(3.14)`?",
    "options": [
      "a) <class 'int'>",
      "b) <class 'float'>",
      "c) <class 'str'>",
      "d) <class 'class'>"
    ],
    "answer": "b) <class 'float'>",
    "explanation": "`3.14` é um número de ponto flutuante, e a função `type()` retorna o tipo da variável, que neste caso é `float`."
  },
  {
    "question": "Qual das seguintes opções é uma forma correta de comentar uma única linha em Python?",
    "options": [
      "a) // Este é um comentário",
      "b) # Este é um comentário",
      "c) /* Este é um comentário */",
      "d) ``"
    ],
    "answer": "b) # Este é um comentário",
    "explanation": "Em Python, o caractere `#` é usado para iniciar um comentário de linha única. Todo o texto após o `#` na mesma linha é ignorado pelo interpretador."
  },
  {
    "question": "O que o operador `//` faz em Python?",
    "options": [
      "a) Divisão de ponto flutuante",
      "b) Divisão inteira (floor division)",
      "c) Módulo",
      "d) Exponenciação"
    ],
    "answer": "b) Divisão inteira (floor division)",
    "explanation": "O operador `//` realiza a divisão inteira (floor division), arredondando o resultado para o número inteiro mais próximo para baixo."
  },
  {
    "question": "Qual é o valor de `x` após a execução do código: `x = 10 % 3`?",
    "options": [
      "a) 3",
      "b) 1",
      "c) 0",
      "d) 3.33"
    ],
    "answer": "b) 1",
    "explanation": "O operador `%` (módulo) retorna o resto da divisão. 10 dividido por 3 é 3 com resto 1."
  },
  {
    "question": "Qual é a função usada para obter entrada do usuário em Python?",
    "options": [
      "a) get_input()",
      "b) read()",
      "c) input()",
      "d) user_input()"
    ],
    "answer": "c) input()",
    "explanation": "A função `input()` é a maneira padrão de obter entrada de texto do usuário no console em Python."
  },
  {
    "question": "Qual é a saída de `print(2 + 3 * 4)`?",
    "options": [
      "a) 20",
      "b) 14",
      "c) 24",
      "d) 9"
    ],
    "answer": "b) 14",
    "explanation": "De acordo com a ordem das operações (PEMDAS/BODMAS), a multiplicação é realizada antes da adição. Então, `3 * 4` é 12, e `2 + 12` é 14."
  },
  {
    "question": "Qual palavra-chave é usada para iniciar uma instrução condicional em Python?",
    "options": [
      "a) condition",
      "b) if",
      "c) when",
      "d) check"
    ],
    "answer": "b) if",
    "explanation": "A palavra-chave `if` é usada para iniciar uma instrução condicional em Python, seguida por uma condição a ser avaliada."
  },
  {
    "question": "O que o seguinte código irá imprimir?\n```python\nx = 10\nif x > 5:\n    print(\"Maior\")\nelse:\n    print(\"Menor ou Igual\")\n```\n",
    "options": [
      "a) Maior",
      "b) Menor ou Igual",
      "c) Erro",
      "d) Nada"
    ],
    "answer": "a) Maior",
    "explanation": "Como o valor de `x` (10) é maior que 5, a condição `x > 5` é verdadeira, e o bloco de código dentro do `if` é executado."
  },
  {
    "question": "Qual das seguintes opções é uma forma correta de escrever um laço `for` que itera de 0 a 4 (inclusive)?",
    "options": [
      "a) for i in range(5):",
      "b) for i in range(0, 4):",
      "c) for i in range(1, 5):",
      "d) for i in 0 to 4:"
    ],
    "answer": "a) for i in range(5):",
    "explanation": "A função `range(n)` gera uma sequência de números de 0 até `n-1`. Portanto, `range(5)` gera 0, 1, 2, 3, 4."
  },
  {
    "question": "O que o laço `while` faz?",
    "options": [
      "a) Executa um bloco de código um número fixo de vezes.",
      "b) Executa um bloco de código enquanto uma condição é verdadeira.",
      "c) Executa um bloco de código apenas uma vez.",
      "d) Para a execução do programa."
    ],
    "answer": "b) Executa um bloco de código enquanto uma condição é verdadeira.",
    "explanation": "Um laço `while` continua executando seu bloco de código repetidamente enquanto a condição especificada for avaliada como verdadeira."
  },
  {
    "question": "Qual palavra-chave é usada para sair de um laço prematuramente?",
    "options": [
      "a) skip",
      "b) continue",
      "c) break",
      "d) exit"
    ],
    "answer": "c) break",
    "explanation": "A palavra-chave `break` é usada para sair imediatamente do laço mais interno em que ela está, retomando a execução do código após o laço."
  },
  {
    "question": "O que o seguinte código irá imprimir?\n```python\nfor i in range(3):\n    if i == 1:\n        continue\n    print(i)\n```\n",
    "options": [
      "a) 0, 1, 2",
      "b) 0, 2",
      "c) 1, 2",
      "d) 0"
    ],
    "answer": "b) 0, 2",
    "explanation": "Quando `i` é igual a 1, a instrução `continue` é executada, o que faz com que a iteração atual seja pulada, e o `print(i)` não seja executado para `i = 1`."
  },
  {
    "question": "O que acontece se a condição de um laço `while` nunca se torna falsa?",
    "options": [
      "a) O laço é ignorado.",
      "b) O programa entra em um laço infinito.",
      "c) O programa lança um erro.",
      "d) O laço executa apenas uma vez."
    ],
    "answer": "b) O programa entra em um laço infinito.",
    "explanation": "Se a condição de um laço `while` permanece sempre verdadeira, o laço nunca termina, levando a um laço infinito que consome recursos e impede o programa de avançar."
  },
  {
    "question": "Qual das seguintes opções não é um operador de comparação em Python?",
    "options": [
      "a) ==",
      "b) !=",
      "c) =",
      "d) >="
    ],
    "answer": "c) =",
    "explanation": "`=` é o operador de atribuição, usado para atribuir um valor a uma variável. `==`, `!=`, e `>=` são operadores de comparação."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ni = 0\nwhile i < 3:\n    print(i)\n    i += 1\n```\n",
    "options": [
      "a) 0, 1, 2, 3",
      "b) 0, 1, 2",
      "c) 1, 2, 3",
      "d) Nada"
    ],
    "answer": "b) 0, 1, 2",
    "explanation": "O laço `while` executa enquanto `i` for menor que 3. Em cada iteração, `i` é impresso e depois incrementado, resultando em 0, 1 e 2."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\nx = 5\nif x > 10:\n    print(\"A\")\nelif x > 5:\n    print(\"B\")\nelse:\n    print(\"C\")\n```\n",
    "options": [
      "a) A",
      "b) B",
      "c) C",
      "d) Erro"
    ],
    "answer": "c) C",
    "explanation": "A primeira condição `x > 10` (5 > 10) é falsa. A segunda condição `x > 5` (5 > 5) também é falsa. Portanto, o bloco `else` é executado."
  },
  {
    "question": "Qual palavra-chave é usada para definir uma função em Python?",
    "options": [
      "a) func",
      "b) define",
      "c) def",
      "d) function"
    ],
    "answer": "c) def",
    "explanation": "A palavra-chave `def` é usada em Python para definir uma nova função."
  },
  {
    "question": "O que a palavra-chave `return` faz em uma função?",
    "options": [
      "a) Exibe a saída da função.",
      "b) Termina a execução da função e, opcionalmente, retorna um valor.",
      "c) Redefine a função.",
      "d) Chama a função novamente."
    ],
    "answer": "b) Termina a execução da função e, opcionalmente, retorna um valor.",
    "explanation": "A instrução `return` encerra a execução de uma função e pode enviar um valor de volta para o chamador da função."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ndef saudacao(nome):\n    print(\"Olá, \" + nome + \"!\")\nsaudacao(\"Alice\")\n```\n",
    "options": [
      "a) Olá, Alice!",
      "b) saudacao(\"Alice\")",
      "c) Erro",
      "d) Nada"
    ],
    "answer": "a) Olá, Alice!",
    "explanation": "A função `saudacao` é definida para imprimir uma saudação com o nome fornecido. Quando chamada com \"Alice\", ela imprime \"Olá, Alice!\"."
  },
  {
    "question": "Uma função que não tem uma instrução `return` explicitamente retorna qual valor por padrão?",
    "options": [
      "a) 0",
      "b) None",
      "c) Uma string vazia",
      "d) False"
    ],
    "answer": "b) None",
    "explanation": "Se uma função Python não possui uma instrução `return` explícita, ela retorna `None` por padrão."
  },
  {
    "question": "Qual das seguintes opções é uma forma correta de chamar uma função chamada `calcular_soma` que aceita dois argumentos `a` e `b`?",
    "options": [
      "a) call calcular_soma(5, 10)",
      "b) calcular_soma 5, 10",
      "c) calcular_soma(5, 10)",
      "d) run calcular_soma(5, 10)"
    ],
    "answer": "c) calcular_soma(5, 10)",
    "explanation": "Para chamar uma função em Python, você usa o nome da função seguido por parênteses que contêm os argumentos, se houver."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ndef dobro(x):\n    return x * 2\nresultado = dobro(5)\nprint(resultado)\n```\n",
    "options": [
      "a) dobro(5)",
      "b) 10",
      "c) 5 * 2",
      "d) Erro"
    ],
    "answer": "b) 10",
    "explanation": "A função `dobro` retorna o dobro do valor de `x`. Quando `dobro(5)` é chamada, ela retorna 10, que é então impresso."
  },
  {
    "question": "O que são os parâmetros de uma função?",
    "options": [
      "a) Os valores que a função retorna.",
      "b) As variáveis listadas dentro dos parênteses na definição da função.",
      "c) As variáveis definidas dentro do corpo da função.",
      "d) O nome da função."
    ],
    "answer": "b) As variáveis listadas dentro dos parênteses na definição da função.",
    "explanation": "Parâmetros são nomes de variáveis placeholders na definição da função que recebem os valores (argumentos) passados quando a função é chamada."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ndef soma(a, b):\n    print(a + b)\nsoma(10, 20)\n```\n",
    "options": [
      "a) 30",
      "b) None",
      "c) 10 20",
      "d) Erro"
    ],
    "answer": "a) 30",
    "explanation": "A função `soma` imprime a soma de seus dois argumentos. Quando chamada com 10 e 20, ela imprime 30."
  },
  {
    "question": "O que acontece se você tentar chamar uma função com um número incorreto de argumentos?",
    "options": [
      "a) O Python irá ajustar automaticamente os argumentos.",
      "b) O programa entrará em um laço infinito.",
      "c) O Python levantará um TypeError.",
      "d) A função irá ignorar os argumentos extras ou faltantes."
    ],
    "answer": "c) O Python levantará um TypeError.",
    "explanation": "Python é rigoroso quanto ao número de argumentos esperados por uma função. Chamar uma função com mais ou menos argumentos do que o esperado resultará em um `TypeError`."
  },
  {
    "question": "Qual das seguintes opções descreve melhor o escopo de uma variável definida dentro de uma função?",
    "options": [
      "a) Escopo global (acessível em qualquer lugar do programa).",
      "b) Escopo local (acessível apenas dentro da função).",
      "c) Escopo de módulo (acessível apenas dentro do arquivo).",
      "d) Escopo de classe (acessível apenas dentro de classes)."
    ],
    "answer": "b) Escopo local (acessível apenas dentro da função).",
    "explanation": "Variáveis definidas dentro de uma função têm escopo local, o que significa que elas só são acessíveis dentro dessa função e não podem ser referenciadas de fora dela."
  },
  {
    "question": "Qual das seguintes opções é uma lista vazia em Python?",
    "options": [
      "a) {}",
      "b) ()",
      "c) []",
      "d) set()"
    ],
    "answer": "c) []",
    "explanation": "Listas em Python são definidas por colchetes. `[]` representa uma lista vazia."
  },
  {
    "question": "Qual é o índice do primeiro elemento em uma lista Python?",
    "options": [
      "a) 1",
      "b) 0",
      "c) -1",
      "d) Varia dependendo do tamanho da lista"
    ],
    "answer": "b) 0",
    "explanation": "A indexação em Python (e em muitas outras linguagens de programação) começa em 0 para o primeiro elemento."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\nlista = [10, 20, 30]\nprint(lista[1])\n```\n",
    "options": [
      "a) 10",
      "b) 20",
      "c) 30",
      "d) Erro"
    ],
    "answer": "b) 20",
    "explanation": "O acesso `lista[1]` retorna o elemento no índice 1 da lista, que é 20 (contando a partir de 0)."
  },
  {
    "question": "Qual método é usado para adicionar um item ao final de uma lista?",
    "options": [
      "a) add()",
      "b) insert()",
      "c) append()",
      "d) push()"
    ],
    "answer": "c) append()",
    "explanation": "O método `append()` é usado para adicionar um único item ao final de uma lista existente."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ntupla = (1, 2, 3)\n# tupla[0] = 10 # Esta linha causaria um erro\nprint(tupla)\n```\n",
    "options": [
      "a) (10, 2, 3)",
      "b) (1, 2, 3, 10)",
      "c) Erro",
      "d) (1, 2, 3)"
    ],
    "answer": "c) Erro",
    "explanation": "Tuplas em Python são imutáveis, o que significa que seus elementos não podem ser alterados, adicionados ou removidos após a criação. Tentar modificá-las resultará em um `TypeError`."
  },
  {
    "question": "Qual das seguintes opções é uma característica das tuplas?",
    "options": [
      "a) Mutáveis",
      "b) Heterogêneas",
      "c) Imutáveis",
      "d) Não ordenadas"
    ],
    "answer": "c) Imutáveis",
    "explanation": "A principal característica das tuplas é que elas são imutáveis; uma vez criadas, seus elementos não podem ser modificados."
  },
  {
    "question": "Qual das seguintes opções é uma forma correta de criar um dicionário vazio em Python?",
    "options": [
      "a) dict_vazio = []",
      "b) dict_vazio = ()",
      "c) dict_vazio = {}",
      "d) dict_vazio = new dict()"
    ],
    "answer": "c) dict_vazio = {}",
    "explanation": "Dicionários em Python são definidos por chaves. `{}` representa um dicionário vazio."
  },
  {
    "question": "Como você acessa o valor associado à chave \"idade\" em um dicionário chamado `pessoa`?",
    "options": [
      "a) pessoa.idade",
      "b) pessoa[idade]",
      "c) pessoa[\"idade\"]",
      "d) get_value(pessoa, \"idade\")"
    ],
    "answer": "c) pessoa[\"idade\"]",
    "explanation": "Valores em dicionários Python são acessados usando a chave correspondente entre colchetes, como em `dicionario[chave]`."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ndicionario = {\"nome\": \"Maria\", \"idade\": 30}\nprint(dicionario[\"nome\"])\n```\n",
    "options": [
      "a) Maria",
      "b) nome",
      "c) {\"nome\": \"Maria\", \"idade\": 30}",
      "d) Erro"
    ],
    "answer": "a) Maria",
    "explanation": "O código acessa o valor associado à chave \"nome\" no dicionário `dicionario`, que é \"Maria\"."
  },
  {
    "question": "Qual das seguintes opções é um conjunto (set) vazio em Python?",
    "options": [
      "a) {}",
      "b) set()",
      "c) []",
      "d) ()"
    ],
    "answer": "b) set()",
    "explanation": "Embora `{}` crie um dicionário vazio, para criar um conjunto vazio, você deve usar a função `set()` explicitamente."
  },
  {
    "question": "Qual palavra-chave é usada para importar um módulo em Python?",
    "options": [
      "a) use",
      "b) load",
      "c) import",
      "d) include"
    ],
    "answer": "c) import",
    "explanation": "A palavra-chave `import` é usada para carregar módulos e seus conteúdos em um script Python."
  },
  {
    "question": "Qual módulo Python é comumente usado para operações matemáticas avançadas, como funções trigonométricas?",
    "options": [
      "a) random",
      "b) os",
      "c) math",
      "d) sys"
    ],
    "answer": "c) math",
    "explanation": "O módulo `math` fornece acesso a funções e constantes matemáticas para operações mais complexas."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\nimport random\nprint(random.randint(1, 1))\n```\n",
    "options": [
      "a) Um número aleatório entre 1 e 100.",
      "b) 1",
      "c) Erro",
      "d) Um número aleatório entre 0 e 1."
    ],
    "answer": "b) 1",
    "explanation": "A função `random.randint(a, b)` retorna um número inteiro aleatório `N` tal que `a <= N <= b`. Como ambos `a` e `b` são 1, o único resultado possível é 1."
  },
  {
    "question": "O que é uma exceção em Python?",
    "options": [
      "a) Um erro de sintaxe.",
      "b) Um evento que interrompe o fluxo normal de um programa.",
      "c) Um aviso que pode ser ignorado.",
      "d) Um comentário especial."
    ],
    "answer": "b) Um evento que interrompe o fluxo normal de um programa.",
    "explanation": "Uma exceção é um evento que ocorre durante a execução de um programa e que interrompe o fluxo normal das instruções. Elas podem ser capturadas e tratadas."
  },
  {
    "question": "Qual bloco de código é usado para lidar com exceções em Python?",
    "options": [
      "a) try/catch",
      "b) do/except",
      "c) try/except",
      "d) handle/error"
    ],
    "answer": "c) try/except",
    "explanation": "O bloco `try/except` é o mecanismo padrão em Python para lidar com exceções. O código que pode levantar uma exceção é colocado no bloco `try`, e o tratamento da exceção é colocado no bloco `except`."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ntry:\n    print(1 / 0)\nexcept ZeroDivisionError:\n    print(\"Divisão por zero!\")\n```\n",
    "options": [
      "a) Erro",
      "b) Divisão por zero!",
      "c) 0",
      "d) Nada"
    ],
    "answer": "b) Divisão por zero!",
    "explanation": "A operação `1 / 0` causa uma `ZeroDivisionError`. Esta exceção é capturada pelo bloco `except ZeroDivisionError`, e a mensagem \"Divisão por zero!\" é impressa."
  },
  {
    "question": "Qual método de string é usado para converter todos os caracteres de uma string para letras maiúsculas?",
    "options": [
      "a) lower()",
      "b) capitalize()",
      "c) upper()",
      "d) title()"
    ],
    "answer": "c) upper()",
    "explanation": "O método `upper()` retorna uma nova string onde todos os caracteres da string original foram convertidos para maiúsculas."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\ns = \"Python\"\nprint(s[1:4])\n```\n",
    "options": [
      "a) Pyth",
      "b) yth",
      "c) ytho",
      "d) Pytho"
    ],
    "answer": "b) yth",
    "explanation": "O fatiamento `s[1:4]` inclui o caractere no índice 1 (que é 'y') até (mas não incluindo) o caractere no índice 4 (que é 'o'). Portanto, ele retorna 'yth'."
  },
  {
    "question": "Qual das seguintes opções é verdadeira sobre strings em Python?",
    "options": [
      "a) São mutáveis.",
      "b) São sequências de caracteres imutáveis.",
      "c) São um tipo de dado numérico.",
      "d) Podem ser modificadas diretamente após a criação."
    ],
    "answer": "b) São sequências de caracteres imutáveis.",
    "explanation": "Strings em Python são imutáveis, o que significa que, uma vez criadas, seu conteúdo não pode ser alterado. Qualquer operação que 'modifique' uma string na verdade retorna uma nova string."
  },
  {
    "question": "Qual é a saída do seguinte código?\n```python\nmensagem = \"Olá\" + \" \" + \"Mundo\"\nprint(mensagem)\n```\n",
    "options": [
      "a) Olá Mundo",
      "b) Olá mundo",
      "c) Olá  Mundo",
      "d) Erro"
    ],
    "answer": "a) Olá Mundo",
    "explanation": "O operador `+` é usado para concatenar strings em Python. As três strings são combinadas para formar \"Olá Mundo\"."
  }
]

# --- Configuracoes da aplicacao ---
st.set_page_config(
    page_title="Simulado Interativo PCEP",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="auto"
)

# --- Definição das cores do tema ---
primary_color = "#347AB6"
secondary_color = "#79A6DC"
background_color = "#F0F8FF"
text_color = "#333333"

# --- CSS para o tema azul ---
custom_css = f"""
<style>
    /* ----------------------------- TIPOGRAFIA ----------------------------- */
    section.main h1, .block-container h1 {{
        font-size: 2.2em;
    }}
    section.main h2, .block-container h2 {{
        font-size: 1.6em;
    }}
    section.main h3, .block-container h3 {{
        font-size: 1.3em;
    }}

    /* ----------------------------- BOTÕES ----------------------------- */
    .stButton>button {{
        background-color: {primary_color};
        color: white;
        border-radius: 10px; /* Aumentado para um look mais rebuscado */
        border: none;
        padding: 12px 24px; /* Padding maior para destaque */
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); /* Sombra sutil */
        transition: all 0.3s ease; /* Transição suave */
        font-size: 1em;
    }}

    .stButton>button:hover {{
        background-color: {secondary_color};
        transform: translateY(-2px); /* Efeito de elevação */
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }}
    .stButton>button:active {{
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }}

    .stButton>button[kind="secondary"], 
    .stButton>button[kind="secondary"]:focus {{
        background-color: #D3D3D3;
        color: #333333;
    }}
    .stButton>button[kind="secondary"]:hover {{
        background-color: #BEBEBE;
        color: #333333;
    }}

    /* Tema Dark */
    .st-emotion-cache-13k62yr .stButton>button,
    body[color-scheme="dark"] .stButton>button {{
        background-color: #4A90E2; /* Tom mais escuro de azul para contraste */
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }}
    .st-emotion-cache-13k62yr .stButton>button:hover,
    body[color-scheme="dark"] .stButton>button:hover {{
        background-color: #63A4FF;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4);
    }}
    .st-emotion-cache-13k62yr .stButton>button[kind="secondary"],
    body[color-scheme="dark"] .stButton>button[kind="secondary"]:focus {{
        background-color: #555555;
        color: #E0E0E0;
    }}
    .st-emotion-cache-13k62yr .stButton>button[kind="secondary"]:hover,
    body[color-scheme="dark"] .stButton>button[kind="secondary"]:hover {{
        background-color: #6E6E6E;
        color: #E0E0E0;
    }}

    .stButton {{
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }}
    /* Alinha os botões quando aparecem juntos */
    .stButton + .stButton {{
    margin-top: 0 !important;
    }}

    /* ----------------------------- FORMULÁRIO DE CADASTRO ----------------------------- */
    div[data-testid="stForm"] {{
        border: 1px solid {secondary_color};
        border-radius: 10px;
        padding: 1rem 1rem 0.5rem 1rem;
    }}
    body[data-theme="dark"] div[data-testid="stForm"] {{
        border-color: #4A5464 !important;
    }}

    /* ----------------------------- DATAFRAME (RANKING) ----------------------------- */
    /* Cor de fundo da linha ao passar o mouse (hover) */
    div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover {{
        background-color: #E7F1FF !important;
    }}
    /* Cor do texto da linha ao passar o mouse (hover) */
    div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover .glide-cell {{
        color: #000000 !important;
    }}
    /* Tema Dark para o DataFrame */
    body[data-theme="dark"] div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover {{
        background-color: #2C3440 !important;
    }}
    body[data-theme="dark"] div[data-testid="stDataFrame"] .glide-table-body .glide-row:hover .glide-cell {{
        color: #FAFAFA !important;
    }}

    /* ----------------------------- RADIO ----------------------------- */
    .stRadio > label p {{
        font-size: 1.05em !important;
    }}
    body[data-theme="dark"] .stRadio > label p,
    body.dark .stRadio > label p {{
        color: #FAFAFA !important;
    }}
    body[data-theme="light"] .stRadio > label p,
    body.light .stRadio > label p {{
        color: #333333 !important;
    }}
    div[data-baseweb="radio"] > label {{
    margin-bottom: 6px !important;
    }}

    /* ----------------------------- TEXTOS DAS QUESTÕES ----------------------------- */
    .quiz-question-text {{
        font-size: 1.2em;
        color: inherit;
        margin-bottom: 10px !important; 
        line-height: 1.1;
    }}
    body[data-theme="dark"] .quiz-question-text, 
    body.dark .quiz-question-text,
    body[data-theme="dark"] .quiz-question-text strong, 
    body.dark .quiz-question-text strong {{
        color: #FAFAFA !important; 
    }}

    /* ----------------------------- CAIXA DE EXPLICAÇÃO ----------------------------- */
    .explanation-box {{
        border: 1px solid {secondary_color};
        background-color: #E7F1FF;
        padding: 15px;
        border-radius: 5px;
        margin-top: 10px !important';
        line-height: 1.6;
        color: {text_color};
    }}
    body[data-theme="dark"] .explanation-box,
    body.dark .explanation-box {{
        background-color: #2C3440 !important;
        border-color: #4A5464 !important;
        color: #FAFAFA !important;
    }}

    /* ----------------------------- RESULTADO ----------------------------- */
    .score-display {{
        font-size: 1.5em;
        font-weight: bold;
        color: {primary_color};
        text-align: center;
        margin-top: 10px !important;
    }}

    .timer-display {{
        font-size: 1.1em;
        font-weight: bold;
        color: {primary_color};
        padding: 10px;
        border: 1px solid {secondary_color};
        border-radius: 5px;
        background-color: #E7F1FF;
        text-align: center;
    }}

    /* ----------------------------- BLOCOS DE CÓDIGO ----------------------------- */
    .quiz-question-text pre,
    .explanation-box pre {{
        background-color: #282c34 !important;
        color: #abb2bf !important;
        padding: 0.6em !important;
        margin: 0.5em !important;
        border-radius: 5px !important;
        overflow-x: auto !important;
        white-space: pre !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, Courier, monospace !important;
        font-size: 0.95em !important;
        line-height: 1.6 !important;
        border: 1px solid #3e4451;
    }}

    .quiz-question-text pre code,
    .explanation-box pre code {{
        display: block !important;
        padding: 0 !important;
        margin: 0 !important;
        white-space: pre !important;
        border: none !important;
    }}

    .quiz-question-text p > code,
    .quiz-question-text li > code,
    .explanation-box p > code,
    .explanation-box li > code {{
        padding: 0.1em 0.4em !important;
        margin: 0 0.2em !important;
        display: inline-block !important;
        white-space: pre-wrap !important;
        vertical-align: baseline !important;
    }}

    /* ----------------------------- SYNTAX HIGHLIGHTING ----------------------------- */
    .quiz-question-text pre .c1, .explanation-box pre .c1,
    .quiz-question-text pre .cm, .explanation-box pre .cm {{
        color: #5c6370 !important; font-style: italic !important;
    }}
    .quiz-question-text pre .k, .explanation-box pre .k,
    .quiz-question-text pre .kn, .explanation-box pre .kn {{
        color: #c678dd !important;
    }}
    .quiz-question-text pre .nb, .explanation-box pre .nb,
    .quiz-question-text pre .nc, .explanation-box pre .nc {{
        color: #e5c07b !important;
    }}
    .quiz-question-text pre .nf, .explanation-box pre .nf {{
        color: #61afef !important;
    }}
    .quiz-question-text pre .s1, .explanation-box pre .s1,
    .quiz-question-text pre .s2, .explanation-box pre .s2 {{
        color: #98c379 !important;
    }}
    .quiz-question-text pre .mi, .explanation-box pre .mi,
    .quiz-question-text pre .mf, .explanation-box pre .mf {{
        color: #d19a66 !important;
    }}
    .quiz-question-text pre .bp, .explanation-box pre .bp,
    .quiz-question-text pre .o, .explanation-box pre .o {{
        color: #56b6c2 !important;
    }}
    .quiz-question-text pre .p, .explanation-box pre .p,
    .quiz-question-text pre .n, .explanation-box pre .n {{
        color: #abb2bf !important;
    }}

    /* ----------------------------- RODAPÉ ----------------------------- */
    .rodape-container {{
        position: static;
        width: 100%;
        margin-top: 2rem;
        padding: 0;
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
    }}
    body[data-theme="dark"] .rodape-container,
    body.st-dark .rodape-container {{
        background-color: #1a1c23 !important;
        border: 1px solid #33353b !important;
    }}

    /* Forçar herança do tema dark do contêiner pai */
    .st-emotion-cache-13k62yr .rodape-container,
    body[color-scheme="dark"] .rodape-container,
    body[data-theme="dark"] .rodape-container,
    body.dark .rodape-container,
    body.st-dark .rodape-container {{
        background-color: #1a1c23 !important;
        border: 1px solid #33353b !important;
    }}
    .st-emotion-cache-13k62yr .rodape-container *,
    body[color-scheme="dark"] .rodape-container *,
    body[data-theme="dark"] .rodape-container *,
    body.dark .rodape-container *,
    body.st-dark .rodape-container * {{
        background-color: #1a1c23 !important;
    }}
    .rodape {{
        margin: 0 auto;
        max-width: 900px;
        text-align: center;
        font-size: 0.7em;
        padding: 10px 1.5rem;
        color: #333333;
        box-sizing: border-box;
    }}
    body[data-theme="dark"] .rodape,
    body.st-dark .rodape {{
        background-color: transparent !important;
        color: #FAFAFA !important;
    }}
    .st-emotion-cache-13k62yr .rodape,
    body[color-scheme="dark"] .rodape,
    body[data-theme="dark"] .rodape,
    body.dark .rodape,
    body.st-dark .rodape {{
        color: #abb2bf !important;
    }}
    .rodape .linha {{
        margin: 5px 0;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
    }}
    .rodape .links {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 5px;
    }}
    .rodape .links a {{
        text-decoration: none;
        transition: transform 0.3s ease;
    }}
    .rodape .links a:hover {{
        transform: scale(1.1);
    }}
    @media (max-width: 768px) {{
        .rodape-container {{
            margin-top: 2rem;
        }}
        section.main h1, .block-container h1 {{
            font-size: 1.2em !important;
        }}
        .main h2 {{
            font-size: 1.2em !important;
        }}
        .main h3 {{
            font-size: 1em !important;
        }}
        .rodape {{
            font-size: 0.75em;
        }}
        .rodape .links {{
            flex-direction: row;  /* mantém horizontal no mobile */
        }}
        /* Remove espaçamento excessivo entre os botões */
        .st-emotion-cache-ocqkz7 {{
        margin-top: 0 !important;
        gap: 0.2rem !important; /* ou 0.2rem se quiser ainda mais próximo */
        }}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# --- Aqui ficam as variáveis globais do SIMULADO como numeros de perguntas, limite de tempo e porcetagem de aprovado ---
NUM_QUESTIONS_PER_QUIZ = 30
QUIZ_TIME_LIMIT_MINUTES = 45
PASSING_PERCENTAGE = 70

RANKING_FILE = 'ranking.json'

# --- Funções ---
def initialize_quiz_session():
    # Garante uma nova semente aleatória a cada inicialização para máxima variedade das perguntas
    random.seed(time.time_ns())

    if len(questions_data) >= NUM_QUESTIONS_PER_QUIZ:
        selected_questions = random.sample(questions_data, NUM_QUESTIONS_PER_QUIZ)
    else:
        selected_questions = random.sample(questions_data, len(questions_data))
    
    st.session_state.questions_to_ask = selected_questions
    st.session_state.total_quiz_questions = len(selected_questions)
    st.session_state.current_question_index = 0
    st.session_state.score = 0
    st.session_state.user_answers = [None] * len(selected_questions)
    st.session_state.answer_submitted = False
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.quiz_start_time = 0.0
    st.session_state.time_up = False
    st.session_state.ranking_updated = False
    # Não limpa o user_info para que o usuário continue logado para novas tentativas
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}

def load_ranking():
    if not os.path.exists(RANKING_FILE):
        return []
    try:
        with open(RANKING_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_ranking(ranking_data):
    with open(RANKING_FILE, 'w', encoding='utf-8') as f:
        json.dump(ranking_data, f, indent=4, ensure_ascii=False)

def add_to_ranking(user_data, score, time_seconds, total_questions_quiz, questions_answered):
    ranking = load_ranking()
    new_entry = {
        "name": user_data.get("name", "Fantasma"),
        "email": user_data.get("email", ""),
        "city": user_data.get("city", ""),
        "country": user_data.get("country", ""),
        "score": score,
        "questions_answered": questions_answered,
        "time_seconds": int(time_seconds),
        "date": datetime.now().strftime("%d-%m-%Y %H:%M"),
        "total_questions": total_questions_quiz 
    }
    ranking.append(new_entry)
    # Ordena por pontos (desc) e depois por tempo (asc)
    ranking.sort(key=lambda x: (-x['score'], x['time_seconds']))
    top_10 = ranking[:10]
    save_ranking(top_10)

def display_question(question_data, current_idx, total_questions):
    # Título geral do simulado
    st.markdown("""            

    ### 🐍 Simulado Interativo da certificação em Python - PCEP

    """)

    st.markdown(
        f"<div class='quiz-question-text'><strong>Pergunta {current_idx + 1}/{total_questions}:</strong></div>", 
        unsafe_allow_html=True)

    question_text = question_data['question']

    # Pré-processar para blocos de código "cercados" por ```python ... ```
    # Regex para encontrar ```python ... ``` e substituir por <pre><code class="language-python">...</code></pre>
    # A flag re.DOTALL faz com que '.' corresponda também a quebras de linha
    question_text = re.sub(
        r'```python\s*\n(.*?)\n\s*```',
        r'<pre><code class="language-python">\1</code></pre>',
        question_text,
        flags=re.DOTALL
    )
    # Pré-processar para código inline (envolvido por crases simples)
    question_text = re.sub(r'`([^`]+)`', r'<code>\1</code>', question_text)

    st.markdown(f"<div class='quiz-question-text'>{question_text}</div>", unsafe_allow_html=True)
    original_options = list(question_data['options']) # Garante que é uma lista

    def format_option_for_display(opt_str):
        # Substitui múltiplos espaços por &nbsp; para correta renderização no HTML
        # Trata de 2 a 5 espaços consecutivos. Pode ser expandido se necessário.
        s = opt_str
        s = s.replace("     ", "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;") # 5 espaços
        s = s.replace("    ", "&nbsp;&nbsp;&nbsp;&nbsp;")   # 4 espaços
        s = s.replace("   ", "&nbsp;&nbsp;&nbsp;")      # 3 espaços
        s = s.replace("  ", "&nbsp;&nbsp;")         # 2 espaços
        return s

    display_options = [format_option_for_display(opt) for opt in original_options]
    
    # Determina o índice para st.radio com base na resposta original armazenada
    current_user_original_answer = st.session_state.user_answers[current_idx]
    radio_index = None
    if st.session_state.answer_submitted and current_user_original_answer is not None:
        try:
            # Encontra o índice da resposta original nas opções originais
            original_answer_index = original_options.index(current_user_original_answer)
            radio_index = original_answer_index # st.radio usará este índice com display_options
        except ValueError:
            # Caso a resposta armazenada não esteja nas opções originais (improvável com dados consistentes)
            radio_index = None

    # st.radio usa unsafe_allow_html implicitamente para as opções se elas contiverem HTML simples como &nbsp;
    user_choice_display_value = st.radio(
        "Escolha sua resposta:",
        options=display_options, # Usa as opções formatadas para exibição
        index=radio_index,
        key=f"q_radio_{current_idx}",
        disabled=st.session_state.answer_submitted
    )

    # Mapeia a escolha de exibição de volta para o valor da opção original
    if user_choice_display_value is not None:
        selected_display_index = display_options.index(user_choice_display_value)
        user_selected_original_option = original_options[selected_display_index]
        return user_selected_original_option
    return None

def display_timer_and_handle_timeout():
    if st.session_state.quiz_started and not st.session_state.quiz_completed and st.session_state.quiz_start_time > 0:
        timer_placeholder = st.sidebar.empty()
        current_time = time.time()
        elapsed = current_time - st.session_state.quiz_start_time
        time_limit_sec = QUIZ_TIME_LIMIT_MINUTES * 60

        if elapsed >= time_limit_sec:
            if not st.session_state.time_up:
                st.session_state.time_up = True
                st.session_state.quiz_completed = True
                timer_placeholder.error("⏰ Tempo Esgotado!")
                st.warning("⏰ Seu tempo para o quiz esgotou! Verificando resultados...")
                st.experimental_rerun()
            return

        remaining_time = time_limit_sec - elapsed
        minutes = int(remaining_time // 60)
        seconds = int(remaining_time % 60)
        timer_placeholder.markdown(
            f"<div class='timer-display'>⏳ Tempo Restante: {minutes:02d}:{seconds:02d}</div>", 
            unsafe_allow_html=True
        )

        display_ranking_sidebar()
        time.sleep(1)
        st.rerun()

def display_ranking_sidebar():
    st.sidebar.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    with st.sidebar.expander("🏆 Top 10 Ranking", expanded=False):
        ranking_data = load_ranking()
        if not ranking_data:
            st.write("O ranking ainda está vazio. Seja o primeiro a pontuar!")
        else:
            # Calcula a porcentagem para cada entrada
            for entry in ranking_data:
                total_q = entry.get('total_questions', NUM_QUESTIONS_PER_QUIZ) # Usa NUM_QUESTIONS_PER_QUIZ como fallback
                entry['percentage'] = (entry['score'] / total_q) * 100 if total_q > 0 else 0

            df = pd.DataFrame(ranking_data)
            # Formata o tempo para exibição
            df['Tempo'] = df['time_seconds'].apply(lambda s: f"{int(s // 60):02d}:{int(s % 60):02d}")
            # Formata a porcentagem para exibição
            df['Porcentagem'] = df['percentage'].apply(lambda p: f"{int(p)}%")
            # Seleciona e renomeia colunas para exibição
            df_display = df[['name', 'Porcentagem', 'Tempo', 'city', 'country']]
            df_display.columns = ["Nome", "Acerto", "Tempo", "Cidade", "País"]
            # Define o índice para começar em 1 (para o ranking)
            df_display.index = range(1, len(df_display) + 1)
            st.dataframe(df_display, use_container_width=True)

def show_results_page():
    score = st.session_state.score
    total = st.session_state.total_quiz_questions
    final_time_seconds = time.time() - st.session_state.quiz_start_time
    user_info = st.session_state.get("user_info", {})
    pct = (score / total) * 100 if total > 0 else 0

    if pct >= PASSING_PERCENTAGE:
        st.header("🎉 Simulado Concluído! 🎉")
    else:
        st.header("👎🏾 Simulado Concluído! 👎🏾")

    if st.session_state.get("time_up", False):
        st.warning("⏰ Seu tempo para o quiz esgotou!")

    # Garante que o ranking seja atualizado apenas uma vez por quiz
    if not st.session_state.get("ranking_updated", False):
        questions_answered = sum(1 for answer in st.session_state.user_answers if answer is not None)
        add_to_ranking(user_info, score, final_time_seconds, total, questions_answered)
        st.session_state.ranking_updated = True

    display_ranking_sidebar()

    st.markdown(f"<p class='score-display'>Você acertou {score} de {total} questões. ({pct:.1f}%)</p>", unsafe_allow_html=True)
    
    if pct >= PASSING_PERCENTAGE:
        st.success("Parabéns! Você foi aprovado na certificação PCEP! ✅")
        st.balloons()  # balões só para APROVADOS
        st.markdown("<div class='centered-gif-mobile'>", unsafe_allow_html=True)
        st.image("https://imagens.net.br/wp-content/uploads/2024/06/os-melhores-gifs-de-parabens-para-qualquer-ocasiao-1.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.error("Você não atingiu a pontuação mínima para aprovação. Tente novamente! ❌")
        st.snow() # emojis de gelor para REPROVADOS
        st.markdown("<div class='centered-gif-mobile'>", unsafe_allow_html=True)
        st.image("https://media1.tenor.com/m/gw207uCZe_MAAAAC/estuda-porra-evelyn-castro.gif", width=300)
        st.markdown("</div>", unsafe_allow_html=True)

    with st.expander("📖 Revisar apenas as questões respondidas"):
        any_answered = False
        if not st.session_state.questions_to_ask:
            st.write("Nenhuma questão para revisar.")
        else:
            for i, q_data_original in enumerate(st.session_state.questions_to_ask):
                user_answer_for_this_q = st.session_state.user_answers[i]

                if user_answer_for_this_q is not None:  # Usuário respondeu a esta pergunta
                    any_answered = True
                    st.markdown(f"**Pergunta {i + 1}:**") # Usa o índice original da pergunta
                    st.markdown(q_data_original['question'], unsafe_allow_html=True)
                    st.markdown(f"**Sua resposta:** {user_answer_for_this_q}")

                    if user_answer_for_this_q == q_data_original["answer"]:
                        st.markdown(f"**Resultado:** Correto ✅")
                    else:
                        st.markdown(f"**Resultado:** Incorreto ❌")
                        st.markdown(f"**Resposta correta:** {q_data_original['answer']}")

                    st.markdown(
                        f"<div class='explanation-box'><strong>🧠 Explicação:</strong><br>{q_data_original.get('explanation', 'Nenhuma explicação disponível.')}</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown("---")
            
            if not any_answered and st.session_state.questions_to_ask:
              st.write("Você não respondeu a nenhuma questão.")

    if st.button("Reiniciar Simulado ♻️"):
        initialize_quiz_session()
        st.session_state.quiz_started = False
        st.session_state.quiz_completed = False
        st.rerun()

# --- Inicializar estado do simulado ---
if "questions_to_ask" not in st.session_state:
    initialize_quiz_session()

# --- Interface principal do simulado ---
if not st.session_state.quiz_started:
    st.markdown("""
        <div style="display: flex; align-items: center; gap: 12px;">
            <img src="https://static.cdnlogo.com/logos/p/83/python.svg" alt="Python Logo" width="65"/>
            <h1 style="margin: 0;">Simulado Interativo da certificação em Python - PCEP</h1>
            <img src="https://pythoninstitute.org/assets/61f11fac8e6f4153315957.png" alt="PCEP Logo" width="60"/>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
### 📢 Sobre a Certificação PCEP:
                
Este simulado é baseado na prova oficial **PCEP™ – Certified Entry-Level Python Programmer**, (Exam PCEP-30-0x) oferecida pelo [Python Institute](https://pythoninstitute.org/pcep).

---
                
📝 **Formato da Prova Oficial:**
- 🔢 **Número de questões:** 30 (múltipla escolha)  
- ⏰ **Tempo para realização:** 45 minutos  
- ✅ **Nota mínima para aprovação:** 70% (ou seja, 21 de 30 questões)  
- 📌 **Aplicação:** Online com supervisão por IA (_proctoring_) ou presencial em centros **Pearson VUE**

🧠 Utilize este simulado para testar seus conhecimentos e se preparar para a certificação real!

""")
    
    display_ranking_sidebar() # Exibe o ranking na página inicial
    with st.expander("👤 Cadastro para o Top 10 Ranking (Opcional)"):
        with st.form("registration_form"):
            name = st.text_input("Nome")
            email = st.text_input("Email")
            city = st.text_input("Cidade")
            country = st.text_input("País")
            submitted = st.form_submit_button("Salvar Cadastro")
            if submitted and name: # Nome é obrigatório para o cadastro
                st.session_state.user_info = {
                    "name": name, "email": email, "city": city, "country": country
                }
                st.success(f"Olá, {name}! Você está cadastrado para o ranking.")

    if st.session_state.get("user_info", {}).get("name"):
        st.info(f"✅ Logado como **{st.session_state.user_info['name']}**. Seu resultado será registrado no ranking se estiver no Top 10.")

    if st.button("🚀 Iniciar Simulado"):
        st.session_state.quiz_started = True
        st.session_state.quiz_start_time = time.time()
        st.rerun()

elif st.session_state.quiz_completed:
    show_results_page()

else:
    current_idx = st.session_state.current_question_index
    total_questions = st.session_state.total_quiz_questions
    current_question = st.session_state.questions_to_ask[current_idx]

    # --- Barra de Progresso ---
    # O progresso e o texto devem refletir a questão atual (índice + 1)
    progress_value = (current_idx + 1) / total_questions
    st.markdown(
        f"<div class='progress-text'>{current_idx + 1} / {total_questions}</div>", 
        unsafe_allow_html=True
    )
    st.progress(progress_value)
    # --- Fim da Barra de Progresso ---
    user_choice = display_question(current_question, current_idx, total_questions)

    # Criar um placeholder para a área de feedback (sucesso/erro e explicação)
    feedback_placeholder = st.empty()
    # Criar um placeholder para os botões de ação após o feedback
    initial_action_buttons_placeholder = st.empty()
    # Criar um placeholder para os botões de ação após o feedback
    action_buttons_placeholder = st.empty()

    if not st.session_state.answer_submitted:
        # Botões "Confirmar e Avançar" e "Finalizar Simulado" DENTRO do placeholder inicial
        with initial_action_buttons_placeholder.container():
            col1, col2 = st.columns([3, 1.1]) # Ajuste a proporção conforme necessário
            with col1:
                if st.button("Confirmar e Avançar ❯", key=f"confirm_next_{current_idx}", use_container_width=True):
                    if user_choice is not None:  # Usuário selecionou uma resposta
                        st.session_state.answer_submitted = True
                        st.session_state.user_answers[current_idx] = user_choice
                        if user_choice == current_question["answer"]:
                            st.session_state.score += 1
                        initial_action_buttons_placeholder.empty() # Limpa estes botões
                        # Não avança o índice ainda, apenas reroda para mostrar o feedback
                        st.rerun()
                    else:  # Usuário não selecionou, considera como "pulada" e avança
                        st.session_state.user_answers[current_idx] = None # Marca como não respondida
                        if current_idx < total_questions - 1:
                            st.session_state.current_question_index += 1
                            # st.session_state.answer_submitted permanece False
                        else:
                            st.session_state.quiz_completed = True
                        initial_action_buttons_placeholder.empty() # Limpa estes botões
                        st.rerun()
            with col2:
                if st.button("Finalizar Simulado 🏁", key="finalizar_quiz_main", use_container_width=True):
                    st.session_state.quiz_completed = True
                    initial_action_buttons_placeholder.empty() # Limpa estes botões
                    if hasattr(st.session_state, 'timer_placeholder'): # Garante que o placeholder do timer existe
                        st.session_state.timer_placeholder.empty() # Limpa o timer também ao finalizar
                    else:
                        st.sidebar.empty() # Tenta limpar a sidebar se o placeholder específico não foi definido
                    st.rerun()
    else:
        # Resposta já foi submetida (answer_submitted is True), mostrar feedback DENTRO do placeholder
        with feedback_placeholder.container(): # Usar .container() para agrupar múltiplos elementos no placeholder
            correct_answer = current_question["answer"]
            user_answer_for_current_q = st.session_state.user_answers[current_idx]

            if user_answer_for_current_q == correct_answer:
                st.success("✅ Resposta correta!")
            else:
                st.error(f"❌ Resposta incorreta! A resposta correta é: **{correct_answer}**")

            st.markdown(
                f"<div class='explanation-box'><strong>🧠 Explicação:</strong><br>{current_question.get('explanation', 'Nenhuma explicação disponível.')}</div><br>",
                unsafe_allow_html=True
            )


        # Botões após o feedback DENTRO do placeholder de botões de ação
        with action_buttons_placeholder.container():
            col1, col2 = st.columns([3, 1.1])
            with col1:
                if current_idx < total_questions - 1:
                    if st.button("Próxima Pergunta ➡️", key=f"next_question_{current_idx}", use_container_width=True):
                        st.session_state.current_question_index += 1
                        st.session_state.answer_submitted = False  # Reset para a próxima pergunta
                        initial_action_buttons_placeholder.empty() # Garante que os botões iniciais não reapareçam indevidamente
                        feedback_placeholder.empty() # Limpa o feedback anterior
                        action_buttons_placeholder.empty() # Limpa estes botões
                        st.rerun()
                else: # Última pergunta já respondida e feedback mostrado
                    if st.button("Ver Resultado Final 🏁", key="finish_quiz_final_feedback", use_container_width=True):
                        st.session_state.quiz_completed = True
                        feedback_placeholder.empty()
                        action_buttons_placeholder.empty()
                        st.rerun()
            with col2:
                if st.button("Finalizar Simulado 🏁", key="finalizar_quiz_feedback", use_container_width=True):
                    st.session_state.quiz_completed = True
                    feedback_placeholder.empty()
                    action_buttons_placeholder.empty()
                    if hasattr(st.session_state, 'timer_placeholder'):
                        st.session_state.timer_placeholder.empty()
                    else:
                        st.sidebar.empty()
                    st.rerun()

display_timer_and_handle_timeout()

# --- Rodapé com informações do desenvolvedor e versão ---
st.markdown(
    f"""
    <div class="rodape-container">
      <div class="rodape">
          <div class="linha"> 👨🏾‍💻 <b>Desenvolvido por:</b></div>
          <div class="links">
              <a href="https://github.com/pedroar9/" target="_blank">
                  <img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white">
              </a>
              <a href="https://www.linkedin.com/in/pedrocarlos-assis/" target="_blank">
                  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white">
              </a>         
          </div>  
          <div class="linha"> <br> </div>
          <div class="linha">⚙️ <b>Versão:</b> 3.0.0</div> 
          <div class="linha">🗓️ <b>Build:</b> {data_atual}</div>        
      </div>
    </div>
    """,
    unsafe_allow_html=True
)