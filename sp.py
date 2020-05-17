# coding: utf-
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd

import copy
from os import path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)
sheet=client.open("Course_List_for_all_students").sheet1
courses=sheet.col_values(3)
count=dict()
for i in range(len(courses)-1):
	section=courses[i+1]
	(count.update({section:int(count.get(section) or 0)+1}))

for i in range(len(courses)-1):
    print(courses[i+1]+":" +str(count.get(courses[i+1])))


            