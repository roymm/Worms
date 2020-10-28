from worm import Worm
import numpy as np
import math
from mpi4py import MPI
import sys
import getopt
import fileHandler
import equations

HAND_TEST_FILENAME = 'poker-hand-training-true.data'
FINAL_RESULTS_FILENAME = 'final_results.txt'



# Funcion que crea lee el archivo inicial de manos de Poker, crea las listas inversas y crea la matriz universo en donde viviran los gusanos
def initSetUp():
    testHands = []
    indexList = []
    # allCards = np.resize(np.arange(13),(5,4,13))

    # Agrega las 5 posiciones
    for i in range(5):
        indexList.append([])

        # Agrego los 4 palos
        for j in range(4):
            indexList[i].append([])

            # Agrego las lista inversa correspondiente a cada carta
            for k in range(13):
                indexList[i][j].append([])

    numLine = 0
    # Procesamiento de archivo de manos

    for line in open(HAND_TEST_FILENAME):
        arrayLine = np.fromstring(line, dtype=int, sep=',')
        position = 0

        for i in range(0, len(arrayLine) - 1, 2):
            rank = arrayLine[i] - 1
            card = arrayLine[i + 1] - 1
            indexList[position][rank][card].append(numLine)
            position += 1

        numLine += 1
        testHands.append(arrayLine)

    testHands = np.array(testHands)
    return indexList


# Funcion que toma una lista de listas (la propiedad dataSet de los gusanos) y relaciona cada carta con su posicion
# a una mano del archivo poker-hand-training-true.data
# Recibe una lista de pares [numero de carta, palo] y retorna una lista de enteros (indices del array testHands)
def searchIndex(permutations, indexList):
    wormIndexList = []
    handPermutations = []
    for permutation in permutations:
        position = 0  # Numero de carta siendo analizada
        auxList = []  # Se almacenan los posibles indices para una permutacion en especifico
        for card in permutation:
            numberCard = card[0]
            rankCard = card[1]
            # possibleIndexList = indexList[position][rankCard][numberCard]
            try:
                possibleIndexList = indexList[position][rankCard][numberCard]
            except:
                print("ERROR en position: " + str(position) + " rank " + str(rankCard) + " card " + str(numberCard))

            if not possibleIndexList:  # Si una carta en una posicion dada no tiene ninguna mano en el archivo, se retorna una lista vacia por default
                auxList = []
                break

            if (
                    position == 0):  # Si es la carta en la primera posicion, se toman esos indices como los iniciales para comparar las otras cartas
                auxList = possibleIndexList
            else:
                i = 0
                while i < len(auxList):
                    wormIndex = auxList[i]
                    if not wormIndex in possibleIndexList:  # Se revisan los indices que ya se tienen, si alguno no está en la carta que se está analizando
                        auxList.remove(
                            wormIndex)  # se elimina de la lista de posibles indices. Así, al final se va a tener una lista de los indices que se repiten
                    i += 1
            position += 1

        if len(auxList) == 1:  # Si se encontró un indice, se guarda junto a su permutacion
            wormIndexList.append((auxList, permutation))
            handPermutations.append(permutation)
    return wormIndexList, handPermutations


#Funcion que se encarga de crear los n gusanos con los que va a trabajar el programa.
#Recibe los valores generales que se aplican a todos los gusanos y retorna una lista de gusanos ordenados por su data set, una lista de intradistancias y una lista de gusanos ordenados por id
def createWorms(k, luciferin, ratio, indexList2, totalWorms, minRange):
    wormList = []
    counter = 0
    wormIndex = minRange
    indexListAux = indexList2
    intraDistances = []

    while (counter < totalWorms):
        indexListAux = initSetUp()
        actualWorm = Worm(luciferin, wormIndex)
        actualWorm.getCards(ratio)  # obtiene las cartas
        actualWorm.buildPermutations()  # le hace todas las permutaciones
        permutations = actualWorm.getPermutations()
        wormIndexList, handPermutations = searchIndex(permutations, indexListAux)
        if (wormIndexList != []):
            actualWorm.setTotalHands(handPermutations, len(handPermutations))
            intraDistance = equations.EQ8(actualWorm)
            actualWorm.setIntraDistance(intraDistance)
            wormList.append(actualWorm)
            wormIndex += 1
            intraDistances.append(intraDistance)
        counter += 1
    wormListAux = wormList.copy()
    return wormList, intraDistances, wormListAux

#Funcion que actualiza los gusanos centroides.
def subconjuntoDatos(wormList, ratio, previousCC):
    # Ordena la lista de gusanos con respecto a la cantidad de permutaciones de mano que tienen
    for i in range(len(wormList) - 1):
        for j in range(0, len(wormList) - i - 1):
            if (wormList[j].total > wormList[j + 1].total):
                wormList[j], wormList[j + 1] = wormList[j + 1], wormList[j]
    CC = []
    counter = 0
    CC.append(wormList[0])
    for i in range(1, len(wormList)):
        if len(CC) == previousCC - 1:
            break
        actualWorm = wormList[i]
        distance = True
        while (counter < len(CC) and distance):
            result = equations.euclidianDistance(CC[counter].position, actualWorm.position)
            if (result < ratio):
                distance = False
            counter += 1
        if (distance):
            CC.append(actualWorm)

    return CC

#Funcion que lee la matriz de distancias entre gusanos y encuentra su vecino mas cercano.
#Recibe el gusano de referencia y retorna un entero que representa el identificador del gusano más cercano
def findClosestNeighbor(worm, neighborMatrix):
    closestNeighborID = 0
    if worm.identificador == 0:
        closestNeighborID = 1
    for neighborID in range(len(neighborMatrix[worm.identificador])):
        if neighborID != worm.identificador:  # Si no soy yo mismo
            if neighborMatrix[worm.identificador][neighborID] < neighborMatrix[worm.identificador][closestNeighborID]:
                closestNeighborID = neighborID
    return closestNeighborID

#Crea una matriz nxn, en donde n es la cantidad de gusanos, con las distancias de todos los gusanos entre si.
#Recibe una lista con todos los gusanos del programa y retorna un array de array numpy de floats
def createNeighborMatrix(wormList):
    neighborMatrix = np.ndarray(shape=(len(wormList), len(wormList)), dtype=float)
    numWormLine = 0
    numWormColumn = 0
    for wormLine in wormList:
        numWormColumn = 0
        for wormColumn in wormList:
            print(
                "Analiza gusano " + str(wormLine.identificador) + " contra el gusano " + str(wormColumn.identificador))
            neighborMatrix[numWormLine][numWormColumn] = equations.euclidianDistance(wormLine.position, wormColumn.position)
            print(neighborMatrix[numWormLine][numWormColumn])
            numWormColumn += 1
        numWormLine += 1
    return neighborMatrix


# Toma la matriz de distancias y actualiza las distancias de un gusano en específico
def updateNeighborMatrix(neighborMatrix, wormToUpDate, wormListAux):
    # Actualiza la linea en la matriz correspondiente al gusano
    for wormColumn in range(len(neighborMatrix[wormToUpDate.identificador])):
        if not wormToUpDate.identificador == wormColumn:    #Para no actualizar la distancia con él mismo
            newDistance = equations.euclidianDistance(wormToUpDate.position, wormListAux[wormColumn].position)
            neighborMatrix[wormToUpDate.identificador][wormColumn] = newDistance
            neighborMatrix[wormColumn][wormToUpDate.identificador] = newDistance
    return neighborMatrix

#Proceso central del programa. Es el encargado del ciclo de mover los gusanos.
def gso(wormList, m, s, gamma, ratio, luciferin, CC, k, SSE, rho, indexList, intraDistances, neighborMatrix,
        wormListAux, minRange, maxRange):
    n = 25010
    totalHands = []
    newWormList = []
    if (maxRange > len(wormList)):
        maxRange = len(wormList)
    for i in range(minRange, maxRange):
        indexListAux = initSetUp()
        actualWorm = wormList[i]
        resultado9 = equations.EQ9(n, SSE, actualWorm.intradistance, wormList[i], intraDistances)
        wormList[i].setAdaptation(resultado9)
        wormList[i].setLuciferin(equations.EQ1(wormList[i], rho, gamma, resultado9))
        closestWormID = findClosestNeighbor(wormList[i], neighborMatrix)
        closestWorm = wormListAux[closestWormID]
        wormList[i].setPosition(equations.EQ4(s, wormList[i], closestWorm))
        neighborMatrix = updateNeighborMatrix(neighborMatrix, wormList[i], wormListAux)
        actualWorm.getCards(ratio)  # obtiene las cartas
        actualWorm.buildPermutations()
        permutations = actualWorm.getPermutations()
        wormIndexList, handPermutations = searchIndex(permutations, indexListAux)
        if (wormIndexList != []):
            actualWorm.setTotalHands(handPermutations, len(handPermutations))
            newWormList.append(actualWorm)
            totalHands.append(len(
                handPermutations))  # aqui le hago set al numero total de manos que tiene un gusano para que sea mas facil sacar los CC
            intraDistance = equations.EQ8(actualWorm)
            actualWorm.setIntraDistance(intraDistance)
            intraDistances.append(intraDistance)

    wormList = newWormList
    return wormList

#Funcion que lee los parametros que se ingresan por linea de comando
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
    totalWorms = 1000 #Las pruebas hechas siempre fueron con 20 gusanos
    neighborMatrix = [[]]
    if (pid == 0):
        rho, gamma, s, luciferin, k, m = obtenerValoresLineaComandos(argv)
        indexList = initSetUp()
    rho, gamma, s, luciferin, k, m, indexList = comm.bcast((rho, gamma, s, luciferin, k, m, indexList), 0)
    pidTotalWorms = int(totalWorms / size)
    minRange = int(pid * pidTotalWorms)
    wormList, intraDistances, wormListAux = createWorms(k, luciferin, ratio, indexList, pidTotalWorms, minRange)
    finalWormList = comm.reduce(wormList, op=MPI.SUM)
    finalIntraDistances = comm.reduce(intraDistances, op=MPI.SUM)
    finalWormListAux = comm.reduce(wormListAux, op=MPI.SUM)
    if (pid == 0):
        CC = subconjuntoDatos(finalWormList, ratio, 0)
        neighborMatrix = createNeighborMatrix(finalWormListAux)
        SSE = equations.EQ6(CC, k)
        # InterDist = EQ7(k, CC, wormList)
    comm.Barrier()
    finalWormList, finalIntraDistances, finalWormListAux, CC, neighborMatrix, SSE = comm.bcast(
        (finalWormList, finalIntraDistances, finalWormListAux, CC, neighborMatrix, SSE), 0)
    minRange = int(pid * len(finalWormList) / size)
    maxRange = int((pid + 1) * len(finalWormList) / size)
    comm.Barrier()
    finalWormList = comm.reduce(wormList, op=MPI.SUM)
    contador = 0
    comm.Barrier()
    largoCentroides = len(CC)
    if (pid == 0):
        while (largoCentroides > k):
            contador += 1
            if (pid == 0):
                finalWormList = gso(finalWormList, m, s, gamma, ratio, luciferin, CC, k, SSE, rho, indexList,
                                    finalIntraDistances, neighborMatrix, finalWormListAux, minRange, maxRange)
                CC = subconjuntoDatos(finalWormList, ratio, largoCentroides)
                print("CC al final del ciclo: " + str(contador) + " = " + str(len(CC)))
                largoCentroides = len(CC)
                SSE = equations.EQ6(CC, k)
                interDist = equations.EQ7(k, CC, wormList)
            # CC, SSE,finalWormList = comm.bcast((CC, SSE, finalWormList),0)
            # comm.Barrier()
        finalResultsWriter = fileHandler.FileHandler()
        finalResultsWriter.writeFinalResults(FINAL_RESULTS_FILENAME, CC)

    #Ciclo paralelizado
    """
        while (largoCentroides > k):
        contador += 1
        minRange = int(pid*(len(finalWormList)/size))
        maxRange = int((pid+1)*(len(finalWormList)/size))
        finalWormList = gso(finalWormList, m, s, gamma, ratio, luciferin, CC, k, SSE, rho, indexList,
                                    finalIntraDistances, neighborMatrix, finalWormListAux, minRange, maxRange)
        comm.Barrier() 
        finalWormList1 = comm.reduce(finalWormList, op=MPI.SUM)  
        comm.Barrier() 
        if(pid==0):
            CC = subconjuntoDatos(finalWormList1, ratio, largoCentroides)
            print("CC al final del ciclo: " + str(contador) + " = " + str(len(CC)))
            largoCentroides = len(CC)
            SSE = EQ6(CC, k)
            #interDist = EQ7(k, CC, wormList)
        comm.Barrier()
        CC, SSE,finalWormList1 = comm.bcast((CC, SSE, finalWormList1),0)
        finalWormList = finalWormList1
        comm.Barrier()
    if (pid==0):
        finalResultsWriter = fileHandler.FileHandler()
        finalResultsWriter.writeFinalResults(FINAL_RESULTS_FILENAME, CC)


    """



if __name__ == "__main__":
    main(sys.argv[1:])
