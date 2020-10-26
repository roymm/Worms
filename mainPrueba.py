from gusanosPrueba import Worm
import numpy as np
import math
from mpi4py import MPI
import sys, getopt

HAND_TEST_FILENAME = 'poker-hand-training-true.data'


def euclidianDistance(pointA,pointB):
    assert len(pointA) == len(pointB)

    summation = 0
    for axisA, axisB in zip(pointA,pointB):
        summation += (axisB-axisA) ** 2

    return math.sqrt(summation)

def EQ1(worm, rho, gamma, resultEQ9):
    F = resultEQ9
    return ((1-rho) * worm.luciferin) + (gamma * F)


def EQ2(wormList, actualWorm, ratio):
    neighborsSet = []
    for index in range(len(wormList)):
        distance = euclidianDistance(wormList[index].position, actualWorm.position)
        #print(wormList[index].luciferin )
        #print(actualWorm.luciferin)
        if (distance < ratio and wormList[index].luciferin > actualWorm.luciferin):
            neighborsSet.append(wormList[index] )
            #print(distance)

    return neighborsSet


def EQ3(actualWorm, wormList, neighborsSet):
    sum= 0
    maxProbability = 0
    selectedWorm = actualWorm
    #selectedWorm = neighborsSet[0]
    for k in range (len(neighborsSet)):
        resultDifferece = neighborsSet[k].getLuciferin() - actualWorm.getLuciferin()
        for i in range (len(neighborsSet)):
            result = neighborsSet[i].getLuciferin() - actualWorm.getLuciferin()
            sum = sum + result
        finalResult = resultDifferece/sum
        if (finalResult > maxProbability):
            maxProbability = finalResult
            selectedWorm = neighborsSet[k]
    return selectedWorm


def EQ4(s, actualWorm, bestNeighbor):
    contador = 0
    newPositions = np.zeros(10)
    distancia = euclidianDistance(actualWorm.position, bestNeighbor.position)
    while (contador < 10):
        resultadoResta = bestNeighbor.position[contador]- actualWorm.position[contador]
        #print(resultadoResta)
        resultadoDivision = s * (resultadoResta/distancia)
        newPositions[contador] =actualWorm.position[contador]+ resultadoDivision
        contador+=1
    #print(newPositions)
    return newPositions


def EQ6(centroidsList, k):
    sumCentroid = 0
    sum = 0
    finalSum = 0
    #print(centroidsList)
    #print(centroidsList[0].totalHands)
    for index in range (len(centroidsList)):
        for permutation in (centroidsList[index].totalHands):
            x = 0
            for card in permutation:
                posicion = []
                #permutation = centroidsList[index].totalHands
                posicion.append(centroidsList[index].position[x])
                x += 1
                posicion.append(centroidsList[index].position[x])
                x += 1

                sum = sum + ((euclidianDistance(posicion, card))**2)
            sumCentroid= sumCentroid + sum
        finalSum = finalSum + sumCentroid


    return finalSum


def EQ7(k, centroidsList, wormList):
    result = 0
    sumI=0
    sumJ=0
    for i in range (len(centroidsList)):
        for j in range (len(centroidsList)):
            sumJ = sumJ + (euclidianDistance(centroidsList[i].position, centroidsList[j].position)**2)
        sumI = sumI + sumJ
    result = sumI
    return result

def EQ8(worm):
    intraD = 0
    finalIntraD = 0
    for permutation in worm.totalHands:
        x = 0
        for card in permutation:
            posicion = []
            #permutation = centroidsList[index].totalHands
            posicion.append(worm.position[x])
            x += 1
            posicion.append(worm.position[x])
            x += 1
            intraD += euclidianDistance(card, posicion)
        finalIntraD += finalIntraD + intraD
    return finalIntraD

def EQ9(n, resultEQ6, resultEQ8, actualWorm, intraDistances):
    result1 = (1/n)*actualWorm.total
    resultMultiplication= resultEQ6 * (resultEQ8/max(intraDistances))
    result = result1 / resultMultiplication
    #print(result)
    return result


#Funcion que crea los gusanos iniciales y hace otras cosas del inicio que todavia no sabemos
def initSetUp():
    testHands = []
    indexList = []
    #allCards = np.resize(np.arange(13),(5,4,13))

        #Agrega las 5 posiciones
    for i in range (5):
        indexList.append([])

            #Agrego los 4 palos
        for j in range(4):
            indexList[i].append([])

                #Agrego las lista inversa correspondiente a cada carta
            for k in range(13):
                indexList[i][j].append([])

    numLine = 0
    #Procesamiento de archivo de manos

    for line in open(HAND_TEST_FILENAME):
        arrayLine = np.fromstring(line, dtype=int, sep=',')
        position = 0

        for i in range(0,len(arrayLine)-1,2):
            rank = arrayLine[i] -1
            card = arrayLine[i+1] -1
            indexList[position][rank][card].append(numLine)
            position += 1

        numLine += 1
        testHands.append(arrayLine)

    testHands = np.array(testHands)
    #print(indexList[0][1][10])
    return indexList #LES HICE RETURN PORQUE CON EL GLOBAL NO ME CORRIA


#Funcion que toma una lista de listas (la propiedad dataSet de los gusanos) y relaciona cada carta con su posicion
# a una mano del archivo poker-hand-training-true.data
# Recibe una lista de pares [numero de carta, palo] y retorna una lista de enteros (indices del array testHands)
def searchIndex(permutations, indexList):
    wormIndexList = []
    handPermutations = []
    #posibleIndexList = []
    #print(permutations)
    #print(str(len(permutations)))
    #permutations = [ [[9,0],[10,0],[12,0],[11,0],[0,0]],  [[10,1],[12,1],[9,1],[11,1],[0,1]]]
    """permutations = [[[5, 0], [10, 1], [8, 0], [1, 0], [3, 1]], [[5, 0], [10, 1], [8, 0], [1, 0], [4, 1]], [[5, 0], [10, 1], [8, 0], [1, 0], [2, 2]], [[5, 0], [10, 1], [8, 0], [1, 0], [3, 2]], [[5, 0], [10, 1], [8, 0], [1, 0], [4, 2]], [[5, 0], [10, 1], [8, 0], [1, 0], [2, 3]], [[5, 0], [10, 1], [8, 0], [1, 0], [3, 3]], [[5, 0], [10, 1], [8, 0], [2, 0], [3, 1]], [[5, 0], [10, 1], [8, 0], [2, 0], [4, 1]], [[5, 0], [10, 
1], [8, 0], [2, 0], [2, 2]], [[5, 0], [10, 1], [8, 0], [2, 0], [3, 2]], [[5, 0], [10, 1], [8, 0], [2, 0], [4, 2]], [[5, 0], [10, 1], [8, 0], [2, 0], [2, 3]], [[5, 0], [10, 1], [8, 0], [2, 0], [3, 3]], 
[[5, 0], [10, 1], [8, 0], [0, 1], [3, 1]], [[5, 0], [10, 1], [8, 0], [0, 1], [4, 1]], [[5, 0], [10, 1], [8, 0], [0, 1], [2, 2]], [[5, 0], [10, 1], [8, 0], [0, 1], [3, 2]], [[5, 0], [10, 1], [8, 0], [0, 1], [4, 2]], [[5, 0], [10, 1], [8, 0], [0, 1], [2, 3]], [[5, 0], [10, 1], [8, 0], [0, 1], [3, 3]], [[5, 0], [10, 1], [8, 0], [1, 1], [3, 1]], [[5, 0], [10, 1], [8, 0], [1, 1], [4, 1]], [[5, 0], [10, 1], [8, 0], [1, 1], [2, 2]], [[5, 0], [10, 1], [8, 0], [1, 1], [3, 2]], [[5, 0], [10, 1], [8, 0], [1, 1], [4, 2]], [[5, 0], [10, 1], [8, 0], [1, 1], [2, 3]], [[5, 0], [10, 1], [8, 0], [1, 1], [3, 3]], [[5, 0], [10, 1], [8, 0], [2, 1], [3, 1]], [[5, 0], [10, 1], [8, 0], [2, 1], [4, 1]], [[5, 0], [10, 1], [8, 0], [2, 1], [2, 2]], [[5, 0], [10, 1], [8, 0], [2, 1], [3, 2]], [[5, 0], [10, 1], [8, 0], [2, 
1], [4, 2]], [[5, 0], [10, 1], [8, 0], [2, 1], [2, 3]], [[5, 0], [10, 1], [8, 0], [2, 1], [3, 3]], [[5, 0], [10, 1], [8, 0], [0, 2], [3, 1]], [[5, 0], [10, 1], [8, 0], [0, 2], [4, 1]], [[5, 0], [10, 1], [8, 0], [0, 2], [2, 2]], [[5, 0], [10, 1], [8, 0], [0, 2], [3, 2]], [[5, 0], [10, 1], [8, 0], [0, 2], [4, 2]], [[5, 0], [10, 1], [8, 0], [0, 2], [2, 3]], [[5, 0], [10, 1], [8, 0], [0, 2], [3, 3]], [[5, 0], [10, 1], [8, 0], [1, 2], [3, 1]], [[5, 0], [10, 1], [8, 0], [1, 2], [4, 1]], [[5, 0], [10, 1], [8, 0], [1, 2], [2, 2]], [[5, 0], [10, 1], [8, 0], [1, 2], [3, 2]], [[5, 0], [10, 1], [8, 0], [1, 2], [4, 2]], [[5, 0], [10, 1], [8, 0], [1, 2], [2, 3]], [[5, 0], [10, 1], [8, 0], [1, 2], [3, 3]], [[5, 0], [10, 1], [7, 1], [1, 0], [3, 1]], [[5, 0], [10, 1], [7, 1], [1, 0], [4, 1]], [[5, 0], [10, 1], [7, 1], [1, 0], [2, 2]], [[5, 0], [10, 1], [7, 1], [1, 0], [3, 2]], [[5, 0], [10, 1], [7, 1], [1, 0], [4, 2]], [[5, 0], [10, 1], [7, 1], [1, 0], [2, 3]], [[5, 0], [10, 1], [7, 1], [1, 0], [3, 3]], [[5, 0], [10, 1], [7, 1], [2, 0], [3, 1]], [[5, 0], [10, 1], [7, 1], [2, 0], [4, 1]], [[5, 0], [10, 1], [7, 1], [2, 0], [2, 2]], [[5, 0], [10, 1], [7, 1], [2, 0], [3, 2]], [[5, 0], [10, 1], [7, 1], [2, 0], [4, 2]], [[5, 0], [10, 1], [7, 1], [2, 0], [2, 3]], [[5, 0], [10, 1], [7, 1], [2, 0], [3, 3]], [[5, 0], [10, 1], [7, 1], [0, 1], [3, 1]], [[5, 0], [10, 1], [7, 1], [0, 1], [4, 1]], [[5, 0], [10, 1], 
[7, 1], [0, 1], [2, 2]], [[5, 0], [10, 1], [7, 1], [0, 1], [3, 2]], [[5, 0], [10, 1], [7, 1], [0, 1], [4, 2]], [[5, 0], [10, 1], [7, 1], [0, 1], [2, 3]], [[5, 0], [10, 1], [7, 1], [0, 1], [3, 3]], [[5, 0], [10, 1], [7, 1], [1, 1], [3, 1]], [[5, 0], [10, 1], [7, 1], [1, 1], [4, 1]], [[5, 0], [10, 1], [7, 1], [1, 1], [2, 2]], [[5, 0], [10, 1], [7, 1], [1, 1], [3, 2]], [[5, 0], [10, 1], [7, 1], [1, 1], [4, 2]], [[5, 0], [10, 1], [7, 1], [1, 1], [2, 3]], [[5, 0], [10, 1], [7, 1], [1, 1], [3, 3]], [[5, 0], [10, 1], [7, 1], [2, 1], [3, 1]], [[5, 0], [10, 1], [7, 1], [2, 1], [4, 1]], [[5, 0], [10, 1], [7, 1], [2, 1], [2, 2]], [[5, 0], [10, 1], [7, 1], [2, 1], [3, 2]], [[5, 0], [10, 1], [7, 1], [2, 1], [4, 2]], [[5, 0], [10, 1], [7, 1], [2, 1], [2, 3]], [[5, 0], [10, 1], [7, 1], [2, 1], [3, 3]], [[5, 
0], [10, 1], [7, 1], [0, 2], [3, 1]], [[5, 0], [10, 1], [7, 1], [0, 2], [4, 1]], [[5, 0], [10, 1], [7, 1], [0, 2], [2, 2]], [[5, 0], [10, 1], [7, 1], [0, 2], [3, 2]], [[5, 0], [10, 1], [7, 1], [0, 2], 
[4, 2]], [[5, 0], [10, 1], [7, 1], [0, 2], [2, 3]], [[5, 0], [10, 1], [7, 1], [0, 2], [3, 3]], [[5, 0], [10, 1], [7, 1], [1, 2], [3, 1]], [[5, 0], [10, 1], [7, 1], [1, 2], [4, 1]], [[5, 0], [10, 1], [7, 1], [1, 2], [2, 2]], [[5, 0], [10, 1], [7, 1], [1, 2], [3, 2]], [[5, 0], [10, 1], [7, 1], [1, 2], [4, 2]], [[5, 0], [10, 1], [7, 1], [1, 2], [2, 3]], [[5, 0], [10, 1], [7, 1], [1, 2], [3, 3]], [[5, 0], [10, 1], [8, 1], [1, 0], [3, 1]], [[5, 0], [10, 1], [8, 1], [1, 0], [4, 1]], [[5, 0], [10, 1], [8, 1], [1, 0], [2, 2]], [[5, 0], [10, 1], [8, 1], [1, 0], [3, 2]], [[5, 0], [10, 1], [8, 1], [1, 0], [4, 2]], [[5, 0], [10, 1], [8, 1], [1, 0], [2, 3]], [[5, 0], [10, 1], [8, 1], [1, 0], [3, 3]], [[5, 0], [10, 1], [8, 1], [2, 0], [3, 1]], [[5, 0], [10, 1], [8, 1], [2, 0], [4, 1]], [[5, 0], [10, 1], [8, 1], [2, 0], [2, 2]], [[5, 0], [10, 1], [8, 1], [2, 0], [3, 2]], [[5, 0], [10, 1], [8, 1], [2, 0], [4, 2]], [[5, 0], [10, 1], [8, 1], [2, 0], [2, 3]], [[5, 0], [10, 1], [8, 1], [2, 0], [3, 3]], [[5, 0], [10, 1], [8, 1], [0, 1], [3, 1]], [[5, 0], [10, 1], [8, 1], [0, 1], [4, 1]], [[5, 0], [10, 1], [8, 1], [0, 1], [2, 2]], [[5, 0], [10, 1], [8, 1], [0, 1], [3, 2]], [[5, 0], [10, 1], [8, 1], [0, 1], [4, 2]], [[5, 0], [10, 1], [8, 1], [0, 1], [2, 3]], [[5, 0], [10, 1], [8, 1], [0, 1], [3, 3]], [[5, 0], [10, 1], [8, 1], [1, 1], [3, 1]], [[5, 0], [10, 1], [8, 1], [1, 1], [4, 1]], [[5, 0], [10, 1], [8, 
1], [1, 1], [2, 2]], [[5, 0], [10, 1], [8, 1], [1, 1], [3, 2]], [[5, 0], [10, 1], [8, 1], [1, 1], [4, 2]], [[5, 0], [10, 1], [8, 1], [1, 1], [2, 3]], [[5, 0], [10, 1], [8, 1], [1, 1], [3, 3]], [[5, 0], [10, 1], [8, 1], [2, 1], [3, 1]], [[5, 0], [10, 1], [8, 1], [2, 1], [4, 1]], [[5, 0], [10, 1], [8, 1], [2, 1], [2, 2]], [[5, 0], [10, 1], [8, 1], [2, 1], [3, 2]], [[5, 0], [10, 1], [8, 1], [2, 1], [4, 2]], [[5, 0], [10, 1], [8, 1], [2, 1], [2, 3]], [[5, 0], [10, 1], [8, 1], [2, 1], [3, 3]], [[5, 0], [10, 1], [8, 1], [0, 2], [3, 1]], [[5, 0], [10, 1], [8, 1], [0, 2], [4, 1]], [[5, 0], [10, 1], [8, 1], [0, 2], [2, 2]], [[5, 0], [10, 1], [8, 1], [0, 2], [3, 2]], [[5, 0], [10, 1], [8, 1], [0, 2], [4, 2]], [[5, 0], [10, 1], [8, 1], [0, 2], [2, 3]], [[5, 0], [10, 1], [8, 1], [0, 2], [3, 3]], [[5, 0], 
[10, 1], [8, 1], [1, 2], [3, 1]], [[5, 0], [10, 1], [8, 1], [1, 2], [4, 1]], [[5, 0], [10, 1], [8, 1], [1, 2], [2, 2]], [[5, 0], [10, 1], [8, 1], [1, 2], [3, 2]], [[5, 0], [10, 1], [8, 1], [1, 2], [4, 
2]], [[5, 0], [10, 1], [8, 1], [1, 2], [2, 3]], [[5, 0], [10, 1], [8, 1], [1, 2], [3, 3]], [[5, 0], [10, 1], [7, 2], [1, 0], [3, 1]], [[5, 0], [10, 1], [7, 2], [1, 0], [4, 1]], [[5, 0], [10, 1], [7, 2], [1, 0], [2, 2]], [[5, 0], [10, 1], [7, 2], [1, 0], [3, 2]], [[5, 0], [10, 1], [7, 2], [1, 0], [4, 2]], [[5, 0], [10, 1], [7, 2], [1, 0], [2, 3]], [[5, 0], [10, 1], [7, 2], [1, 0], [3, 3]], [[5, 0], [10, 1], [7, 2], [2, 0], [3, 1]], [[5, 0], [10, 1], [7, 2], [2, 0], [4, 1]], [[5, 0], [10, 1], [7, 2], [2, 0], [2, 2]], [[5, 0], [10, 1], [7, 2], [2, 0], [3, 2]], [[5, 0], [10, 1], [7, 2], [2, 0], [4, 2]], [[5, 0], [10, 1], [7, 2], [2, 0], [2, 3]], [[5, 0], [10, 1], [7, 2], [2, 0], [3, 3]], [[5, 0], [10, 1], [7, 2], [0, 1], [3, 1]], [[5, 0], [10, 1], [7, 2], [0, 1], [4, 1]], [[5, 0], [10, 1], [7, 2], [0, 1], [2, 2]], [[5, 0], [10, 1], [7, 2], [0, 1], [3, 2]], [[5, 0], [10, 1], [7, 2], [0, 1], [4, 2]], [[5, 0], [10, 1], [7, 2], [0, 1], [2, 3]], [[5, 0], [10, 1], [7, 2], [0, 1], [3, 3]], [[5, 0], [10, 1], [7, 2], [1, 1], [3, 1]], [[5, 0], [10, 1], [7, 2], [1, 1], [4, 1]], [[5, 0], [10, 1], [7, 2], [1, 1], [2, 2]], [[5, 0], [10, 1], [7, 2], [1, 1], [3, 2]], [[5, 0], [10, 1], [7, 2], [1, 1], [4, 2]], [[5, 0], [10, 1], [7, 2], [1, 1], [2, 3]], [[5, 0], [10, 1], [7, 2], [1, 1], [3, 3]], [[5, 0], [10, 1], [7, 2], [2, 1], [3, 1]], [[5, 0], [10, 1], [7, 2], [2, 1], [4, 1]], [[5, 0], [10, 1], [7, 2], 
[2, 1], [2, 2]], [[5, 0], [10, 1], [7, 2], [2, 1], [3, 2]], [[5, 0], [10, 1], [7, 2], [2, 1], [4, 2]], [[5, 0], [10, 1], [7, 2], [2, 1], [2, 3]], [[5, 0], [10, 1], [7, 2], [2, 1], [3, 3]], [[5, 0], [10, 1], [7, 2], [0, 2], [3, 1]], [[5, 0], [10, 1], [7, 2], [0, 2], [4, 1]], [[5, 0], [10, 1], [7, 2], [0, 2], [2, 2]], [[5, 0], [10, 1], [7, 2], [0, 2], [3, 2]], [[5, 0], [10, 1], [7, 2], [0, 2], [4, 2]], [[5, 0], [10, 1], [7, 2], [0, 2], [2, 3]], [[5, 0], [10, 1], [7, 2], [0, 2], [3, 3]], [[5, 0], [10, 1], [7, 2], [1, 2], [3, 1]], [[5, 0], [10, 1], [7, 2], [1, 2], [4, 1]], [[5, 0], [10, 1], [7, 2], [1, 2], [2, 2]], [[5, 0], [10, 1], [7, 2], [1, 2], [3, 2]], [[5, 0], [10, 1], [7, 2], [1, 2], [4, 2]], [[5, 0], [10, 1], [7, 2], [1, 2], [2, 3]], [[5, 0], [10, 1], [7, 2], [1, 2], [3, 3]], [[5, 0], [11, 1], [8, 0], [1, 0], [3, 1]], [[5, 0], [11, 1], [8, 0], [1, 0], [4, 1]], [[5, 0], [11, 1], [8, 0], [1, 0], [2, 2]], [[5, 0], [11, 1], [8, 0], [1, 0], [3, 2]], [[5, 0], [11, 1], [8, 0], [1, 0], [4, 2]], [[5, 0], [11, 1], [8, 0], [1, 0], [2, 3]], [[5, 0], [11, 1], [8, 0], [1, 0], [3, 3]], [[5, 0], [11, 1], [8, 0], [2, 0], [3, 1]], [[5, 0], [11, 1], [8, 0], [2, 0], [4, 1]], [[5, 0], [11, 1], [8, 0], [2, 0], [2, 2]], [[5, 0], [11, 1], [8, 0], [2, 0], [3, 2]], [[5, 0], [11, 1], [8, 0], [2, 0], [4, 2]], [[5, 0], [11, 1], [8, 0], [2, 0], [2, 3]], [[5, 0], [11, 1], [8, 0], [2, 0], [3, 3]], [[5, 0], [11, 
1], [8, 0], [0, 1], [3, 1]], [[5, 0], [11, 1], [8, 0], [0, 1], [4, 1]], [[5, 0], [11, 1], [8, 0], [0, 1], [2, 2]], [[5, 0], [11, 1], [8, 0], [0, 1], [3, 2]], [[5, 0], [11, 1], [8, 0], [0, 1], [4, 2]], 
[[5, 0], [11, 1], [8, 0], [0, 1], [2, 3]], [[5, 0], [11, 1], [8, 0], [0, 1], [3, 3]], [[5, 0], [11, 1], [8, 0], [1, 1], [3, 1]], [[5, 0], [11, 1], [8, 0], [1, 1], [4, 1]], [[5, 0], [11, 1], [8, 0], [1, 1], [2, 2]], [[5, 0], [11, 1], [8, 0], [1, 1], [3, 2]], [[5, 0], [11, 1], [8, 0], [1, 1], [4, 2]], [[5, 0], [11, 1], [8, 0], [1, 1], [2, 3]], [[5, 0], [11, 1], [8, 0], [1, 1], [3, 3]], [[5, 0], [11, 1], [8, 0], [2, 1], [3, 1]], [[5, 0], [11, 1], [8, 0], [2, 1], [4, 1]], [[5, 0], [11, 1], [8, 0], [2, 1], [2, 2]], [[5, 0], [11, 1], [8, 0], [2, 1], [3, 2]], [[5, 0], [11, 1], [8, 0], [2, 1], [4, 2]], [[5, 0], [11, 1], [8, 0], [2, 1], [2, 3]], [[5, 0], [11, 1], [8, 0], [2, 1], [3, 3]], [[5, 0], [11, 1], [8, 0], [0, 2], [3, 1]], [[5, 0], [11, 1], [8, 0], [0, 2], [4, 1]], [[5, 0], [11, 1], [8, 0], [0, 
2], [2, 2]], [[5, 0], [11, 1], [8, 0], [0, 2], [3, 2]],[[10,1],[12,1],[9,1],[11,1],[0,1]], [[5, 0], [11, 1], [8, 0], [0, 2], [4, 2]], [[5, 0], [11, 1], [8, 0], [0, 2], [2, 3]], [[5, 0], [11, 1], [8, 0], [0, 2], [3, 3]], [[5, 0], [11, 1], [8, 0], [1, 2], [3, 1]], [[5, 0], [11, 1], [8, 0], [1, 2], [4, 1]], [[5, 0], [11, 1], [8, 0], [1, 2], [2, 2]], [[5, 0], [11, 1], [8, 0], [1, 2], [3, 2]], [[5, 0], [11, 1], [8, 0], [1, 2], [4, 2]], [[5, 0], [11, 1], [8, 0], [1, 2], [2, 3]], [[5, 0], [11, 1], [8, 0], [1, 2], [3, 3]], [[5, 0], [11, 1], [7, 1], [1, 0], [3, 1]], [[5, 0], [11, 1], [7, 1], [1, 0], [4, 1]], [[5, 0], [11, 1], [7, 1], [1, 0], [2, 2]], [[5, 0], [11, 1], [7, 1], [1, 0], [3, 2]], [[5, 0], [11, 1], [7, 1], [1, 0], [4, 2]], [[5, 0], [11, 1], [7, 1], [1, 0], [2, 3]], [[5, 0], [11, 1], [7, 1], [1, 0], [3, 3]], [[5, 0], [11, 1], [7, 1], [2, 0], [3, 1]], [[5, 0], [11, 1], [7, 1], [2, 0], [4, 1]], [[5, 0], [11, 1], [7, 1], [2, 0], [2, 2]], [[5, 0], [11, 1], [7, 1], [2, 0], [3, 2]], [[5, 0], [11, 1], [7, 1], [2, 0], [4, 2]], [[5, 0], [11, 1], [7, 1], [2, 0], [2, 3]], [[5, 0], [11, 1], [7, 1], [2, 0], [3, 3]], [[5, 0], [11, 1], [7, 1], [0, 1], [3, 1]], [[5, 0], [11, 1], [7, 1], [0, 1], [4, 1]], [[5, 0], [11, 1], [7, 1], [0, 1], [2, 2]], [[5, 0], [11, 1], [7, 1], [0, 1], [3, 2]], [[5, 0], [11, 1], [7, 1], [0, 1], [4, 2]], [[5, 0], [11, 1], [7, 1], [0, 1], [2, 3]], [[5, 0], [11, 1], [7, 1], [0, 1], [3, 3]], [[5, 0], [11, 1], 
[7, 1], [1, 1], [3, 1]], [[5, 0], [11, 1], [7, 1], [1, 1], [4, 1]], [[5, 0], [11, 1], [7, 1], [1, 1], [2, 2]], [[5, 0], [11, 1], [7, 1], [1, 1], [3, 2]], [[5, 0], [11, 1], [7, 1], [1, 1], [4, 2]], [[5, 0], [11, 1], [7, 1], [1, 1], [2, 3]], [[5, 0], [11, 1], [7, 1], [1, 1], [3, 3]], [[5, 0], [11, 1], [7, 1], [2, 1], [3, 1]], [[5, 0], [11, 1], [7, 1], [2, 1], [4, 1]], [[5, 0], [11, 1], [7, 1], [2, 1], [2, 2]], [[5, 0], [11, 1], [7, 1], [2, 1], [3, 2]], [[5, 0], [11, 1], [7, 1], [2, 1], [4, 2]], [[5, 0], [11, 1], [7, 1], [2, 1], [2, 3]], [[5, 0], [11, 1], [7, 1], [2, 1], [3, 3]], [[5, 0], [11, 1], [7, 1], [0, 2], [3, 1]], [[5, 0], [11, 1], [7, 1], [0, 2], [4, 1]], [[5, 0], [11, 1], [7, 1], [0, 2], [2, 2]], [[5, 0], [11, 1], [7, 1], [0, 2], [3, 2]], [[5, 0], [11, 1], [7, 1], [0, 2], [4, 2]], [[5, 
0], [11, 1], [7, 1], [0, 2], [2, 3]], [[5, 0], [11, 1], [7, 1], [0, 2], [3, 3]], [[5, 0], [11, 1], [7, 1], [1, 2], [3, 1]], [[5, 0], [11, 1], [7, 1], [1, 2], [4, 1]], [[5, 0], [11, 1], [7, 1], [1, 2], 
[2, 2]], [[5, 0], [11, 1], [7, 1], [1, 2], [3, 2]], [[5, 0], [11, 1], [7, 1], [1, 2], [4, 2]], [[5, 0], [11, 1], [7, 1], [1, 2], [2, 3]], [[5, 0], [11, 1], [7, 1], [1, 2], [3, 3]], [[5, 0], [11, 1], [8, 1], [1, 0], [3, 1]], [[5, 0], [11, 1], [8, 1], [1, 0], [4, 1]], [[5, 0], [11, 1], [8, 1], [1, 0], [2, 2]], [[5, 0], [11, 1], [8, 1], [1, 0], [3, 2]], [[5, 0], [11, 1], [8, 1], [1, 0], [4, 2]], [[5, 0], [11, 1], [8, 1], [1, 0], [2, 3]], [[5, 0], [11, 1], [8, 1], [1, 0], [3, 3]], [[5, 0], [11, 1], [8, 1], [2, 0], [3, 1]], [[5, 0], [11, 1], [8, 1], [2, 0], [4, 1]], [[5, 0], [11, 1], [8, 1], [2, 0], [2, 2]], [[5, 0], [11, 1], [8, 1], [2, 0], [3, 2]], [[5, 0], [11, 1], [8, 1], [2, 0], [4, 2]], [[5, 0], [11, 1], [8, 1], [2, 0], [2, 3]], [[5, 0], [11, 1], [8, 1], [2, 0], [3, 3]], [[5, 0], [11, 1], [8, 1], [0, 1], [3, 1]], [[5, 0], [11, 1], [8, 1], [0, 1], [4, 1]], [[5, 0], [11, 1], [8, 1], [0, 1], [2, 2]], [[5, 0], [11, 1], [8, 1], [0, 1], [3, 2]], [[5, 0], [11, 1], [8, 1], [0, 1], [4, 2]], [[5, 0], [11, 1], [8, 1], [0, 1], [2, 3]], [[5, 0], [11, 1], [8, 1], [0, 1], [3, 3]], [[5, 0], [11, 1], [8, 1], [1, 1], [3, 1]], [[5, 0], [11, 1], [8, 1], [1, 1], [4, 1]], [[5, 0], [11, 1], [8, 1], [1, 1], [2, 2]], [[5, 0], [11, 1], [8, 1], [1, 1], [3, 2]], [[5, 0], [11, 1], [8, 1], [1, 1], [4, 2]], [[5, 0], [11, 1], [8, 1], [1, 1], [2, 3]], [[5, 0], [11, 1], [8, 1], [1, 1], [3, 3]], [[5, 0], [11, 1], [8, 
1], [2, 1], [3, 1]], [[5, 0], [11, 1], [8, 1], [2, 1], [4, 1]], [[9,0],[10,0],[12,0],[11,0],[0,0]], [[5, 0], [11, 1], [8, 1], [2, 1], [2, 2]], [[5, 0], [11, 1], [8, 1], [2, 1], [3, 2]], [[5, 0], [11, 1], [8, 1], [2, 1], [4, 2]], [[5, 0], [11, 1], [8, 1], [2, 1], [2, 3]], [[5, 0], [11, 1], [8, 1], [2, 1], [3, 3]], [[5, 0], [11, 1], [8, 1], [0, 2], [3, 1]], [[5, 0], [11, 1], [8, 1], [0, 2], [4, 1]], [[5, 0], [11, 1], [8, 1], [0, 2], [2, 2]], [[5, 0], [11, 1], [8, 1], [0, 2], [3, 2]], [[5, 0], [11, 1], [8, 1], [0, 2], [4, 2]], [[5, 0], [11, 1], [8, 1], [0, 2], [2, 3]], [[5, 0], [11, 1], [8, 1], [0, 2], [3, 3]], [[5, 0], [11, 1], [8, 1], [1, 2], [3, 1]], [[5, 0], [11, 1], [8, 1], [1, 2], [4, 1]], [[5, 0], [11, 1], [8, 1], [1, 2], [2, 2]], [[5, 0], [11, 1], [8, 1], [1, 2], [3, 2]]]"""
    for permutation in permutations:
        position = 0    #Numero de carta siendo analizada
        auxList = []    #Se almacenan los posibles indices para una permutacion en especifico
        #print(permutations)
        #print("Empieza la permutacion : " + str(permutation))
        #permutation = [[9,0],[10,0],[12,0],[11,0],[0,0]]
        for card in permutation:
            #print(card)
            numberCard = card[0]
            rankCard = card[1]
            #possibleIndexList = indexList[position][rankCard][numberCard]
            try:
                possibleIndexList = indexList[position][rankCard][numberCard]
            except:
                print("ERROR en position: " + str(position) + " rank " + str(rankCard) + " card " + str(numberCard))

            if not possibleIndexList:   #Si una carta en una posicion dada no tiene ninguna mano en el archivo, se retorna una lista vacia por default
                auxList = []
                #print("No se encuentran indices para la carta "+ str(card) + " en la posicion " +str(position))
                break

            if(position == 0):          #Si es la carta en la primera posicion, se toman esos indices como los iniciales para comparar las otras cartas
                auxList = possibleIndexList
                #print("Se toman los indices " + str(possibleIndexList) + " de la primera carta " + str(card))

            else:
                #largo = len(auxList)
                i=0
                while i < len(auxList):
                    wormIndex = auxList[i]
                    if not wormIndex in possibleIndexList: #Se revisan los indices que ya se tienen, si alguno no está en la carta que se está analizando
                        #print("Quito los indices: " + str(wormIndex))
                        auxList.remove(wormIndex)     # se elimina de la lista de posibles indices. Así, al final se va a tener una lista de los indices que se repiten
                        #largo -= 1
                        #i -= 1
                        #print(str(wormIndex) + " no esta en " + str(possibleIndexList))
                    #else:
                        #print(str(wormIndex) + " esta en " + str(auxList))

                    i += 1
            position += 1

        if len(auxList) == 1:        #Si se encontró un indice, se guarda junto a su permutacion
            wormIndexList.append((auxList,permutation))
            handPermutations.append(permutation)
            #print (str(auxList) + " : " + str(permutation))

    #print("Termino de buscar indices")
    return wormIndexList, handPermutations


#CREA EL GUSANO
def createWorms(k, luciferin, ratio, indexList2, totalWorms, minRange):
    wormList = []
    #CC = []
    #esto tiene que ser una funcion aparte, no en main
    counter = 0
    wormIndex = minRange
    #totalWorms = 20 #k*25010
    indexListAux = indexList2
    intraDistances = []

    while (counter < totalWorms):
        indexListAux = initSetUp()
        actualWorm = Worm(luciferin,wormIndex)
        #print (actualWorm.position[0])
        actualWorm.getCards(ratio) #obtiene las cartas
        actualWorm.buildPermutations() #le hace todas las permutaciones
        permutations = actualWorm.getPermutations()
        wormIndexList, handPermutations = searchIndex(permutations,indexListAux)
        #print(handPermutations)
        if (wormIndexList!=[]):
            actualWorm.setTotalHands(handPermutations, len(handPermutations))
            #gus= [actualWorm.getTotalHands(), actualWorm]
            #totalHands.append(len(handPermutations)) #aqui le hago set al numero total de manos que tiene un gusano para que sea mas facil sacar los CC
            intraDistance= EQ8(actualWorm)
            actualWorm.setIntraDistance(intraDistance)
            wormList.append(actualWorm)
            wormIndex += 1
            intraDistances.append(intraDistance)
        #actualWorm.setTotalHands(totalHands, len(totalHands))
        #newIntraDistance=EQ8(actualWorm)
        #)
        #intradistance = formula 8"""

        counter+=1

    #searchIndex(wormList[0].permutations,indexList)
    #CC=[]
    wormListAux = wormList.copy()

    #CC = subconjuntoDatos(wormList, ratio) #esto tengo que perfeccionarlo aun
    #print(wormList)
    return wormList, intraDistances, wormListAux



def subconjuntoDatos(wormList, ratio, previousCC):
    #subconjuntoDatos.sort()
    #Ordena la lista de gusanos con respecto a la cantidad de permutaciones de mano que tienen
    for i in range(len(wormList)-1):
        for j in range (0, len(wormList)-i-1):
            if (wormList[j].total > wormList[j+1].total):
                wormList[j], wormList[j+1] = wormList[j+1], wormList[j]
    CC=[]
    counter = 0
    CC.append(wormList[0])
    for i in range (1, len(wormList)):
        if len(CC) == previousCC - 1:
            break
        actualWorm = wormList[i]
        distance = True
        while (counter < len(CC) and distance):
            result = euclidianDistance(CC[counter].position, actualWorm.position)
            if (result<ratio):
                distance = False
            counter += 1
        if (distance):
            CC.append(actualWorm)

    return CC

def findClosestNeighbor(worm,neighborMatrix):
    closestNeighborID = 0
    if worm.identificador == 0:
        closestNeighborID = 1
    for neighborID in range(len(neighborMatrix[worm.identificador])):
        if neighborID != worm.identificador:            #Si no soy yo mismo
            if neighborMatrix[worm.identificador][neighborID] < neighborMatrix[worm.identificador][closestNeighborID]:
                closestNeighborID = neighborID
    return closestNeighborID

def createNeighborMatrix(wormList):
    neighborMatrix = np.ndarray(shape=(len(wormList),len(wormList)), dtype=float)
    numWormLine = 0
    numWormColumn = 0
    for wormLine in wormList:
        numWormColumn = 0
        for wormColumn in wormList:
            print("Analiza gusano " + str(wormLine.identificador) + " contra el gusano " + str(wormColumn.identificador))
            neighborMatrix[numWormLine][numWormColumn] = euclidianDistance(wormLine.position, wormColumn.position)
            print(neighborMatrix[numWormLine][numWormColumn])
            numWormColumn += 1
        numWormLine += 1
    return neighborMatrix

#Toma la matriz de distancias y actualiza las distancias de un gusano en específico
def updateNeighborMatrix(neighborMatrix, wormToUpDate, wormListAux):
    #Actualiza la linea en la matriz correspondiente al gusano
    for wormColumn in range(len(neighborMatrix[wormToUpDate.identificador])):
        newDistance = euclidianDistance(wormToUpDate.position,wormListAux[wormColumn].position)
        if math.isnan(newDistance):
            print("Se cae calculando distancia entre " + str(wormToUpDate.identificador) + " y " + str(wormColumn) +":")
            print(wormToUpDate.position)
            print(wormListAux[wormColumn].position)

        neighborMatrix[wormToUpDate.identificador][wormColumn] = newDistance
        neighborMatrix[wormColumn][wormToUpDate.identificador] = newDistance
    return neighborMatrix




def gso(wormList, m, s, gamma, ratio, luciferin, CC, k, SSE, rho, indexList, intraDistances, neighborMatrix,wormListAux, minRange, maxRange):
    n = 25010
    totalHands = []
    newWormList = []
    if (maxRange>len(wormList)):
        maxRange=len(wormList)
    for i in range (minRange, maxRange):
        indexListAux = initSetUp()
        actualWorm = wormList[i]
        resultado9 = EQ9(n,SSE, actualWorm.intradistance, wormList[i], intraDistances)
        wormList[i].setAdaptation(resultado9)
        wormList[i].setLuciferin(EQ1(wormList[i], rho, gamma, resultado9))
        closestWormID = findClosestNeighbor(wormList[i], neighborMatrix)
        closestWorm = wormListAux[closestWormID]
        wormList[i].setPosition(EQ4(s, wormList[i], closestWorm))
        neighborMatrix = updateNeighborMatrix(neighborMatrix,wormList[i],wormListAux)
        actualWorm.getCards(ratio) #obtiene las cartas
        actualWorm.buildPermutations()
        permutations = actualWorm.getPermutations()
        wormIndexList, handPermutations = searchIndex(permutations,indexListAux)
        if (wormIndexList!=[]):
            actualWorm.setTotalHands(handPermutations, len(handPermutations))
            newWormList.append(actualWorm)
                #gus= [actualWorm.getTotalHands(), actualWorm]
            totalHands.append(len(handPermutations)) #aqui le hago set al numero total de manos que tiene un gusano para que sea mas facil sacar los CC
            intraDistance= EQ8(actualWorm)
            actualWorm.setIntraDistance(intraDistance)
            intraDistances.append(intraDistance)

    wormList = newWormList
    return wormList
        #ESTO LO HACE EL PROCESO 0



def obtenerValoresLineaComandos(argv):
    decLuciferin = ""
    incLuciferin = ""
    distWorms = ""
    valIniLuciferin = ""
    classes = ""
    worms = ""
    try:
        opts, arg = getopt.getopt(argv, "r:g:s:l:k:m:", ["R=", "G=", "S=", "L=", "K=", "M="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-r", "--R"):
            decLuciferin = arg
        elif opt in ("-g", "--G"):
            incLuciferin = arg
        elif opt in ("-s", "--S"):
            distWorms = arg
        elif opt in ("-l", "--L"):
            valIniLuciferin = arg
        elif opt in ("-k", "--K"):
            classes = arg
        elif opt in ("-m", "--M"):
            worms = arg
    return float(decLuciferin), float(incLuciferin), float(distWorms), int(valIniLuciferin), int(classes), float(worms)


def main(argv):
    comm = MPI.COMM_WORLD
    pid = comm.rank
    size = comm.size
    rho = 0
    gamma = 0
    s = 0
    luciferin = 0
    k = 0
    m = 0
    wormList = []
    CC = []
    intraDistances = []
    wormListAux = []
    indexList = []
    SSE = 0
    ratio = 1.5
    totalWorms = 20
    neighborMatrix = [[]]
    if(pid==0):
        rho, gamma, s, luciferin, k, m = obtenerValoresLineaComandos(argv)
        indexList = initSetUp()

    rho, gamma, s, luciferin, k, m, indexList = comm.bcast((rho, gamma, s, luciferin, k, m, indexList),0)
    pidTotalWorms = int(totalWorms/size)
    minRange = int(pid*pidTotalWorms)
    wormList, intraDistances, wormListAux = createWorms(k, luciferin, ratio, indexList, pidTotalWorms, minRange)
    finalWormList = comm.reduce(wormList, op=MPI.SUM)
    finalIntraDistances = comm.reduce(intraDistances, op=MPI.SUM)
    finalWormListAux= comm.reduce(wormListAux, op=MPI.SUM)

    if (pid==0):
        CC = subconjuntoDatos(finalWormList, ratio, 0)
        neighborMatrix = createNeighborMatrix(finalWormListAux)
        SSE = EQ6(CC, k)
        #InterDist = EQ7(k, CC, wormList)
    comm.Barrier()
    finalWormList, finalIntraDistances, finalWormListAux, CC, neighborMatrix, SSE = comm.bcast((finalWormList, finalIntraDistances, finalWormListAux, CC, neighborMatrix, SSE),0)
    minRange = int(pid*len(finalWormList)/size)
    maxRange = int((pid+1)*len(finalWormList)/size)
    comm.Barrier()
    finalWormList = comm.reduce(wormList, op=MPI.SUM)
    contador = 0
    comm.Barrier()
    largoCentroides = len(CC)
    if (pid==0):
        while (largoCentroides>k):
            contador+=1
            if (pid==0):
                finalWormList = gso(finalWormList, m, s, gamma, ratio, luciferin, CC, k, SSE, rho, indexList,
                               finalIntraDistances, neighborMatrix, finalWormListAux, minRange, maxRange)
                CC = subconjuntoDatos(finalWormList, ratio, largoCentroides)
                print("CC al final del ciclo: " + str(contador) + " = " +str(len(CC)))
                largoCentroides = len(CC)
                SSE = EQ6(CC, k)
                interDist = EQ7(k, CC, wormList)
            #CC, SSE,finalWormList = comm.bcast((CC, SSE, finalWormList),0)
            #comm.Barrier()


if __name__ == "__main__":
    main(sys.argv[1:])
