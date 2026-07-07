-- Comentário na primeira linha
data Forma = Circulo Int
           | Retangulo Int Int

area :: Forma -> Int
area f = case f of
    Circulo r  -> r * r
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

main :: IO ()
main = do
    let r = area (Circulo 5)
    return r
