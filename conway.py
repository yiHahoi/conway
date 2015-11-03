
###############################
########## TAREA 04 ###########
### Diego Carrasco Vasquez ####
###############################

import sys
import os
import time
import numpy
sys.path.append(os.getcwd())

##################
## Clase Conway ##
##################

# Clase Conway
class CONWAY(object):
    """
    La Clase CONWAY recibe las dimensiones de la matriz conway.
    La funcion loadCellFile() carga en la matriz conway los valores definidos en el archivo .cell.
    Mediante el metodo tick() avanza el estado de prevState.
    countNeighbors() devuelve el numero de vecinos vivos de una celda en la posicion i,j
    applyRules() actualiza el estado de las celdas en prevState.

    """

    def __init__(self, W = 20, H = 20):
        """ Inicializa Variables """
        self.WIDTH = W
        self.HEIGHT = H
        self.prevState = numpy.zeros((self.HEIGHT,self.WIDTH))
        self.nextState = numpy.zeros((self.HEIGHT,self.WIDTH))
        numpy.copyto(self.prevState,self.nextState)


    def loadCellFile(self, fileName, xPos = 0, yPos = 0):
        """
        Agrega a la matriz de numpy el patron definido en el archivo .cell
        """
        cellFile = open(fileName, 'r')
        row_ctr = 0
        for line in cellFile:
            if '!' not in line:
                col_ctr = 0
                for char in line:
                    if char == '.':
                        self.prevState[ yPos + row_ctr,
                                        xPos + col_ctr] = 0
                    elif char == 'O':
                        self.prevState[ yPos + row_ctr,
                                        xPos + col_ctr] = 1
                    col_ctr += 1
            row_ctr += 1
        cellFile.close()


    def tick(self):
        """ Avanza un estado """
        self.applyRules()
        numpy.copyto(self.prevState,self.nextState)


    def applyRules(self):
        """ Aplica las reglas del juego """
        for i in range(self.HEIGHT):
            for j in range(self.WIDTH):
                count = self.countNeighbors(i,j)
                #VIVA
                if self.prevState[i,j] == 1:
                    #Subpoblacion
                    if count < 2:
                        self.nextState[i,j] = 0
                    #Sobrepoblacion
                    elif count > 3:
                        self.nextState[i,j] = 0
                    #Estasis
                    else:
                        self.nextState[i,j] = 1
                #MUERTA
                else:
                    #Reproduccion
                    if count == 3:
                        self.nextState[i,j] = 1

                        


    def countNeighbors(self,i,j):
        """
        Cuenta el numero de vecinos vivos de la posicion i,j

        [ i-1,j-1 ]    [ i-1,j ]    [ i-1,j+1 ]
        [  i,j-1  ]    [  i,j  ]    [  i,j+1  ]
        [ i+1,j-1 ]    [ i+1,j ]    [ i+1,j+1 ]

        """
        ctr = 0
        #FILA 1
        if i-1 >= 0 and j-1 >= 0 and self.prevState[i-1,j-1] == 1:
            ctr += 1
        if i-1 >= 0 and self.prevState[i-1,j] == 1:
            ctr += 1
        if i-1 >= 0 and j+1 < self.WIDTH and self.prevState[i-1,j+1] == 1:
            ctr += 1
        #FILA 2
        if j-1 >= 0 and self.prevState[i,j-1] == 1:
            ctr += 1
        if j+1 < self.WIDTH and self.prevState[i,j+1] == 1:
            ctr += 1
        #FILA 3
        if i+1 < self.HEIGHT and j-1 >= 0 and self.prevState[i+1,j-1] == 1:
            ctr += 1
        if i+1 < self.HEIGHT and self.prevState[i+1,j] == 1:
            ctr += 1
        if i+1 < self.HEIGHT and j+1 < self.WIDTH and self.prevState[i+1,j+1] == 1:
            ctr += 1

        return ctr
    





