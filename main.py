from mpi4py import MPI
import numpy as np
import logging
import sys
import equations
import worm
import card


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

#Funcion que crea los gusanos iniciales y hace otras cosas del inicio que todavia no sabemos
def initSetUp(numberWorms):
    #Creacion de universo con una matriz de 13 (cartas) * 4 (palos) * 5 cartas en la mano
    if(pid == 0):
        cards = np.resize(np.arange(13),(5,4,13))
        print(cards)
    
    #Procesamiento de archivo de manos
    #if(pid == 0):
    #    for line in open('poker-hand-training-true.data'):
    #        linesFile += [line]
    #    numLinesFile = len(linesFile)
    #    vi = int(pid*numLinesFile/size)
    #    vf = int((pid+1)*numLinesFile/size) - 1
    #    for i in range(vi,vf):
    #        np.fromstring(linesFile[i], dtype=int, sep=',')

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
    return int(decLuciferin), int(incLuciferin), int(distWorms). int(valIniLuciferin), int(classes), int(worms)

    return int(stringProductor), int(stringConsumidor)

def main(argv):
    comm = MPI.COMM_WORLD
    tiempoInicial = MPI.Wtime() #Para medir el tiempo pared
    comm.Barrier()
    
    initSetUp(10)
    
    diferenciaTiempo = MPI.Wtime() - tiempoInicial  #Calcula el tiempo pared
    tiempoMaxTotal = comm.reduce(diferenciaTiempo, op=MPI.MAX) #Obtiene el tiempo con mayor duracion

if __name__ == "__main__":
    main(sys.argv[1:])       # le pasa a main la lista de opciones, los parametros
