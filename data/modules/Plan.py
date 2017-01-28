#!/usr/bin/python3

from data.modules.ModulPU import ModulPU

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from threading import Thread
import requests
import shutil
from bs4 import BeautifulSoup

class Plan(ModulPU):
	'''Plan Zajęć'''
	def __init__(self,config):
		super().__init__()
		self.cn = config
		self.obrazplanu = QLabel()
		self.obrazplanu.setScaledContents(True)
		spacja = QSpacerItem(1000,1000)
		self.mess1 = QLabel("")
		bu1 = QPushButton("Pobierz plan")
		bu1.clicked.connect(self.bu1_action)

		scrool = QScrollArea()
		scrool.setWidgetResizable(1)
		scrool.setWidget(self.obrazplanu)

		self.layout.addWidget(bu1,0,0)
		self.layout.addWidget(scrool,1,0)
		self.layout.addWidget(self.mess1,2,0)
		self.update()

	def bu1_action(self):
		strona = self.cn["PAGES"]["ACTION"] + "home/plan&division=semester"
		#Pobranie strony
		plan = self.cn["SESSION"].get(strona)
		plan_text = BeautifulSoup(plan.text)
		link = plan_text.find('img',usemap="#plan_image_map")
		#Pobieram obrazek
		r = self.cn["SESSION"].get(link["src"], stream=True)
		if r.status_code == 200:
			with open("plan.gif", 'wb') as filee:
				r.raw.decode_content = 1
				shutil.copyfileobj(r.raw, filee)
		self.mess1.setText("Pobrano plan do folderu z programem.")
		self.update()

	def update(self):
		ob = QPixmap("plan.gif")
		if(ob.isNull() == False):
			scaled = ob
			self.obrazplanu.setPixmap(scaled)
