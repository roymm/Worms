import math
import numpy

#Calcula la distancia euclidiana entre dos puntos de n dimensiones. Recibe dos listas y retorna un entero
def euclidianDistance(pointA,pointB):
    assert len(pointA) == len(pointB)

    summation = 0
    for axisA, axisB in zip(pointA,pointB):
        summation += (axisB-axisA) ** 2

    return math.sqrt(summation)

