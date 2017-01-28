#!/usr/bin/python3

from data.modules.ModulPU import ModulPU

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import Thread
import requests
from bs4 import BeautifulSoup

class Zapisz(ModulPU):
	'''Zapisz na zajecia'''
	def __init__(self,config):
		super().__init__()
		self.cn = config

		self.mess1 = QLabel("")
		bu1 = QPushButton("Zapisz")
		bu1.clicked.connect(self.bu1_action)
		self.las = QLineEdit()
		self.las.setText("0800-KK-OLAP")
		self.layout.addWidget(bu1,0,0)
		self.layout.addWidget(self.las,0,1)
		self.update()

	def bu1_action(self):
		strona = self.cn["PAGES"]["ACTION"]+"katalog2/przedmioty/pokazPrzedmiot&prz_kod="+self.las.text()
		stro = "https://usosweb.umk.pl/kontroler.php?_action=dla_stud/rejestracja/brdg2/grupyPrzedmiotu&rej_kod=0851-2015%2F16Z&prz_kod=0800-31KKP-DW&cdyd_kod=2015%2F16Z&odczyt=0&prgos_id=228379&callback=g_afbbf28c"
		zwrot = self.cn["SESSION"].get(stro)
		with open("lol","w") as l:
			l.write(zwrot.text)
