import math
import numpy

#Calcula la distancia euclidiana entre dos puntos de n dimensiones. Recibe dos listas y retorna un entero
def euclidianDistance(pointA,pointB):
    assert len(pointA) == len(pointB)

    summation = 0
    for axisA, axisB in zip(pointA,pointB):
        summation += (axisB-axisA) ** 2

    return math.sqrt(summation)

#Funcion que determina el nivel de Luciferina. Recibe:
#- t: Iteracion?
#- rho: Constante recibida por consola. Default 0.4
#- gamma: Constante recibida por consola. Default 0.6


def EQ1(gusano, rho, gamma, resultadoEQ9):
    F = resultadoEQ9
    return (1-rho) * gusano.getLuciferin() + gamma * F

def EQ2(listaGusanos, gusanoActual, r, rho, gamma, resultadoEQ9):
    gusanosVecinos = []
    resultadoEcuacion1 = EQ1(gusanoActual, rho, gamma, resultadoEQ9)
    for index in range(len(listaGusanos)):
        if (gusanoActual != index):
            distance = euclidianDistance(listaGusanos[index].getPosition(), listaGusanos[gusanoActual].getPosition())
            resultadoEQ1 = EQ1(index, rho, gamma, resultadoEQ9)
            if (distance < r and resultadoEQ1 > resultadoEcuacion1):
                gusanosVecinos.append(index)

    return gusanosVecinos


def EQ3(j,z, listaGusanos, rho, gamma, resultadoEQ9):
    sumatoria=0
    resultado = EQ2(listaGusanos, j, z, rho, gamma, resultadoEQ9)
    for k in range in resultado:
        sumatoria = sumatoria + EQ2(listaGusanos, j, z, rho, gamma, resultadoEQ9)*(EQ1(k, rho, gamma, resultadoEQ9)-EQ1(j, rho, gamma, resultadoEQ9))
    resultado= (EQ1(z, rho, gamma, resultadoEQ9)-EQ1(j, rho, gamma, resultadoEQ9))/sumatoria
    return resultado


def EQ4(s, gusanitos, gusanoActual, gusanoVecino):
    contador = 0
    newPositions = np.zeros(10)
    posicionAnt = [gusanitos[gusanoVecino].position[contador]]
    posicionAnt2 = [gusanitos[gusanoActual].position[contador]]
    while (contador < 10):
        resultadoDivision = 0
        resultadoResta = gusanitos[gusanoVecino].position[contador] - gusanitos[gusanoActual].position[contador]
        distancia = euclidianDistance(posicionAnt, posicionAnt2)
        resultadoDivision = s * (resultadoResta/distancia)
        newPositions[contador] = gusanitos[gusanoActual].position[contador] + resultadoDivision
        contador+=1
    gusanitos[gusanoActual].setPosition(newPositions)

def EQ6(listaCentroides, k):
    sumFinal = 0
    sum = 0 
    for index in range (k):
        for i in range (len(listaCentroides[index].getPermutations())):
            permutation = listaCentroides[index].getPermutations()
            sum = sum + (euclidianDistance(listaCentroides[index].getPosition(), permutation[i] ))
        sumFinal = sumFinal + sum
    return sumFinal


def EQ7(k, CC, gusanitos):
    resultado = 0
    sumatoriaI=0
    sumatoriaJ=0
    for i in range (1, k):
        for j in range (1,k):
            sumatoriaJ = sumatoriaJ + (euclidianDistance(gusanitos[CC[i]].position, gusanitos[CC[j]].position)**2)
        sumatoriaI = sumatoriaI + sumatoriaJ
    resultado = sumatoriaI
    return resultado

def EQ8(worm):
    intraD = 0
    for permutation in worm.permutations:
        intraD += euclidianDistance(permutation,worm.position)
    return intraD

