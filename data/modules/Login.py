#!/usr/bin/python3

from data.modules.ModulPU import ModulPU

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import Thread
import requests
import shutil
from bs4 import BeautifulSoup

class Login(ModulPU):
	'''Strona Logowania'''
	make = pyqtSignal()
	delete = pyqtSignal()
	def __init__(self,config):
		super().__init__()
		self.config = config
		########################################################################
		# strona logowania do usług UMK wraz z przekierowaniem do usługi USOSweb
		self.LoginPage = config["PAGES"]["LOGIN"] + 'login?service=' + config["PAGES"]["ACTIONX"] + 'logowaniecas/index()' + '&locale=pl' 
		# adres na który wchodzimy aby się wylogować
		self.LogoutPage = config["PAGES"]["ACTIONX"] + 'logowaniecas/wyloguj()'
		# MÓJ USOSWEB, służy do testowania poprawnego zalogowania
		self.HomePage = config["PAGES"]["ACTION"] + 'home/index'
		########################################################################
		#config
		config["TABS"]["LOGIN"] = self

		#Sygnal
		self.make.connect(config["TABS"]["GLOWNA"].LoadModules)
		self.delete.connect(config["TABS"]["GLOWNA"].DeleteModules)

		#Wyswietlanie
		self.message = QLabel("Wprowadź swoje dane, aby zalogować do USOS",self)
		self.login_str = ""
		login = QLineEdit()
		login.setObjectName("login")
		login.textChanged.connect(self.wypisz_login)
		login.setText(config["LOGIN"])

		### LOGO ###############
		logo_label = QLabel()
		logo_label.resize(800,400)
		logo = QPixmap("data/pusosLogo.png")
		if(logo.isNull() == False):
			scaled = logo.scaled(logo_label.size())
			logo_label.setPixmap(scaled)
		########################

		self.password_str = ""
		password = QLineEdit()
		password.setEchoMode(2)
		password.textChanged.connect(self.wypisz_pass)
		password.setText(config["PASSWORD"])

		self.ok_butt = QPushButton("Zaloguj")
		self.ok_butt.clicked.connect(self.button_clicked)
		spacjaY = QSpacerItem(1,400)
		spacjaX = QSpacerItem(200,1)

		#Login Form Local Layout
		lay = QFormLayout()
		lay.addRow("Konto: ",login)
		lay.addRow("Hasło: ",password)
		lay.addRow(self.ok_butt)

		#Add to Global Template
		self.layout.addWidget(logo_label,0,0,1,3)
		self.layout.addItem(spacjaX,1,0)
		self.layout.addLayout(lay,1,1)
		self.layout.addItem(spacjaX,1,2)
		self.layout.addWidget(self.message,2,1)

	def keyPressEvent(self,event):
		key = event.key()
		if(key == Qt.Key_Return or key == Qt.Key_Enter):
			if(self.ok_butt.isEnabled()):
				self.button_clicked()
	def wypisz_login(self,wy):
		self.login_str = wy
	def wypisz_pass(self,wy):
		self.password_str = wy
	def button_clicked(self):
		self.ok_butt.setEnabled(0)
		self.th = Thread(target=self.login)
		self.th.start()
	def login(self):
		if self.config["ONLINE"] == 0:
			if(self.login_str == "" or self.password_str == ""):
				self.message.setText("Proszę wypełnić wszystkie pola!")
				self.ok_butt.setEnabled(1)
				return
			self.message.setText("Pobieram lt...")
			self.config["LOGIN"] = self.login_str
			self.config["PASSWORD"] = self.password_str
			##########################################TU DZIALANIA LOGUJACE
			self.config["SESSION"] = requests.Session()
			session = self.config["SESSION"]
			session.headers = self.config["HEADER"]
			resp = session.get(self.LoginPage)
			lt =  resp.text.partition('hidden" name="lt" value="')[2].partition('"')[0]
			execut = resp.text.partition('hidden" name="execution" value="')[2].partition('"')[0]
			self.message.setText("Loguje do systemu...")
			postData = {'username': self.config["LOGIN"], 'password': self.config["PASSWORD"], 'lt': lt,'execution': execut, '_eventId': 'submit'}
			session.post(self.LoginPage,postData)
			if self.LoginCheck() == 1:
				self.message.setText("Nie udało się zalogować do systemu")
				self.ok_butt.setEnabled(1)
				return
			##########################################
			self.make.emit()
			self.ok_butt.setText("Wyloguj")
			self.message.setText("Zalogowano do USOS")
		else:
			## WYLOGOWANIE
			resp = self.config["SESSION"].get(self.LogoutPage)
			if self.LoginCheck() == 1:
				#self.config["LOGIN"] = ""
				self.config["PASSWORD"] = ""
				self.delete.emit()
				self.message.setText("Wylogowano ze systemu USOS")
				self.ok_butt.setText("Zaloguj")
			else:
				self.message.setText("Nie udało się wylogować ze systemu")
		self.ok_butt.setEnabled(1)

	def LoginCheck(self):
		odpowiedz = self.config["SESSION"].get(self.HomePage)
		if(odpowiedz.status_code == 200):
			self.config["ONLINE"] = 1
			return 0
		else:
			self.config["ONLINE"] = 0
			return 1
