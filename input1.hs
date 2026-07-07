-- Comentário na primeira linha
data Cor = Vermelho | Verde | Azul

-- case com construtor simples
descrever :: Cor -> String
descrever c = case c of
    Vermelho -> "quente"
    Verde    -> "neutro"
    Azul     -> "frio"

-- case com construtor com argumentos
data Forma = Circulo Int | Retangulo Int Int

area :: Forma -> Int
area f = case f of
    Circulo r     -> r * r
    Retangulo l a -> l * a

-- where: definições locais ao final da função
imc :: Int -> Int -> String
imc peso altura = resultado
    where
        indice    = peso / altura
        resultado = if indice < 2 then "abaixo" else "normal"

-- guardas
classificar :: Int -> String
classificar n
    | n < 0     = "negativo"
    | n == 0    = "zero"
    | otherwise = "positivo"

-- let-in: definições locais dentro de uma expressão
calc :: Int -> Int -> Int
calc a b =
    let soma  = a + b
        dobro = soma * 2
    in dobro + 1

-- função recursiva
fatorial :: Int -> Int
fatorial 0 = 1
fatorial n = n * fatorial n

-- do com let agrupado e return
main :: IO ()
main = do
    let x = 10
        y = x * 2
    return y
