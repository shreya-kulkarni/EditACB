import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
import copy
from os import path
from ui import Ui_MainWindow, Ui_SecondPage, Ui_PreReq
import gspread
from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/drive"]
credentials = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(credentials)

ACB_BACKLOG_LIST = client.open("ACBBACKLOG").sheet1
PENDING_COURSE_LIST = client.open("Pending Courses").sheet1
PREREQ_LIST =client.open("Pre-requisite").sheet1
TIME_TABLE = client.open("TIMETABLE").sheet1
PENDING_BACKLOG = client.open("Pending Backlog").sheet1

main_win = None
prereqWindow = None
student_id = None
student_name = None
courseDict = {}
studentIDS = []
electives = []

class MainWindow:
    def __init__(self, studentIDS):
        global prereq
        global isPrereqFor
        isPrereqFor = {}
        prereq = {}
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)
        self.ui.listWidget.addItems(studentIDS)
        self.ui.pushButton.clicked.connect(self.pushButton_click)
        #prereq_file = pd.read_excel(PREREQ_LIST, skiprows=1)
        self.formPrereq()

    def show(self):
        self.main_win.show()
    def pushButton_click(self):
        global student_id
        student_id = self.ui.listWidget.currentItem().text().split('-')[1]
        global student_name
        student_name = self.ui.listWidget.currentItem().text().split('-')[0]
        global main_win
        main_win = SecondPage()
        main_win.show()
        
    #def formPrereq(self):
        preSubject=PREREQ_LIST.col_values(2)
        Catalog=PREREQ_LIST.col_values(3)
        preq1_Subject=PREREQ_LIST.col_values(7)
        preq1_catalog=PREREQ_LIST.col_values(8)
        preq2_Subject=PREREQ_LIST.col_values(13)
        preq2_catalog=PREREQ_LIST.col_values(14)
        preq3_Subject=PREREQ_LIST.col_values(19)
        preq3_catalog=PREREQ_LIST.col_values(20)
        preq4_Subject=PREREQ_LIST.col_values(25)
        preq4_catalog=PREREQ_LIST.col_values(26)
        or_and = ""
        #print(preSubject)
        for i in range(len(preSubject)-2):
            course1 = preSubject[i+2].strip(
            ) + Catalog[i+2].strip()
            print(preSubject[i+2])
            if str(preq1_Subject[i+2]) == 'nan':
                continue
            l = preq1_Subject[i+2].strip(
            ) + preq1_catalog[i+2].strip()
            prereq[course1] = [l]
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
#######################################################################
        
            if str(preq2_Subject[i+2]) == 'nan':
                continue
            l = preq2_Subject[i+2].strip(
            ) + preq2_catalog[i+2][i].strip()
            prereq[course1].append(l)
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
########################################################
            if str(preq3_Subject[i+2]) == 'nan':
                continue
            l = preq3_Subject[i+2].strip(
            ) + preq3_catalog[i+2][i].strip()
            prereq[course1].append(l)
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
########################################################
            if str(preq4_Subject[i+2]) == 'nan':
                continue
            l = preq4_Subject[i+2].strip(
            ) + preq4_catalog[i+2][i].strip()
            prereq[course1].append(l)
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
########################################################
