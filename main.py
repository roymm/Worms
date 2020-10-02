from mpi4py import MPI
import getopt
import numpy as np
import logging
import sys
import equations
import worm
import card
import sys, getopt

#TODO: Hay que crear listas inversas para encontrar cuales manos abarca un gusano en x posicion. 
# Las listas inversas son arreglos de indices de la lista completa de manos (la que se lee del archivo)
# Para cada carta en cada posicion posible (o sea 13 x 5) se necesita crear una lista que tenga los indices de las manos en donde se esta usando esa carta en esa posicion
# Ejemplo: Si tenemos la siguiente lista de todas las posibles manos:
# ...
# 1001: <(1,1),(5,3),(4,1),(10,2)>
# 1002: <(1,1),(4,3),(4,1),(9,3)>
# 1003: <(5,2),(5,3),(4,1),(10,2)>
# ...
#Entonces, la lista inversa de la carta <5,3> como segunda carta en la mano es:
# <1001,1003>
#Luego de tener todos los indices del radio de las cartas que cubre el gusano, se analiza y si hay algun indice que se repite
# en todas las dimensiones, significa que esa mano la cubre el gusano

comm = MPI.COMM_WORLD		# obt acceso al "comunicador"
pid = comm.rank				# obt numero de proceso	
size = comm.size            #obt cantidad de procesos corriendo el programa
indexList = []              #Listas inversas de cada carta en cada posicion de la mano
allCards = []               #Todas las cartas en las 5 posiciones (universo)
testHands = []              #Archivo poker-hand-training-true.data en memoria

#Funcion que crea los gusanos iniciales y hace otras cosas del inicio que todavia no sabemos
def initSetUp():
    global testHands
    global allCards
    global indexList
    #Creacion de universo con una matriz de 13 (cartas) * 4 (palos) * 5 cartas en la mano
    if(pid == 0):
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
            #Leo el palo 
            for i in range(0,len(arrayLine)-1,2):
                rank = arrayLine[i]
                card = arrayLine[i+1]
                indexList[position][rank-1][card-1].append(numLine)
                position += 1
                
            numLine += 1
            testHands.append(arrayLine)
        
        testHands = np.array(testHands)
        print(indexList[0][0][12])

#Funcion que toma los valores ingresados por el usuario en la linea de comandos y los verifica
def obtenerValoresLineaComandos(argv):
    decLuciferin = ""
    incLuciferin = ""
    distWorms = ""
    valIniLuciferin = ""
    classes = ""
    worms = ""
    try:
        opts, arg = getopt.getopt(argv, "r:g:s:l:k:m", ["R=", "G=", "S=", "L=", "K=", "M="])
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
    return int(decLuciferin), int(incLuciferin), int(distWorms), int(valIniLuciferin), int(classes), int(worms)

def subconjuntoDatos(k, subconjuntoDatos):
    #subconjuntoDatos.sort()
    CC=[]
    contador=0
    #contador2=0
    aux = 0
    while (contador<k):

        max = subconjuntoDatos[0]
        for index in range(len(subconjuntoDatos)):
            if (subconjuntoDatos[index]>max and not index in CC):
                max = subconjuntoDatos
                aux = index          
        CC.append(aux)
        contador+=1
    
    return CC


def main(argv):
    comm = MPI.COMM_WORLD
    tiempoInicial = MPI.Wtime() #Para medir el tiempo pared
    comm.Barrier()
    
    initSetUp()
    
    diferenciaTiempo = MPI.Wtime() - tiempoInicial  #Calcula el tiempo pared
    tiempoMaxTotal = comm.reduce(diferenciaTiempo, op=MPI.MAX) #Obtiene el tiempo con mayor duracion
    
    if(pid==0):
        print(tiempoMaxTotal)

if __name__ == "__main__":
    main(sys.argv[1:])       # le pasa a main la lista de opciones, los parametros
