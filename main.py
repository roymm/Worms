from mpi4py import MPI
from numpy import random
import logging
import sys
import equations
import worm

comm = MPI.COMM_WORLD		# obt acceso al "comunicador"
pid = comm.rank				# obt numero de proceso	
size = comm.size            #obt cantidad de procesos corriendo el programa

#Funcion que crea los gusanos iniciales y hace otras cosas del inicio que todavia no sabemos
def initSetUp(numberWorms):
    vi = int(pid*numberWorms/size + 2)
	vf = int((pid+1)*numberWorms/size + 2) - 1

    for i in range(vi,vf):
        coordinates = random.randint(100, size=(5))
        newWorm = worm.Worm(i,)

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
    
    
    diferenciaTiempo = MPI.Wtime() - tiempoInicial  #Calcula el tiempo pared
    tiempoMaxTotal = comm.reduce(diferenciaTiempo, op=MPI.MAX) #Obtiene el tiempo con mayor duracion

if __name__ == "__main__":
    main(sys.argv[1:])       # le pasa a main la lista de opciones, los parametros
