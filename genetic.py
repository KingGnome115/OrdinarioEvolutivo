import random
import statistics
import sys
import time
from bisect import bisect_left
from math import exp


def _generate_parent(length, geneSet, get_fitness): #Método que genera un padre aleatorio
    genes = []
    while len(genes) < length: #Mientras la longitud de genes sea menor a la longitud del padre 
        sampleSize = min(length - len(genes), len(geneSet)) #Tamaño de la muestra es el minimo entre la longitud del padre y la longitud del conjunto de genes
        genes.extend(random.sample(geneSet, sampleSize)) #Se extiende la lista de genes con una muestra aleatoria del conjunto de genes
    fitness = get_fitness(genes)#Se calcula el fitness del padre generado (el fitness es la cantidad de genes que coinciden con el objetivo)
    return Chromosome(genes, fitness) #Se retorna el padre generado


def _mutate(parent, geneSet, get_fitness):#Método que muta un padre para generar un hijo
    childGenes = parent.Genes[:] #Se copia la lista de genes del padre al hijo
    index = random.randrange(0, len(parent.Genes)) #Se elige un indice aleatorio entre 0 y la longitud del padre
    newGene, alternate = random.sample(geneSet, 2) #Se eligen dos genes aleatorios del conjunto de genes 
    childGenes[index] = alternate if newGene == childGenes[index] else newGene #Si el nuevo gen es igual al gen del padre en el indice elegido, se cambia por el otro gen aleatorio, de lo contrario se cambia por el nuevo gen
    fitness = get_fitness(childGenes)#Se calcula el fitness del hijo generado (el fitness es la cantidad de genes que coinciden con el objetivo)
    return Chromosome(childGenes, fitness)# regresa el fitness de un individuo


def _mutate_custom(parent, custom_mutate, get_fitness):#Método que muta un padre para generar un hijo con una mutación personalizada
    childGenes = parent.Genes[:] #Se copia la lista de genes del padre al hijo
    custom_mutate(childGenes)#Se muta el hijo con la mutación personalizada
    fitness = get_fitness(childGenes) #Se calcula el fitness del hijo generado (el fitness es la cantidad de genes que coinciden con el objetivo) 
    return Chromosome(childGenes, fitness)


def get_best(get_fitness, targetLen, optimalFitness, geneSet, display, #Método que obtiene el mejor individuo de una población
            custom_mutate=None, custom_create=None, maxAge=None):
    if custom_mutate is None: #Si no se especifica una mutación personalizada se usa la mutación por defecto
        def fnMutate(parent): #Método que muta un padre para generar un hijo con la mutación por defecto
            return _mutate(parent, geneSet, get_fitness) 
    else:
        def fnMutate(parent): #Método que muta un padre para generar un hijo con una mutación personalizada
            return _mutate_custom(parent, custom_mutate, get_fitness)

    if custom_create is None: #Si no se especifica una creación personalizada se usa la creación por defecto
        def fnGenerateParent(): #Método que genera un padre aleatorio con la creación por defecto
            return _generate_parent(targetLen, geneSet, get_fitness) #Se genera un padre aleatorio con la creacion por defecto
    else:
        def fnGenerateParent(): #Método que genera un padre aleatorio con una creación personalizada
            genes = custom_create() #Se genera un padre aleatorio con la creación personalizada
            return Chromosome(genes, get_fitness(genes))

    for improvement in _get_improvement(fnMutate, fnGenerateParent, maxAge): #Se obtiene el mejor individuo de la población 
        display(improvement) #Se muestra el mejor individuo de la población 
        if not optimalFitness > improvement.Fitness: #Si el fitness del mejor individuo es mayor o igual al fitness optimo se retorna el mejor individuo
            return improvement


def _get_improvement(new_child, generate_parent, maxAge): #Método que obtiene el mejor individuo de una población
    parent = bestParent = generate_parent() #Se genera un padre aleatorio
    yield bestParent #Se retorna el mejor individuo de la población 
    historicalFitnesses = [bestParent.Fitness] #Se crea una lista con el fitness del mejor individuo de la población 
    while True:
        child = new_child(parent) #Se muta el padre para generar un hijo 
        if parent.Fitness > child.Fitness: #Si el fitness del padre es mayor al fitness del hijo se muta el padre para generar un hijo
            if maxAge is None: #Si no se especifica una edad maxima se muta el padre para generar un hijo
                continue #Se muta el padre para generar un hijo
            parent.Age += 1 #Si se especifica una edad maxima se aumenta la edad del padre
            if maxAge > parent.Age: #Si la edad del padre es menor a la edad maxima se muta el padre para generar un hijo
                continue
            index = bisect_left(historicalFitnesses, child.Fitness, 0, #Si la edad del padre es mayor o igual a la edad maxima se muta el padre para generar un hijo
                                len(historicalFitnesses))#Se muta el padre para generar un hijo
            proportionSimilar = index / len(historicalFitnesses)
            if random.random() < exp(-proportionSimilar):
                parent = child
                continue
            bestParent.Age = 0 #La edad del mejor individuo de la población se reinicia
            parent = bestParent#El padre se reinicia
            continue
        if not child.Fitness > parent.Fitness:#Si el fitness del hijo es mayor al fitness del padre se muta el padre para generar un hijo
            # same fitness
            child.Age = parent.Age + 1#Si el fitness del hijo es igual al fitness del padre se aumenta la edad del hijo
            parent = child
            continue
        child.Age = 0
        parent = child
        if child.Fitness > bestParent.Fitness:#Si el fitness del hijo es mayor al fitness del mejor individuo de la población se muta el padre para generar un hijo
            bestParent = child
            yield bestParent#Se retorna el mejor individuo de la población
            historicalFitnesses.append(bestParent.Fitness)#Se agrega el fitness del mejor individuo de la población a la lista de fitness históricos


class Chromosome:#Clase que representa un individuo de la población
    def __init__(self, genes, fitness):#Constructor de la clase
        self.Genes = genes#Lista de genes del individuo
        self.Fitness = fitness#Fitness del individuo
        self.Age = 0#Edad del individuo


class Benchmark:#Clase que representa un benchmark para medir el tiempo de ejecución de un algoritmo
    @staticmethod#Método estático
    def run(function):#Método que ejecuta un algoritmo y mide el tiempo de ejecución
        timings = []#Lista de tiempos de ejecución
        stdout = sys.stdout#Se guarda la salida estándar
        for i in range(100):#Se ejecuta el algoritmo 100 veces
            sys.stdout = None#Se deshabilita la salida estándar
            startTime = time.time()#Se obtiene el tiempo de inicio de ejecución
            function()#Se ejecuta el algoritmo
            seconds = time.time() - startTime#Se obtiene el tiempo de ejecución
            sys.stdout = stdout#Se habilita la salida estándar
            timings.append(seconds)# Se agrega el tiempo de ejecución a la lista de tiempos de ejecución
            mean = statistics.mean(timings)#Se calcula el promedio de los tiempos de ejecución
            if i < 10 or i % 10 == 9:#Si es la primera iteración o la iteración es múltiplo de 10 se muestra el promedio de los tiempos de ejecución
                print("{} {:3.2f} {:3.2f}".format(#Se muestra el promedio de los tiempos de ejecución
                    1 + i, mean,#Se muestra el promedio de los tiempos de ejecución
                    statistics.stdev(timings, mean) if i > 1 else 0))#Se muestra la desviación estándar de los tiempos de ejecución