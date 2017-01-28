#!/usr/bin/python3

import sys
import os
from PyQt5.QtWidgets import QApplication,QDesktopWidget,QWidget,QTabWidget,QMessageBox
from PyQt5.QtCore import QCoreApplication, Qt
#{mods}#
from data.modules import Login,Oceny,Plan,Zapisz
#{end}#
########################################################################################
########################################  Main Class  ###################################
########################################################################################
class PU_main(QWidget):
	def CreateConfig(self):
		'''Ustalenie konfiguracji programu'''
		self.config = { "TABS": {"GLOWNA":self} }
		self.config["ONLINE"] = 0
		self.config["SESSION"] = ""
		with open("data/config.dat","r") as cfgf:
			tempStr = cfgf.read()
		file_general = tempStr.partition("[GENERAL]")[2].partition("[")[0].strip()
		file_pages = tempStr.partition("[PAGES]")[2].partition("[")[0].strip()
		file_agent = tempStr.partition("[NETWORKAGENT]")[2].partition("[")[0].strip()

		for x in file_general.split(os.linesep):
			self.config[x.partition("=")[0]] = x.partition("=")[2]
		self.config["PAGES"] = {}
		for x in file_pages.split(os.linesep):
			self.config["PAGES"][x.partition("=")[0]] = x.partition("=")[2]
		self.config["PAGES"].update(
			{
				"USOS_DOMAIN": self.config["PAGES"]["USOS"].partition("//")[2],
				"ACTION": self.config["PAGES"]["USOS"] + self.config["PAGES"]["CONTROLLER_ACTION"],
				"ACTIONX": self.config["PAGES"]["USOS"] + self.config["PAGES"]["CONTROLLER_ACTION"]+"actionx:"
			}
		)
		self.config["HEADER"] = []
		for x in file_agent.split(os.linesep):
			self.config["HEADER"].append((x.partition("=")[0],x.partition("=")[2]))

	def LoadModules(self):
		'''Wczytuje poszczegolne taby.'''
		#{mods}#
		self.taby.addTab(Oceny.Oceny(self.config),Oceny.Oceny.__doc__)
		self.taby.addTab(Plan.Plan(self.config),Plan.Plan.__doc__)
		self.taby.addTab(Zapisz.Zapisz(self.config),Zapisz.Zapisz.__doc__)
		#{end}#

	def DeleteModules(self):
		'''Usuwa taby po zalogowaniu'''
		ile = self.taby.count()
		while(ile > 0):
			self.taby.removeTab(ile)
			ile -= 1

	def __init__(self):
		'''Init Class'''
		super().__init__()
		self.setGeometry(100, 100, 800, 600)
		self.setWindowTitle('PocketUSOS - Witaj w programie')
		ilemaokno = self.frameSize()

		#Utworzenie pliku konfiguracyjnego
		self.CreateConfig()

		#Ustawienia tabow
		self.taby = QTabWidget(self)
		self.taby.resize(ilemaokno.width()-1,ilemaokno.height()-1)
		self.taby.addTab(Login.Login(self.config),Login.Login.__doc__)
		self.taby.show()

		#Ustawienia wyswietlania
		wymiary = self.frameGeometry()
		centerp = QDesktopWidget().availableGeometry().center()
		wymiary.moveCenter(centerp)
		self.move(wymiary.topLeft())
		self.show()

	def closeEvent(self, event):
		'''Zamykam program'''
		with open("data/config.dat","r") as f2r:
			tempStr = f2r.read().strip()
		tempStr = tempStr.split(os.linesep)
		acc = 0
		with open("data/config.dat","w") as f2w:
			for x in tempStr:
				if(x[0:9] == "[GENERAL]"):
					acc = 1
				if(x[0:5] == "LOGIN" and acc == 1):
					acc = 0
					f2w.write("LOGIN="+self.config["LOGIN"])
				else:
					f2w.write(x)
				f2w.write(os.linesep)

		if(self.config["ONLINE"] == 1):
			reply = QMessageBox.warning(self, 'Wyjście z programu', "Czy na pewno chcesz wyjść z programu bez wylogowania?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
			if reply == QMessageBox.Yes:
				event.accept()
			else:
				event.ignore()
		else:
			event.accept()
########################################################################################
########################################  Main Loop  ####################################
########################################################################################
if __name__ == '__main__':
	app = QApplication(sys.argv)
	okno = PU_main()
	sys.exit(app.exec_())
