import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
import numpy as np
import copy
from os import path

from ui import Ui_MainWindow, Ui_SecondPage, Ui_PreReq
count=dict()
courses=pd.read_excel("Course_List_for_all_students.xls");


for i in range(len(courses)):
            section = courses["Section"][i].split('-')[0]+courses["Section"][i].split('-')[1]
            count.update({section:int(count.get(section) or 0)+1})
            
for i in range(len(courses)):

 section = courses["Section"][i].split('-')[0]+courses["Section"][i].split('-')[1]
 print(section)
 print(count.get(section))
class newfun:
   def __init__(self):
   	self.ui.pushButton.clicked.connect(self.validate)
   	def setToValidate(self):
        self.ui.pushButton.setText("Validate")
        
   # def validate(self):
       
