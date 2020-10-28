import math
import numpy as np

#Ecuacion que calcula la distancia euclidiana entre dos vectores de un mismo tamaño.
#Recibe dos vectores y retorn un float
def euclidianDistance(pointA, pointB):
    assert len(pointA) == len(pointB)

    summation = 0
    for axisA, axisB in zip(pointA, pointB):
        summation += (axisB - axisA) ** 2

    return math.sqrt(summation)


def EQ1(worm, rho, gamma, resultEQ9):
    F = resultEQ9
    return ((1 - rho) * worm.luciferin) + (gamma * F)


def EQ2(wormList, actualWorm, ratio):
    neighborsSet = []
    for index in range(len(wormList)):
        distance = euclidianDistance(wormList[index].position, actualWorm.position)
        # print(wormList[index].luciferin )
        # print(actualWorm.luciferin)
        if (distance < ratio and wormList[index].luciferin > actualWorm.luciferin):
            neighborsSet.append(wormList[index])
            # print(distance)

    return neighborsSet


def EQ3(actualWorm, wormList, neighborsSet):
    sum = 0
    maxProbability = 0
    selectedWorm = actualWorm
    # selectedWorm = neighborsSet[0]
    for k in range(len(neighborsSet)):
        resultDifferece = neighborsSet[k].getLuciferin() - actualWorm.getLuciferin()
        for i in range(len(neighborsSet)):
            result = neighborsSet[i].getLuciferin() - actualWorm.getLuciferin()
            sum = sum + result
        finalResult = resultDifferece / sum
        if (finalResult > maxProbability):
            maxProbability = finalResult
            selectedWorm = neighborsSet[k]
    return selectedWorm


def EQ4(s, actualWorm, bestNeighbor):
    contador = 0
    newPositions = np.zeros(10)
    distancia = euclidianDistance(actualWorm.position, bestNeighbor.position)
    while (contador < 10):
        resultadoResta = bestNeighbor.position[contador] - actualWorm.position[contador]
        # print(resultadoResta)
        resultadoDivision = s * (resultadoResta / distancia)
        newPositions[contador] = actualWorm.position[contador] + resultadoDivision
        contador += 1
    # print(newPositions)
    return newPositions


def EQ6(centroidsList, k):
    sumCentroid = 0
    sum = 0
    finalSum = 0
    # print(centroidsList)
    # print(centroidsList[0].totalHands)
    for index in range(len(centroidsList)):
        for permutation in (centroidsList[index].totalHands):
            x = 0
            for card in permutation:
                posicion = []
                # permutation = centroidsList[index].totalHands
                posicion.append(centroidsList[index].position[x])
                x += 1
                posicion.append(centroidsList[index].position[x])
                x += 1

                sum = sum + ((euclidianDistance(posicion, card)) ** 2)
            sumCentroid = sumCentroid + sum
        finalSum = finalSum + sumCentroid

    return finalSum


def EQ7(k, centroidsList, wormList):
    result = 0
    sumI = 0
    sumJ = 0
    for i in range(len(centroidsList)):
        for j in range(len(centroidsList)):
            sumJ = sumJ + (euclidianDistance(centroidsList[i].position, centroidsList[j].position) ** 2)
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
            # permutation = centroidsList[index].totalHands
            posicion.append(worm.position[x])
            x += 1
            posicion.append(worm.position[x])
            x += 1
            intraD += euclidianDistance(card, posicion)
        finalIntraD += finalIntraD + intraD
    return finalIntraD


def EQ9(n, resultEQ6, resultEQ8, actualWorm, intraDistances):
    result1 = (1 / n) * actualWorm.total
    resultMultiplication = resultEQ6 * (resultEQ8 / max(intraDistances))
    result = result1 / resultMultiplication
    # print(result)
    return result


