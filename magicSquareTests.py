import datetime
import random
import unittest
import genetic
import matplotlib.pyplot as plt

#El problema que se busca resolver es el de encontrar una matriz cuadrada de tamaño n, tal que la suma de cada fila, columna y diagonal sea igual a la suma esperada

#Las variables que se toman en cuenta para resolver este problema son:
# - diagonalSize: Tamaño de la matriz
# - expectedSum: Suma esperada de cada fila, columna y diagonal
# - maxAge: Edad máxima de la población
# - mutationCount: Cantidad de mutaciones
# - poolSize: Tamaño de la población

#El algoritmo genético procede de la siguiente manera:
# - Se crea una población inicial de 100 individuos
# - Se evalúa la aptitud de cada individuo
# - Se seleccionan los individuos más aptos
# - Se cruzan los individuos seleccionados
# - Se mutan los individuos
# - Se evalúa la aptitud de los individuos mutados
# - Se seleccionan los individuos más aptos
# - Se repite el proceso hasta que se cumpla la condición de parada
# - Se retorna el individuo más apto

#La generación de ruido se hace de la siguiente manera:
# - Se toma un individuo de la población
# - Se toman dos genes aleatorios del individuo
# - Se intercambian los genes
# - Se retorna el individuo mutado
# - Se repite el proceso hasta que se hayan mutado todos los individuos de la población

#La función de selección se hace de la siguiente manera:
# - Se toman dos individuos aleatorios de la población
# - Se retorna el individuo más apto
# - Se repite el proceso hasta que se hayan seleccionado todos los individuos de la población

#La función de reproducción se hace de la siguiente manera:
# - Se toman dos individuos aleatorios de la población
# - Se toman dos genes aleatorios de cada individuo
# - Se intercambian los genes
# - Se retorna el individuo más apto

#La función de mutación se hace de la siguiente manera:
# - Se toman dos genes aleatorios del individuo
# - Se intercambian los genes
# - Se retorna el individuo mutado
#El tipo de mutación que se utiliza es la de intercambio de genes

#La función aptitud se define como la suma de las diferencias entre la suma esperada y la suma de cada fila, columna y diagonal

#Para la generación de individuos se utiliza la clase Chromosome la cual los crea de forma aleatoria

#Los genes se componen de números del 1 al 10
#Lo que representa cada gen es el número que se encuentra en la posición de la matriz

#Ejemplo de generación del individuo mas apto
# 1 2 3 4 5 6 7 8 9 10
# 11 12 13 14 15 16 17 18 19 20
# 21 22 23 24 25 26 27 28 29 30
# 31 32 33 34 35 36 37 38 39 40
# 41 42 43 44 45 46 47 48 49 50
# 51 52 53 54 55 56 57 58 59 60
# 61 62 63 64 65 66 67 68 69 70
# 71 72 73 74 75 76 77 78 79 80
# 81 82 83 84 85 86 87 88 89 90
# 91 92 93 94 95 96 97 98 99 100

#Lo primero que hace el programa es crear una población inicial de 100 individuos
#Luego evalúa la aptitud de cada individuo
#Selecciona los individuos más aptos
#Cruza los individuos seleccionados
#Muta los individuos
#Evalúa la aptitud de los individuos mutados

x = []
y = []

def get_fitness(genes, diagonalSize, expectedSum): #Método de fitness para el problema de las matrices mágicas
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = \
        get_sums(genes, diagonalSize) #Se obtienen las sumas de las filas, columnas y diagonales
    sumOfDifferences = sum(int(abs(s - expectedSum)) #Se obtiene la suma de las diferencias entre la suma esperada y la suma de cada fila, columna y diagonal
                        for s in rows + columns +
                        [southeastDiagonalSum, northeastDiagonalSum]
                            if s != expectedSum)
    return Fitness(sumOfDifferences)


def display(candidate, diagonalSize, startTime): #Método para mostrar el individuo mas apto
    timeDiff = datetime.datetime.now() - startTime 
    #Se obtienen las sumas de las filas, columnas y diagonales
    rows, columns, northeastDiagonalSum, southeastDiagonalSum = \
        get_sums(candidate.Genes, diagonalSize) 

    for rowNumber in range(diagonalSize): #Se muestran las filas de la matriz
        row = candidate.Genes[
              rowNumber * diagonalSize:(rowNumber + 1) * diagonalSize]
        print("\t ", row, "=", rows[rowNumber])
    print(northeastDiagonalSum, "\t", columns, "\t", southeastDiagonalSum)
    print(" - - - - - - - - - - -", candidate.Fitness, timeDiff)
    #Añadimos los datos a la gráfica



def get_sums(genes, diagonalSize): #Método para obtener las sumas de las filas, columnas y diagonales de la matriz
    rows = [0 for _ in range(diagonalSize)] #Se inicializan las sumas de las filas en 0 
    columns = [0 for _ in range(diagonalSize)] #Se inicializan las sumas de las columnas en 0
    southeastDiagonalSum = 0
    northeastDiagonalSum = 0
    for row in range(diagonalSize): #Se recorren las filas de la matriz 
        for column in range(diagonalSize): #Se recorren las columnas de la matriz 
            value = genes[row * diagonalSize + column] #Se obtiene el valor de la celda actual
            rows[row] += value #Se suma el valor de la celda actual a la suma de la fila actual
            columns[column] += value #Se suma el valor de la celda actual a la suma de la columna actual
        southeastDiagonalSum += genes[row * diagonalSize + row] #Se suma el valor de la celda actual a la suma de la diagonal sur-este
        northeastDiagonalSum += genes[row * diagonalSize + #Se suma el valor de la celda actual a la suma de la diagonal norte-este
                                        (diagonalSize - 1 - row)] #Se resta 1 al tamaño de la matriz para obtener la columna de la celda actual
    return rows, columns, northeastDiagonalSum, southeastDiagonalSum #Se crea la clase Fitness para el problema de las matrices mágicas


def mutate(genes, indexes): #Método para mutar los genes de un individuo
    indexA, indexB = random.sample(indexes, 2) #Se toman dos genes aleatorios del individuo
    genes[indexA], genes[indexB] = genes[indexB], genes[indexA] #Se intercambian los genes


class MagicSquareTests(unittest.TestCase): #Clase para realizar las pruebas unitarias del problema de las matrices mágicas
    def test_size_3(self): #Método para generar una matriz mágica de tamaño 3
        self.generate(3, 50)#Se genera una matriz mágica de tamaño 3 con 50 individuos

    def test_size_4(self):#Método para generar una matriz mágica de tamaño 4
        self.generate(4, 50)#Se genera una matriz mágica de tamaño 4 con 50 individuos

    def test_size_5(self):#Método para generar una matriz mágica de tamaño 5
        self.generate(5, 500)#Se genera una matriz mágica de tamaño 5 con 500 individuos

    def test_size_10(self):#Método para generar una matriz mágica de tamaño 10
        self.generate(10, 5000)#Se genera una matriz mágica de tamaño 10 con 5000 individuos

    def test_benchmark(self):#Método para generar una matriz mágica de tamaño 20
        genetic.Benchmark.run(self.test_size_3)#Se genera una matriz mágica de tamaño 20 con 50000 individuos
        

    def generate(self, diagonalSize, maxAge):#Método para generar una matriz mágica de tamaño diagonalSize
        nSquared = diagonalSize * diagonalSize#Se obtiene el tamaño de la matriz al cuadrado
        geneset = [i for i in range(1, nSquared + 1)]#Se crea el conjunto de genes
        expectedSum = diagonalSize * (nSquared + 1) / 2#Se obtiene la suma esperada de las filas, columnas y diagonales

        def fnGetFitness(genes):#Método para obtener el fitness de un individuo
            return get_fitness(genes, diagonalSize, expectedSum)#Se retorna el fitness del individuo

        def fnDisplay(candidate):#Método para mostrar el individuo mas apto
            display(candidate, diagonalSize, startTime)#Se muestra el individuo mas apto

        geneIndexes = [i for i in range(0, len(geneset))]#Se crea un arreglo con los indices de los genes

        def fnMutate(genes):#Método para mutar los genes de un individuo 
            mutate(genes, geneIndexes)#Se mutan los genes del individuo

        def fnCustomCreate():#Método para crear un individuo aleatorio
            return random.sample(geneset, len(geneset)) #Se crea un individuo aleatorio con los genes del conjunto de genes

        optimalValue = Fitness(1)#Se crea el fitness óptimo para el problema
        startTime = datetime.datetime.now()#Se obtiene la hora actual del sistema
        best = genetic.get_best(fnGetFitness, nSquared, optimalValue,#Se obtiene el individuo mas apto para el problema
                                geneset, fnDisplay, fnMutate, fnCustomCreate,#Se pasan los parámetros necesarios para el algoritmo genético
                                maxAge)
        self.assertTrue(not optimalValue > best.Fitness)#Se verifica que el fitness del individuo mas apto sea óptimo


class Fitness:#Se crea la clase Fitness para el problema de las matrices mágicas
    def __init__(self, sumOfDifferences):#Constructor de la clase Fitness
        self.SumOfDifferences = sumOfDifferences#Se inicializa el atributo SumOfDifferences que representa la suma de las diferencias entre las sumas de las filas, columnas y diagonales

    def __gt__(self, other):#Método para comparar dos fitness 
        return self.SumOfDifferences < other.SumOfDifferences#Se retorna el fitness con menor suma de diferencias entre las sumas de las filas, columnas y diagonales

    def __str__(self):#Método para obtener la representación en cadena de un fitness
        return "{}".format(self.SumOfDifferences)#Se retorna la suma de las diferencias entre las sumas de las filas, columnas y diagonales


if __name__ == '__main__':
    unittest.main()
    #Guardamos la gráfica en un archivo
    