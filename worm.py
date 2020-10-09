import random
import numpy as np
import itertools

class Worm:
    luciferin = 0
    adaptation = 0

    def __init__(self, luciferin):
        #EL NIVEL DE LUCIFERINA ES IGUAL A 5,0 PA TODOS
        self.luciferin = luciferin
        self.adaptation = 0 #funcion 9
        self.dataSet = [] #las cartas que tiene el gusano esto se extrae
        self.intradistance = 0 #sumatoria esto se tiene que calcular por medio de la formuala 8
        self.totalCartas=0
        self.permutations = []
        #Genera una posicion aleatoria de 10 dimensiones
        posiAux=np.zeros(10)
        contador=0
        while contador<10:
            position = round(random.uniform(1, 13), 2)
            posiAux[contador]=position
            contador+=1
            position = round(random.uniform(1, 4), 2)
            posiAux[contador]= position
            contador+=1
        self.position = posiAux #vector con 10 posiciones aleatoria

    def getPosition(self):
        return self.position

    def setCards(self, setCards, setTotal):
        self.dataSet=setCards
        self.totalCartas=setTotal
    
    def setAdaptation(self, newAdaptation):
        self.adaptation = newAdaptation

    def setIntraDistance(self, sum):
        self.intradistance = sum

    #Funcion que toma la propiedad dataSet y crea permutaciones de todas las cartas en el radio del gusano. Estas permutaciones respetan la
    #posicion original de las cartas encontradas
    #Retorna None si se encuentra que el gusano no econtro en su radio ninguna carta en alguna posicion
    def buildPermutations(self):
        for firstCard in self.dataSet[0]:
            for secondCard in self.dataSet[1]:
                for thirdCard in self.dataSet[2]:
                    for fourthCard in self.dataSet[3]:
                        for fifthCard in self.dataSet[4]:
                            permutation = [firstCard,secondCard,thirdCard,fourthCard,fifthCard]
                            if [] in permutation:
                                return None
                            print(permutation)
                            self.permutations.append(permutation)

    def getCards(self, positions, ratio):
        contador=0
        index = 0
        total = 0
        cardSet = []
        cartita= []
        while (contador<5):
            card = [0,0]
            
            cardSet= []
            resultado1 = (positions[index] - int(positions[index]))
            resultado1=round(resultado1, 2)

            if (resultado1 <= ratio):
                card[0]=(int(positions[index])+1)
                card[1]=int(positions[index+1])
                cardSet.append(card)
                #print(card)
                total+=1
                
            card = [0,0]
            resultado1 = int(positions[index] + ratio)
            #resultado1=round(resultado1, 2)
            #print(positions[index])
            #print(int(positions[index]))
            #print(resultado1)
            if (resultado1 > int(positions[index])):
                card[0]=int((positions[index])+2)
                card[1]=int(positions[index+1])
                cardSet.append(card)
                total+=1
                #print(positions[index])
                #print(int(positions[index]))
                #print(resultado1)
            index+=1
            card = [0,0]
            resultado1 = positions[index] - int(positions[index])
            resultado1=round(resultado1, 2)
            if (resultado1 <= ratio and int((positions[index])-1)>0):
                card[0]=int((positions[index-1])+1)
                card[1]=int((positions[index])-1)
                cardSet.append(card)
                total+=1
                #print(card)
                #print(positions[index])
                #print(int(positions[index]))
                #print(resultado1)
            resultado1 = int(positions[index] + ratio)
            #resultado1=round(resultado1, 2)
            card = [0,0]
            if (resultado1 > int(positions[index]) and int((positions[index])-1)<5):
                card[0]=int(positions[index-1])+1
                card[1]=int(positions[index])+1
                cardSet.append(card)
                total+=1
            index+=1
            contador+=1
            #print(contador)
            cartita.append(cardSet)
        #print(cartita)
        #print(total)
        return cartita, total
"""      
    def __str__(self):
        return (f"Worm:"
            f"Coordinates: {self.coordinates}"
            f"Luciferin: {self.luciferin}"
            f"Adaptation (F): {self.adaptation}"
            f"Covered data set: {self.coveredSet}"
            f"Intradistance: {self.intradistance}")
"""
