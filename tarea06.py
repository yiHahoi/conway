
###############################
########## TAREA 06 ###########
### Diego Carrasco Vasquez ####
###############################

import sys
import os
import conway
import pyqtgraph as pg
import numpy as np
from PyQt4 import QtGui, QtCore, uic
sys.path.append(os.getcwd())

##############
## VENTANA  ##
##############


class WINDOW(QtGui.QMainWindow):
    def __init__(self):

        QtGui.QMainWindow.__init__(self)

        # variables
        self.columnSize = 20
        self.rowSize = 20
        self.xInitPos = 0
        self.yInitPos = 0
        self.state = conway.CONWAY(self.rowSize,self.columnSize)
        self.alive = 0
        self.aliveEvolution = []
        self.color1 = pg.mkBrush(255,255,255)
        self.color2 = pg.mkBrush(0,0,0)
        self.brushes = []
        self.fileName = ''
        self.pause = True
        self.generation = 0

        # se carga la ui
        self.ui = uic.loadUi('ventana.ui',self)

        # se conectan los botones en la ui a sus funciones
        self.ui.connect(self.ui.tick, QtCore.SIGNAL('clicked()'), self.nextState)
        self.ui.connect(self.ui.botonStartPause, QtCore.SIGNAL('clicked()'), self.startPause)
        self.ui.connect(self.ui.botonRestart, QtCore.SIGNAL('clicked()'), self.reloadState)
        self.ui.connect(self.ui.botonClean, QtCore.SIGNAL('clicked()'), self.cleanState)
        self.ui.connect(self.ui.botonOpen, QtCore.SIGNAL('clicked()'), self.openFileDialog)
        self.ui.sizeOptions.valueChanged.connect(self.gridSize)
        self.ui.speedSlide.valueChanged.connect(self.changeSpeed)
        self.ui.xPosValue.textEdited.connect(self.changeXInitPos)
        self.ui.yPosValue.textEdited.connect(self.changeYInitPos)
        
        # se crea el plot con la matriz de celdas
        self.gfx = self.ui.PlotView.addPlot()
        self.restartPlot()
        self.createGrid()
        self.updateGrid()

        # se crea el plot con la grafica de celdas vivas
        self.gfx2 = self.ui.PlotView2.addPlot(title='Celdas Vivas')
        self.restartPlot2()

        # Timer
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.TIME_INTERVAL = 1000
        self.TIME_INTERVAL_MAX = 2000


    # Crea plot
    def restartPlot(self):
        # ventana grafica
        self.ui.PlotView.removeItem(self.gfx)
        self.gfx = self.ui.PlotView.addPlot()
        self.datos = pg.ScatterPlotItem()
        self.gfx.addItem(self.datos)
        self.gfx.hideAxis('bottom')
        self.gfx.hideAxis('left')
        self.gfx.setXRange(1,0)
        self.gfx.setYRange(1,0)
        self.gfx.setMouseEnabled(x=False, y=False)
        self.gfx.enableAutoRange(x=True,y=True)


    # Crea plot2
    def restartPlot2(self):
        # ventana grafica       
        self.ui.PlotView2.removeItem(self.gfx2)
        self.gfx2 = self.ui.PlotView2.addPlot(title='Celdas Vivas por Generacion')
        self.gfx2.setLabel('left','Celdas Vivas')
        self.gfx2.setLabel('bottom','Generacion')
        self.datos2 = self.gfx2.plot(pen='y')
        self.datos2.setData(self.aliveEvolution)
        self.gfx2.enableAutoRange(x=True,y=True)


    # actualiza los colores de la grid
    def createGrid(self):
        self.pause = True
        self.generation = 0
        self.cells = []
        self.brushes = []
        self.datos.clear()
        self.state = conway.CONWAY(self.rowSize,self.columnSize)
        
        for i in range(self.rowSize):
            for j in range(self.columnSize):
                if self.state.prevState[i,j] == 0:
                    self.brushes.append(self.color1)
                else:
                    self.brushes.append(self.color2)
                self.cells.append({'pos': (j+0.5, self.rowSize-i+0.5),
                              'size':300/self.rowSize,
                              'symbol': 's',
                              'brush': self.brushes[-1],
                              'pen': {'color': (0,0,0),
                                      'width': 0.5},
                               })

        self.datos.addPoints(self.cells)
        self.datos.sigClicked.connect(self.clicked)



    # actualiza los colores de la grid
    def updateGrid(self):
        ctr = 0
        self.alive = 0
        for i in range(self.rowSize):
            for j in range(self.columnSize):
                if self.state.prevState[i,j] == 0:
                    self.brushes[ctr] = self.color1
                else:
                    self.brushes[ctr] = self.color2                    
                    self.alive += 1
                ctr += 1
        self.datos.setBrush(self.brushes, mask=None)


    def gridSize(self, N):
        self.columnSize = N
        self.rowSize = N
        self.restartPlot()
        self.createGrid()
        

    def updateTimer(self):
        if self.pause == False:
            self.nextState()
            self.timer.start(self.TIME_INTERVAL)

    def changeSpeed(self, speed):
        self.TIME_INTERVAL = self.TIME_INTERVAL_MAX - speed

    # funcion sartPause()
    def startPause(self):
        if self.pause:
            self.pause = False
            self.updateTimer()
        else:
            self.pause = True

    def nextState(self):
        self.state.tick()
        self.updateGrid()
        linea = '# Generacion: '+str(self.generation)+'     # Celdas Vivas: '+str(self.alive)
        self.ui.infoBox.append(linea)
        self.aliveEvolution.append(self.alive)
        self.restartPlot2()
        self.generation += 1
        
    ## Make all plots clickable
    def clicked(self, plot,  points):
        x , y = points[0].pos()
        x = int(x - 0.5)
        y = int(y - 1.5)
        #print 'celda seleccionada: pos=( ', x, ', ', y, ' )'
        if self.state.prevState[self.rowSize-1-y,x] == 1:
            self.state.prevState[self.rowSize-1-y,x] = 0
        else:
            self.state.prevState[self.rowSize-1-y,x] = 1
        self.updateGrid()

    def changeXInitPos(self,val):
        self.xInitPos = int(val)
        
    def changeYInitPos(self,val):
        self.yInitPos = int(val)

    def cleanState(self):
        self.pause = True
        self.aliveEvolution = []
        self.restartPlot()
        self.createGrid()
        self.updateGrid()
        
    def reloadState(self):
        self.state.loadCellFile(self.fileName, self.xInitPos, self.yInitPos)
        self.updateGrid()

    def openFileDialog(self):
        self.fileName = QtGui.QFileDialog.getOpenFileName(self, 'Abrir archivo', '/home/yihahoi/Dropbox/PYTHON/Tarea06/cells/')
        self.state.loadCellFile(self.fileName, self.xInitPos, self.yInitPos)
        self.updateGrid()



# Loop Main de la interfaz
App = QtGui.QApplication(sys.argv)
win = WINDOW()
win.show()
sys.exit(App.exec_())

