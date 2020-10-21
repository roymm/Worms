import numpy as np

class FileHandler:
    def __init__(self):
        pass
    
    #Lee el archivo fileName linea por linea y devuelve una matriz NumPy de
    def readCSVToArray(self,fileName):
        with open(fileName) as openFile:
            arrayCSV = [np.fromstring(arrayLine, dtype=int, sep=',') for arrayLine in openFile]
            return arrayCSV