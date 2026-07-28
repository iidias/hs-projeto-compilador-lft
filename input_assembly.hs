-- Programa de exemplo dentro do escopo combinado para a Assembly
-- Sem data/lista/tupla

-- funcao recursiva (fatorial CORRETO, com n - 1)
fatorial :: Int -> Int
fatorial 0 = 1
fatorial n = n * fatorial (n - 1)

-- guardas
classificar :: Int -> Int
classificar n
    | n < 0     = -1
    | n == 0    = 0
    | otherwise = 1

-- where: definicoes locais ao final da funcao
dobra_e_soma :: Int -> Int -> Int
dobra_e_soma a b = resultado
    where
        dobro     = a * 2
        resultado = dobro + b

-- let-in: definicoes locais dentro de uma expressao
calc :: Int -> Int -> Int
calc a b =
    let soma  = a + b
        dobro = soma * 2
    in dobro + 1

-- recursao com guardas: MDC de Euclides
mdc :: Int -> Int -> Int
mdc a b
    | b == 0    = a
    | otherwise = mdc b (a mod b)

-- do com let agrupado e return: junta tudo num resultado so
main :: IO ()
main = do
    let f = fatorial 5
        c = classificar (-7)
        d = dobra_e_soma 3 4
        e = calc 10 20
        g = mdc 48 18
    return (f + c + d + e + g)