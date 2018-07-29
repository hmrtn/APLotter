####################################
####  University of Washington  ####
####  Advanced Propulsion Lab   ####
####       Hans Martin          ####
####  Last Edit: July, 2018   ####
####################################


import sys
import os
import matplotlib.pyplot as plt 
import numpy as np
import random
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMessageBox, QCheckBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

temp = 10*1.16E4
boltz = 1.38E-23
area = 1.749E-5
elec = 1.602E-19
mass = 6.67E-26
correct = 0.004
const = 0.6*elec*area*np.sqrt(boltz*temp/mass)
window = 500


class Window(QDialog): 
    
    def __init__(self, parent = None): 
    
        super(Window, self).__init__(parent)

        self.setGeometry(100,115,250,150)
        self.setWindowTitle('APLotter 1.0')
        self.setWindowIcon(QIcon('assets/ic_aplotter.png'))

        self.buttonLP = QPushButton('Plot Langmuir Data', self)
        self.buttonRP = QPushButton('Plot RPA Data', self)
        self.buttonFP = QPushButton('Plot Faraday Data', self)
        self.expOpt = QCheckBox('Export Data', self)

        layout = QVBoxLayout()
        layout.addWidget(self.buttonLP)
        layout.addWidget(self.buttonRP)
        layout.addWidget(self.buttonFP)
        layout.addWidget(self.expOpt)
        self.setLayout(layout)

        self.buttonLP.clicked.connect(LPlot)

class LPlot(QDialog):

    AVGDIC = {}
    DENSDIC = {}
    DATADIC = {}
    RMSDIC = {}

    def __init__(self):

        super(LPlot, self).__init__()

        self.avg_dic = LPlot.AVGDIC
        self.dens_dic = LPlot.DENSDIC
        self.data_dic = LPlot.DATADIC
        self.rms_dic = LPlot.RMSDIC
        self.initLPlot()

    def initLPlot(self):
        
        if 'DLP' in os.listdir(): 
            os.chdir('DLP')

        self.get_data_dic()
        self.get_rms_dic()
        self.get_avg_dic()
        self.get_dens_dic()
    
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)

        self.setWindowTitle('LPlotter')
        self.setLayout(layout)

        self.pltDLP()

        os.chdir('..')

    def get_data_dic(self):

        for folder in os.listdir():
            self.data_dic.update({folder:[]})
            for shot in os.listdir(folder):
                self.data_dic[folder].append([np.ndfromtxt(folder+'/'+shot, delimiter = '\t')])

    def get_rms_dic(self):

        for key in self.data_dic.keys():
            self.rms_dic.update({key:[]})
            for shot in self.data_dic[key]:
                V = shot[0][:,1]
                rms = correct*np.sqrt(np.convolve(np.square(V), 
                            np.ones((window,))/window, mode = 'same'))
                self.rms_dic[key].append([rms])
                
    def get_avg_dic(self):

        for key in self.rms_dic.keys():
            self.avg_dic.update({key:(np.sum(self.rms_dic[key], axis = 0)/len(self.rms_dic[key]))})
    
    def get_dens_dic(self):

        for key in self.avg_dic.keys():
            self.dens_dic.update({key:self.avg_dic[key]/const})

    def pltDLP(self):
        
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.set_xlabel('Time ($\mu$s)'); ax.set_ylabel('$n_{e}$ ($m^{-3}$)')
        ax.set_title('Plasma Density')
        ax.minorticks_on()
        ax.grid(which = 'major', alpha = 0.5); ax.grid(which = 'minor', alpha = 0.2)

        for key in self.avg_dic.keys():
            for i in self.dens_dic[key]:
                data = i
                ax.plot(data, '-')
                self.canvas.draw()
                ax.legend(self.avg_dic,  prop={'size': 7})

        QDialog.exec(self)

def main():

    app = QApplication(sys.argv)
    main = Window()
    main.show()
    sys.exit(app.exec())

if __name__ == '__main__'                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          :
    main()
    