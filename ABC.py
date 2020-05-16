import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import pandas as pd
import copy
from os import path

from ui import Ui_MainWindow, Ui_SecondPage, Ui_PreReq

ACB_BACKLOG_LIST = 'ACBBACKLOG.xls'
PENDING_COURSE_LIST = 'Pending Courses.xls'
PREREQ_LIST = 'Pre-requisite.xlsx'
TIME_TABLE = 'TIMETABLE.xls'
PENDING_BACKLOG = "Pending Backlog.xls"      #delete this after changing Pending Courses.xls or ACBBACKLOG.xls

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
        prereq_file = pd.read_excel(PREREQ_LIST, skiprows=1)
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

    def formPrereq(self):
        prereq_file = pd.read_excel(PREREQ_LIST, skiprows=1)
        or_and = ""
        for i in range(len(prereq_file['Subject'])):
            course1 = prereq_file['Subject'][i].strip(
            ) + prereq_file['Catalog'][i].strip()

            if str(prereq_file['preq1 subject'][i]) == 'nan':
                continue
            l = prereq_file['preq1 subject'][i].strip(
            ) + prereq_file['preq1 catalog'][i].strip()
            prereq[course1] = [l]
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
#######################################################################
            if str(prereq_file['preq2 sub'][i]) == 'nan':
                continue
            l = prereq_file['preq2 sub'][i].strip(
            ) + prereq_file['preq2 cat'][i].strip()
            prereq[course1].append(l)
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
#######################################################################

            if str(prereq_file['preq3 no'][i]) == 'nan':
                continue
            l = prereq_file['preq3 no'][i].strip(
            ) + prereq_file['preq3 cat'][i].strip()
            prereq[course1].append(l)
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)
#######################################################################

            if str(prereq_file['preq4 no'][i]) == 'nan':
                continue
            l = prereq_file['preq4 no'][i].strip(
            ) + prereq_file['preq4 cat'][i].strip()
            prereq[course1].append(l)
            if l not in isPrereqFor:
                isPrereqFor[l] = [course1]
            else:
                isPrereqFor[l].append(course1)

class SecondPage:

    def __init__(self):
        self.main_win = QMainWindow()
        self.ui = Ui_SecondPage()
        self.ui.setupUi(self.main_win)
        self.tableSlotClash = 0
        if student_id not in courseDict:
            courseDict[student_id] = ["No pending courses"]
        timetable = pd.read_excel(TIME_TABLE)

        global courseDictWithoutName
        courseDictWithoutName = []  # {CSF241,EEEF241}
        global courseToSections  # {CSF241: ["M-2","W-2"]}
        global courseToSectionsNotSelected
        global exam
        global count
        global courseNameForPreq
        global electives
        electives = []
        courseNameForPreq = ""
        count = {}
        exam = {}
        courseToSections = {}
        for i in courseDict[student_id]:
            courseDictWithoutName.append(i.split('-')[0])  # csf221

        self.ui.listWidget_1.addItems(courseDict[student_id])
        electives += courseDictWithoutName

        for i in range(len(timetable['Course ID'])):
            subject = timetable['Subject'][i]
            catalog = timetable['Catalog'][i].strip()
            title = timetable['Course Title'][i].strip()
            if (subject + catalog) not in electives:
                electives.append(subject + catalog)
                self.ui.listWidget_1.addItems([subject + catalog + "-" + title])



        self.ui.label_2.setText(student_name + " (" + student_id +")")

        for i in electives:
            count[i] = 0

        # timetable = pd.read_excel('sem 2 15-16tt-24 FEB 16.xlsx', skiprows=2)
        # for i in range(len(timetable['DAYS'])):
        # 	c = timetable['COURSENO'][i].split()[0]+timetable['COURSENO'][i].split()[1]
        # 	if c in courseDictWithoutName:
        # 		key = c+'-'+str(timetable['STAT'][i])+str(timetable['SEC'][i])
        # 		courseToSections[key] = timetable['DAYS'][i].split()

        for i in range(len(timetable['Exam Tm Cd'])):
            c = timetable['Subject'][i] + timetable['Catalog'][i].strip()
            if c in exam or str(timetable['Exam Tm Cd'][i]) == 'nan':
                continue
            exam[c] = timetable['Exam Tm Cd'][i]
        
        self.sectionToClassnbr = {}
        for i in range(len(timetable['Course ID'])):
            c = timetable['Subject'][i] + timetable['Catalog'][i].strip() + '-' + timetable['Section'][i].strip()
            self.sectionToClassnbr[c] = timetable['Class Nbr'][i]

        for i in range(len(timetable['Course ID'])):
            c = timetable['Subject'][i] + timetable['Catalog'][i].strip()
            if c in electives:
                key = c + '-' + str(timetable['Section'][i])
                if (key not in electives) and (key not in courseToSections):
                    courseToSections[key] = set()
                if str(timetable['Mtg Start'][i]) == 'nan':
                    continue
                l = self.giveTime(
                    timetable['Mtg Start'][i],
                    timetable['End time'][i],
                    timetable['Class Pattern'][i])
                # print(l)
                for el in l:
                    courseToSections[key].add(el)

   
        # print(courseToSections)
        courseToSectionsNotSelected = copy.copy(courseToSections)
        self.ui.pushButton_back.clicked.connect(self.pushButton_click)
        self.ui.listWidget_1.itemClicked.connect(self.courseClick)
        self.ui.listWidget.itemClicked.connect(self.sectionClickAdd)
        self.ui.listWidget_2.itemClicked.connect(self.sectionClickRemove)
        self.ui.pushButton1.clicked.connect(self.showPrereq)
        self.ui.pushButton.clicked.connect(self.validate)
        def calculate(s):
            count=dict()
            courses=pd.read_excel("Course_List_for_all_students.xls")
            for i in range(len(courses)):
                section = courses["Section"][i].split('-')[0]+courses["Section"][i].split('-')[1]
            count.update({section:int(count.get(section) or 0)+1})
            for i in range(len(courses)):
                section = courses["Section"][i].split('-')[0]+courses["Section"][i].split('-')[1]
                return count.get(s.split('-')[0]+s.split('-')[1])
                   
                self.ui.pushButton_2.clicked.connect(calculate())

        global days, tableWidgetMap
        tableWidgetMap = {}
        days = {'M': 0, 'T': 1, 'W': 2, 'TH': 3, 'F': 4, 'S': 5}

        if path.exists("stu_op#" + student_id + ".xls"):
            self.getXLS()

    def getXLS(self):
        self.setToValidate();
        self.ui.listWidgetErrors.clear()
        oldXLS = pd.read_excel("stu_op#" + student_id + ".xls")

        for i in range(len(oldXLS)):
            section = oldXLS["Section"][i]
            c = section.split('-')[0]
            count[c] = count[c] + 1
            courseToSectionsNotSelected.pop(section)
            self.ui.listWidget_2.addItems([section])
            schedule = courseToSections[section]
            for s in schedule:
                day = int(days[s.split('-')[0]])
                slot = int(s.split('-')[1])
                if (day, slot - 1) not in tableWidgetMap:
                    tableWidgetMap[day, slot - 1] = [section]
                else:
                    tableWidgetMap[day, slot - 1].append(section)
        self.formTable()

    def setToValidate(self):
        self.ui.pushButton.setText("Validate")
        
    def validate(self):
        if self.ui.pushButton.text() == "Validate":
            l1 = self.checkExamClash()
            l2 = self.checkPrereqClash()
            l = l1 + l2
            if self.tableSlotClash == 1:
                self.ui.listWidgetErrors.addItems(["Clash in time table slots. Check for Yellow Cells"])
            elif len(l) != 0:
                self.ui.listWidgetErrors.addItems(l)
            else:
                self.ui.listWidgetErrors.addItems(
                    ["No errors found. Click Save to generate output"])
                self.ui.pushButton.setText("Save")
        else:
            self.ui.listWidgetErrors.clear()

            op = pd.DataFrame(columns=['StudentID', 'StudentName', 'Section', 'ClassNbr'])
            for i in range(self.ui.listWidget_2.count()):
                courseSection = self.ui.listWidget_2.item(i).text()
                op.loc[i] = [student_id, student_name, courseSection, self.sectionToClassnbr[courseSection]]
            
            op.to_excel("stu_op#" + student_id + ".xls", index = False)
            self.ui.listWidgetErrors.addItems(["Saved Successfully !!"])

    # def generateOutput(self):

    def getDays(self, days):
        res = []
        for i in days:
            res += [str(i)]
            if i == 'H':
                res.pop()
                res[-1] += 'H'
        return res

    def giveTime(self, a, b, c):
        l = []
        s = int(str(a)[0:2]) - 7
        e = int(str(b)[0:2]) - 7
        if str(b)[3:5] != '00':
            e = e + 1
        d = self.getDays(c)
        for i in range(s, e):
            for j in d:
                l.append(j + '-' + str(i))

        return l

    def show(self):
        self.main_win.show()

    def pushButton_click(self):
        global main_win
        main_win = MainWindow(studentIDS)
        main_win.show()

    def courseClick(self, item):
        course = self.ui.listWidget_1.currentItem().text().split('-')[0]
        self.ui.listWidget.clear()
        f = False
        for i in courseToSectionsNotSelected:
            if i.split('-')[0] == course:
                f = True
                self.ui.listWidget.addItems([i])
        if f == False and count[course] == 0:
            self.ui.listWidget.addItems(["Course not offered this sem"])

    def formTable(self):
        self.tableSlotClash = 0

        for i in range(6):
            for j in range(11):
                if (i, j) not in tableWidgetMap:
                    continue
                else:
                    s = '//'.join(tableWidgetMap[(i, j)])
                    self.ui.tableWidget.setItem(i, j, QTableWidgetItem(s))
                    if len(tableWidgetMap[(i, j)]) > 1:
                        self.tableSlotClash = 1
                        self.ui.tableWidget.item(
                            i, j).setBackground(
                            QtGui.QColor(
                                255, 255, 0))

    def sectionClickAdd(self, item):
        self.setToValidate();
        self.ui.listWidgetErrors.clear()
        section = self.ui.listWidget.currentItem().text()
        if section == "Course not offered this sem":
            return
        c = section.split('-')[0]
        count[c] = count[c] + 1
        courseToSectionsNotSelected.pop(section)
        #def calculate(s):
        count_2=dict()
        courses=pd.read_excel("Course_List_for_all_students.xls")
        for i in range(len(courses)):
            sec = courses["Section"][i]
            count_2.update({sec:int(count_2.get(section) or 0)+1})
            
        #print(section)
        number=0
        if section in count_2:
            number=count_2.get(section)

        #print(section)
        #print(number)
        self.ui.listWidget_2.addItems([section+": "+str(number)])
        self.ui.listWidget.takeItem(self.ui.listWidget.currentRow())
        schedule = courseToSections[section]
        for s in schedule:
            day = int(days[s.split('-')[0]])
            slot = int(s.split('-')[1])
            if (day, slot - 1) not in tableWidgetMap:
                tableWidgetMap[day, slot - 1] = [section]
            else:
                tableWidgetMap[day, slot - 1].append(section)
        self.formTable()

    def sectionClickRemove(self, item):
        self.setToValidate();
        self.ui.listWidgetErrors.clear()
        section = self.ui.listWidget_2.currentItem().text().split(':')[0]
        c = section.split('-')[0]
        count[c] = count[c] - 1
        courseToSectionsNotSelected[section] = courseToSections[section]
        self.ui.listWidget_2.takeItem(self.ui.listWidget_2.currentRow())
        schedule = courseToSections[section]
        for s in schedule:
            day = int(days[s.split('-')[0]])
            slot = int(s.split('-')[1])
            tableWidgetMap[day, slot - 1].remove(section)

        if self.ui.listWidget_1.currentItem().text().split(
                '-')[0] == section.split('-')[0]:
            self.ui.listWidget.addItems([section])

        self.formTable()

    # def pushButton_prereq(self):
    #     course = self.ui.listWidget_1.currentItem().text().split('-')[0]
    #     # print(course)
    #     prereq_file = pd.read_excel(
    #         'Pre-requisite_15-07-2019.xlsx', skiprows=1)
    #     # print(prereq_file.columns)
    #     l = ""
    #     for i in range(len(prereq_file['Subject'])):
    #         course1 = prereq_file['Subject'][i].strip(
    #         ) + prereq_file['Catalog'][i].strip()
    #         if course == course1:
    #             l = prereq_file['preq1 subject'][i] + \
    # prereq_file['preq1 catalog'][i] + prereq_file['pereq1 title '][i]

    def checkExamClash(self):
        l = []
        for i in electives:
            for j in electives:
                if i == j:
                    continue
                if count[i] >= 1 and count[j] >= 1:
                    if i in exam and j in exam and  exam[i] == exam[j]:
                        l.append("Exam clash between " + i + " " + j)
                    elif i not in exam:
                        self.ui.listWidgetErrors.addItems(["Warning: exam dates for {} not in Timetable. Skipping exam clash for this course".format(i)])
                        break
        return l

    def checkPrereqClash(self):
        l = []
        for i in courseDictWithoutName:
            for j in courseDictWithoutName:
                if i == j:
                    continue
                if count[i] == 0 and count[j] >= 1 and j in prereq and i in prereq[j]:
                    l.append(j + " selected but it's prereq " + i + " is not")
        return l

    def showPrereq(self):
        courseNameForPreq = self.ui.listWidget_1.currentItem(
        ).text().split('-')[0]
        global prereqWindow
        prereqWindow = PreReq(courseNameForPreq)
        prereqWindow.show()

    
   

class PreReq:
    def __init__(self, courseNameForPreq):

        self.main_win = QMainWindow()
        self.ui = Ui_PreReq()
        self.ui.setupUi(self.main_win)
        if courseNameForPreq in prereq:
            self.ui.listWidgetLeft.addItems(prereq[courseNameForPreq])
        else:
            self.ui.listWidgetLeft.addItems([""])
        if courseNameForPreq in isPrereqFor:
            self.ui.listWidgetRight.addItems(isPrereqFor[courseNameForPreq])
        else:
            self.ui.listWidgetRight.addItems([""])

    def show(self):
        self.main_win.show()

def getPendingBacklog():
    back_list = pd.read_excel(ACB_BACKLOG_LIST)
    pending = pd.read_excel(PENDING_COURSE_LIST, skiprows = 1)

    for i in range(len(pending)):
        if pending['Campus ID'][i] not in list(back_list['Campus ID']):
            pending.drop(i,inplace=True)

    pending.to_excel(PENDING_BACKLOG)  

if __name__ == '__main__':
    pd.options.mode.chained_assignment = None
    app = QApplication(sys.argv)
    back_list = pd.read_excel(ACB_BACKLOG_LIST)
    if not path.exists(PENDING_BACKLOG):
        getPendingBacklog()

    merged = pd.read_excel(PENDING_BACKLOG)

    for i in range(len(back_list['NAME'])):
        if '.' in back_list['NAME'][i]:
            back_list['NAME'][i] = back_list['NAME'][i][:len(
                back_list['NAME'][i]) - 1]
    studentIDS = [
        x + "-" + y for x,
        y in zip(
            back_list['NAME'],
            back_list['Campus ID'])]
    for i in range(len(merged['Campus ID'])):
        if merged['Campus ID'][i] in courseDict:
            courseDict[merged['Campus ID'][i]].append(merged['Subject'][i].strip(
            ) + merged['Catalog'][i].strip() + '-' + merged['Course Name'][i])
        else:
            courseDict[merged['Campus ID'][i]] = [merged['Subject'][i].strip(
            ) + merged['Catalog'][i].strip() + '-' + merged['Course Name'][i]]
    # print(courseDict)





    main_win = MainWindow(studentIDS)
    main_win.show()
    sys.exit(app.exec_())
