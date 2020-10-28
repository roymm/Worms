import numpy as np

class FileHandler:
    def __init__(self):
        pass

    #Funcion que escribe los resultados finales del algoritmo en un archivo.
    #Recibe una lista de los gusanos centroides y un nombre de archivo para escribir
    def writeFinalResults(self, filename,listaCentroides):
        with open(filename,'w+') as openFile:
            openFile.write("---RESULTADOS FINALES---\n\n")
            for centroide in listaCentroides:
                openFile.write("- Centroide  ID " + str(centroide.identificador)+'\n')
                openFile.write("Coordenadas: " + str(centroide.position)+'\n')
                openFile.write("Datos asociados: " + str(centroide.dataSet)+'\n\n')