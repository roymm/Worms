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
def EQ1(t,rho,gamma):
    F = EQ9(t)
    return (1-rho) * EQ1(t-1,rho,gamma) + gamma * F

#Fucnion que calcula el valor de adaptacion
def EQ9(t):
    return


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

def EQ3(j,z):
    sumatoria=0
    resultado = EQ2(j)
    for k in range (resultado):
        sumatoria = sumatoria + EQ2(j)*(EQ1(k)-EQ1(j))
    resultado= (EQ1(z)-EQ1(j))/sumatoria
    return resultado