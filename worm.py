import random
import numpy as np


class Worm:
    def __init__(self, luciferin, identificador):
        # EL NIVEL DE LUCIFERINA ES IGUAL A 5,0 PA TODOS
        self.luciferin = luciferin
        self.adaptation = 0  # funcion 9
        posiAux = np.zeros(10)
        contador = 0
        while contador < 10:
            position = round(random.uniform(0, 12), 2)
            posiAux[contador] = position
            contador += 1
            position = round(random.uniform(0, 3), 2)
            posiAux[contador] = position
            contador += 1
        self.position = posiAux  # vector con 10 posiciones aleatoria
        self.permutations = []
        self.dataSet = []  # las cartas que tiene el gusano esto se extrae
        self.intradistance = 0  # sumatoria esto se tiene que calcular por medio de la formuala 8
        self.total = 0  # total de numeros de permutaciones que va a tener el gusano
        self.totalHands = []  #
        self.identificador = identificador

    def getPosition(self):
        return self.position

    def getLuciferin(self):
        return self.luciferin

    def setPosition(self, newPosition):
        self.position = newPosition

    def setCards(self, setCards):
        self.dataSet = setCards
        # self.totalCartas=setTotal

    def setAdaptation(self, newAdaptation):
        self.adaptation = newAdaptation

    def setIntraDistance(self, sum):
        self.intradistance = sum

    def getPermutations(self):
        return self.permutations

    def getTotalHands(self):
        return self.total

    def setTotalHands(self, newHands, newTotal):
        self.totalHands = newHands
        self.total = newTotal

    def setLuciferin(self, newLuciferin):
        self.luciferin = newLuciferin

    # Funcion que toma la propiedad dataSet y crea permutaciones de todas las cartas en el radio del gusano. Estas permutaciones respetan la
    # posicion original de las cartas encontradas
    # Retorna None si se encuentra que el gusano no econtro en su radio ninguna carta en alguna posicion
    def buildPermutations(self):
        for firstCard in self.dataSet[0]:
            for secondCard in self.dataSet[1]:
                for thirdCard in self.dataSet[2]:
                    for fourthCard in self.dataSet[3]:
                        for fifthCard in self.dataSet[4]:
                            permutation = [firstCard, secondCard, thirdCard, fourthCard, fifthCard]
                            if [] in permutation:
                                return None

                            self.permutations.append(permutation)
                            # print(self.permutations)"""

    # AGREGAR CUADNO RS SEA IGUAL A 1,5
    # Hacer un set para las cartas y la intra distancia
    # hacer un get pa las posiciones
    def getCards(self, ratio):
        # print("entro a getCards")
        contador = 0
        index = 0
        cardSet = []
        # finalCardSet = []
        # print(self.position)
        while (contador < 5):
            cardSet = []
            limitMax1 = int(self.position[index] + ratio)
            limiteMin1 = int(self.position[index] - ratio)
            limitMax2 = int(self.position[index + 1] + ratio)
            limiteMin2 = int(self.position[index + 1] - ratio)
            for i in range(4):
                for j in range(13):
                    if (j <= limitMax1 and j >= 0 and j >= limiteMin1 and (i != limiteMin2 or j != limiteMin1)):
                        if (i <= limitMax2 and i >= 0 and i >= limiteMin2 and (i != limitMax2 or j != limitMax1)):
                            card = [j, i]
                            if (card not in cardSet):
                                cardSet.append(card)
            index += 2
            contador += 1
            self.dataSet.append(cardSet)
            # finalCardSet.append(cardSet)
        # return finalCardSet

