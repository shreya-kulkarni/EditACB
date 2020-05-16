from os import listdir
import pandas as pd

fileList = listdir()

dfList = []

for file in fileList:
	if "stu_op#" in file:
		df = pd.read_excel(file)
		dfList.append(df)

if len(dfList) > 0:
	finalDf = pd.concat(dfList)
	finalDf.to_excel("Course_List_for_all_students.xls", index = False)

courses=pd.read_excel("Course_List_for_all_students.xls");
for i in range(len(courses)):
            section = oldXLS["Section"][i]
            c = section.split('-')[0]
            r=section.split('-')[1];
            count[c][r] = count[c][r] + 1
            print count[c][r]
           

