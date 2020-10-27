import numpy as np

class FileHandler:
    def __init__(self):
        pass
    
    #Lee el archivo fileName linea por linea y devuelve una matriz NumPy de
    def readCSVToArray(self,fileName):
        with open(fileName) as openFile:
            arrayCSV = [np.fromstring(arrayLine, dtype=int, sep=',') for arrayLine in openFile]
            return arrayCSV

    def writeFinalResults(self, filename,listaCentroides):
        with open(filename,'w+') as openFile:
            openFile.write("---RESULTADOS FINALES---\n\n")
            for centroide in listaCentroides:
                openFile.write("- Centroide  ID " + str(centroide.identificador)+'\n')
                openFile.write("Coordenadas: " + str(centroide.position)+'\n')
                openFile.write("Datos asociados: " + str(centroide.dataSet)+'\n\n')