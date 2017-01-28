#!/usr/bin/python3

from PyQt5.QtWidgets import *

class ModulPU(QWidget):
	def __init__(self):
		super().__init__()
		self.layout = QGridLayout()
		self.setLayout(self.layout)

#################################################################################################################
#################################################################################### Przykladowa klasa modulu ####
#################################################################################################################
#class Przyklad(ModulPU):	#Dziedziczenie po klasie glownej "Modul"
#	def __init__(self,config):
#		super().__init__()
#		butt = QPushButton("Click ME",self)
#		butt.clicked.connect(self.wcisniety)
#		butt.show()
#		self.layout.addWidget(butt,0,0)
#		self.cn = config
#	def wcisniety(self):
#		qm = QMessageBox(self)
#		qm.setText(self.cn["LOGIN"])
#		qm.show()
