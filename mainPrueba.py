from gusanosPrueba import Worm
import numpy as np
import math


def euclidianDistance(pointA,pointB):
    assert len(pointA) == len(pointB)

    summation = 0
    for axisA, axisB in zip(pointA,pointB):
        summation += (axisB-axisA) ** 2

    return math.sqrt(summation)

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
    for permutation in worm.permutationsAux:
        intraD += euclidianDistance(permutation,worm.position)
    return intraD

def EQ9(k, n, total, resultado6, resultado7):
    resultado =0

    return resultado


#Funcion que crea los gusanos iniciales y hace otras cosas del inicio que todavia no sabemos
def initSetUp():
    #global testHands
    #global allCards
    #global indexList 
    #Creacion de universo con una matriz de 13 (cartas) * 4 (palos) * 5 cartas en la mano
    #if(pid == 0):
    testHands = []
    indexList = []
    allCards = np.resize(np.arange(13),(5,4,13))
        
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
    for line in open('poker-hand-training-true.data'):
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
    return testHands, indexList #LES HICE RETURN PORQUE CON EL GLOBAL NO ME CORRIA


#Funcion que toma una lista de listas (la propiedad dataSet de los gusanos) y relaciona cada carta con su posicion 
# a una mano del archivo poker-hand-training-true.data
# Recibe una lista de pares [numero de carta, palo] y retorna una lista de enteros (indices del array testHands)
def searchIndex(permutations, indexList):
    wormIndexList = []
    print(str(len(permutations)))
    for permutation in permutations:
        position = 0    #Numero de carta siendo analizada
        auxList = []    #Se almacenan los posibles indices para una permutacion en especifico
        print("Empieza la permutacion : " + str(permutation))
        permutation = [[9,0],[10,0],[12,0],[11,0],[0,0]]
        for card in permutation:
            #print(card)
            numberCard = card[0]
            rankCard = card[1]
            try:
                possibleIndexList = indexList[position][rankCard][numberCard]
            except:
                print("ERROR en position: " + str(position) + " rank " + str(rankCard) + " card " + str(numberCard))

            if not possibleIndexList:   #Si una carta en una posicion dada no tiene ninguna mano en el archivo, se retorna una lista vacia por default
                auxList = []
                print("No se encuentran indices para la carta "+ str(card) + " en la posicion " +str(position))
                break

            if(position == 0):          #Si es la carta en la primera posicion, se toman esos indices como los iniciales para comparar las otras cartas
                auxList = possibleIndexList
                #print("Se toman los indices " + str(possibleIndexList) + " de la primera carta " + str(card))

            else:
                largo = len(auxList)
                i=0
                while i < largo:
                    wormIndex = auxList[i]
                    if not wormIndex in possibleIndexList: #Se revisan los indices que ya se tienen, si alguno no está en la carta que se está analizando
                        #print("Quito los indices: " + str(wormIndex))
                        auxList.remove(wormIndex)     # se elimina de la lista de posibles indices. Así, al final se va a tener una lista de los indices que se repiten
                        largo -= 1
                        i -= 1
                        #print(str(wormIndex) + " no esta en " + str(possibleIndexList))
                    #else:
                        #print(str(wormIndex) + " esta en " + str(auxList))

                    i += 1
            position += 1
        
        if len(auxList) == 1:        #Si se encontró un indice, se guarda junto a su permutacion
            wormIndexList.append((auxList,permutation))
            print (str(auxList) + " : " + str(permutation))
    
    #print("Termino de buscar indices")
    return wormIndexList


#CREA EL GUSANO
def createWorms(k, luciferin, ratio, indexList):
    wormList = []
    totalHands = []
    #esto tiene que ser una funcion aparte, no en main
    counter = 0
    totalWorms = 5 #k*25010
    while (counter < totalWorms):
        actualWorm = Worm(luciferin)
        cards = actualWorm.getCards(ratio) #obtiene las cartas
        #print(cards)
        #print (totalCards)
        actualWorm.setCards(cards) 
        #print(cards)
        actualWorm.buildPermutations() #le hace todas las permutaciones
        permutations = actualWorm.getPermutations()
        #print(permutations)

        
        #totalHands = searchIndex(permutations, indexList) #no se si los indices que devuelve son igual a la cantidad de manos que tiene el gusano con respecto al archivo de manos
        
        actualWorm.setTotalHands(totalHands, len(totalHands)) 

        wormList.append(actualWorm)

        #newIntraDistance=EQ8(actualWorm)
        totalHands.append(actualWorm.getTotalHands()) #aqui le hago set al numero total de manos que tiene un gusano para que sea mas facil sacar los CC
        actualWorm.setIntraDistance(EQ8(actualWorm))
        #intradistance = formula 8
        counter+=1
    
    searchIndex(wormList[0].permutations,indexList)
    CC=[]
    #CC = subconjuntoDatos(k, totalHands, wormList, ratio) #esto tengo que perfeccionarlo aun
    return wormList, CC



def subconjuntoDatos(k, subconjuntoDatos, wormList, ratio):
    #subconjuntoDatos.sort()
    CC=[]
    contador=0
    #contador2=0
    aux = 0
    while (contador<k):
        max = subconjuntoDatos[0]
        for index in range(len(subconjuntoDatos)):
            if (subconjuntoDatos[index]>=max and index not in CC):
                #if (len(CC)==0):
                max = subconjuntoDatos[index]
                aux = index 
                #else:
                    #if (distanceCentroids(wormList, CC, index, ratio)):
                    #    max = subconjuntoDatos[index]
                    #    aux = index 
            max = subconjuntoDatos[0]       
        CC.append(aux)
        contador+=1
    return CC


def distanceCentroids(wormList, CC, actualWorm, ratio): #esta funcion aun no sirve
    rightDistance = False
    distance = 0
    for index in range (len(CC)):
        if (CC[index] != actualWorm):
            #print (CC[index])
            #distance = euclidianDistance(wormList[CC[index]].getPosition(), wormList[actualWorm].getPosition())
            if (distance>ratio):
                rightDistance = True
    return rightDistance


#hacer el gso principal
"""

def gso(wormList, m, s, gamma, ratio, luciferin, CC):
    contador=0
    gusanitos=[]
    for index in range (m):
        gusanitos.append(crearGusanito())

    while (contador < len(gusanitos)):
        subconjuntoDatos = gusanitos[contador].obtenerSubconjunto()

    #se calcula la formula 8
    CC=seleccionarCC(k, subconjuntoDatos)
    #se calcula la formula 6
    #se calcula la formula 7
    contador=0
    #while (contador < len(CC)):
        #hacer un arreglo con los Fj
        #formula 9
        #formula 1
        #formula 2
        #formula 3
        #formula 4
        #verificar condiciones
        #formula 8
        #subconjuntoDatos pero ahora con el array de Fj
        #formula 6 y 7
        #formula 5 pero realmente no

"""
def main():
    M = 0.09
    s= 0.03
    gamma = 0.6
    ratio = 0.55
    luciferin = 5
    k=10
    s = 0.03
    testHands, indexList = initSetUp()
    wormList, CC = createWorms(k, luciferin, ratio, indexList)
    #wormList[0].buildPermutations()
    #test = searchIndex(wormList[0].permutations,indexList) 
    #print(wormList[0].permutations)
    #print(test)
    #SSE = EQ6(CC, k)
    #InterDist = EQ7(k, CC, wormList)
    
    
    
    """
    #esto tiene que ser una funcion aparte, no en main
    while (contador<totalWorms):
        gusanoActual = Worm(luciferin)
        positions = gusanoActual.getPosition()
        #print (positions)
        cards, totalCards = gusanoActual.getCards(positions, ratio)
        #print(cards)
        #print (totalCards)
        #gusanoActual.setCards(cards, totalCards)
        CC.append(totalCards)
        gusanitos.append(gusanoActual)
        #intradistance = formula 8
        contador+=1
    """
    #ccReal = subconjuntoDatos(k, CC)
    #print(ccReal)
   # intraDistacia = EQ7(k, ccReal, wormList)
    #EQ4(s, wormList, 3, 5)
    #ecuacion6
    #ecuacion7
    #hacer gso con el CC obtenido

main()