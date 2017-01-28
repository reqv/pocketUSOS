#!/usr/bin/python3

from data.modules.ModulPU import ModulPU

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import Thread
import requests
import shutil
from bs4 import BeautifulSoup

class Oceny(ModulPU):
	'''Oceny'''
	def __init__(self,config):
		super().__init__()
		lays = QFormLayout()
		#DEFINICJE STRON
		self.act_oceny = config["PAGES"]["ACTION"] + "dla_stud/studia/oceny/index"

		#Pobranie strony
		ocenki = config["SESSION"].get(self.act_oceny)
		self.ocenki_txt = BeautifulSoup(ocenki.text)

		#layout
		self.form = ""
		self.scrool = QScrollArea()
		self.scrool.setWidgetResizable(1)
		self.scrool.setFixedHeight(400)
		self.srednia = QLabel("")

		szukaj = QPushButton("Szukaj",self)
		szukaj.clicked.connect(self.wyszukaj)
		self.pole = QLineEdit()
		label = QLabel("Podaj id tabeli z ocenami: ")
		spacja = QSpacerItem(400,1)
		self.layout.addItem(spacja,0,0)
		self.layout.addWidget(label,0,1)
		self.layout.addWidget(self.pole,0,2)
		self.layout.addWidget(szukaj,0,3)
		self.layout.addItem(spacja,0,4)
		self.layout.addWidget(self.srednia,0,5)
		self.layout.addWidget(self.scrool,1,0,1,6)


	def wyszukaj(self):
		self.wyczysc()
		suma = 0
		ile = 0
		tabid = self.pole.displayText()
		tab = self.ocenki_txt.find(id="tab"+tabid)
		if tab == None:
			return
		tr = tab.find_all('tr')
		for x in tr:
			td = x.findAll("td")
			typ = td[2].findAll("a")
			ocena = td[2].findAll("span")
			if len(typ) != len(ocena):
				if ocena[0].string != "(brak ocen)":
					typ.insert(0,"Ocena: ")
				else:
					typ.insert(0,"")
			i = 0
			j = len(ocena) -1
			while j > -1:
				if ocena[j].string[0] == "(" and ocena[j].string != "(brak ocen)":
					del ocena[j]
				j -= 1
			calosc = ""
			for l in ocena:
				if calosc != "":
					calosc += "\n"
				if ocena[i].string != "ZAL" and ocena[i].string != "(brak ocen)":
					suma += float(ocena[i].string.replace(",","."))
					ile += 1
				if typ[i] == "Ocena: " or typ[i] == "":
					calosc += typ[i]
				else:
					calosc += typ[i].text +": "
				calosc += ocena[i].string
				i+=1
			self.form.addRow(QLabel(td[0].find("a").text),QLabel(calosc))
		if ile != 0:
			suma = suma / ile
		else:
			suma = 0.0
		self.srednia.setText("Średnia: {:.2}".format(suma))
			
	def wyczysc(self):
		del self.form
		self.form = QFormLayout()
		self.form.setHorizontalSpacing(80)
		self.form.setVerticalSpacing(40)
		grupa = QGroupBox("Dostepna lista ocen")
		grupa.setLayout(self.form)
		#wczytanie nowego
		stary = self.scrool.takeWidget()
		del stary
		self.scrool.setWidget(grupa)
