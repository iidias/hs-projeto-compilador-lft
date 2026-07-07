-- Testa precedência: * antes de +, ^ antes de *
ex1 :: Int
ex1 = 1 + 2 * 3

-- Testa associatividade: - associa à esquerda
ex2 :: Int
ex2 = 10 - 3 - 2

-- Testa potência: associa à direita
ex3 :: Int
ex3 = 2 ^ 3 ^ 2

-- Testa operadores lógicos e relacionais juntos
ex4 :: Bool
ex4 = 1 < 2 && 3 > 0

-- lambda com um argumento
dobrar :: Int -> Int
dobrar = \x -> x * 2

-- lambda com dois argumentos
somar :: Int -> Int -> Int
somar = \x y -> x + y

-- lambda usada diretamente em expressão
resultado :: Int
resultado = (\x -> x + 1) 5

-- literais básicos
inteiro :: Int
inteiro = 42

booleano :: Bool
booleano = True

texto :: String
texto = "ola mundo"

caractere :: Char
caractere = 'a'

-- lista e tupla
lista :: Int
lista = [1, 2, 3]

tupla :: Int
tupla = (1, 2)

-- range
intervalo :: Int
intervalo = [1..10]