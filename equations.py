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