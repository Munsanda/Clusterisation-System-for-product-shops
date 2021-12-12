#Created by Munsanda Elias Mweemba 2021 March
#-------------For user interface---------------------
from test1 import Ui_MainWindow	
from TableModelerClass import TableModeler
from PyQt5 import QtCore, QtWidgets
import sys

#---------------------------------------------------
#----------------------------------------------------
#To open a file
import subprocess
#import easygui## currently in use
from itertools import islice
#read xls file to pandas, and convert to list to display in tableview
import pandas as pd
#------------------
#Threading task modules 
from PyQt5.QtCore import QThreadPool, QRunnable, pyqtSlot
from PyQt5.QtWidgets import QMessageBox

from Clusterization import Clusterize
from Analysis import Analyze

import easygui

import matplotlib.pyplot as plt

#database
import pyodbc

import shutil

import os

#-------------------------------------------------------


"""
Variables:
	OpenFilePath 		--- path of the file
	DataInListForm 		---	File loaded into a list, to be used in analysis and clusterization
	TODO:status              --- Outputs the current status of the program




"""
########################################################################################################################
#Class on button click events
class Events(Ui_MainWindow, QtWidgets.QMainWindow, QRunnable):
	def __init__(self):
		super(Events,self).__init__()

		self.Recently_Open_Files = []
		self.setupUi(self)
		self.showMaximized()
		self.setWindowTitle("Market segmentation")
		self.ShowRecents()
		self.threadpool = QThreadPool()# to run a function on a different thread
		self.SaveList = list()

		self.QMessageBox = QMessageBox(self)



		#"Open Button clicked Events"
		#x = threading.Thread(target=thread_function, args=(1,))
		self.pushButton.clicked.connect(self.OpenFile)

		#Action Open Clicked Event
		#self.actionOpen.clicked.connect(self.OpenFile)
		#self.actionOpen.mousePressEvent = self.OpenFile
		self.actionOpen.triggered.connect(self.OpenFile)

		#move to left tab
		self.actionactionLeft.triggered.connect(self.ChangeTabFocusLeft)
		#move to right tab
		self.actionRight.triggered.connect(self.ChangeTabFocusRight)

		#"Label 19 Click Events "
		self.label_19.mousePressEvent = self.Label19Clicked
		self.label_20.mousePressEvent = self.Label20Clicked
		self.label_21.mousePressEvent = self.Label21Clicked

		#Analyze button
		self.pushButton_4.clicked.connect(self.AnalyzeFunction)
		#Clusterize button
		self.pushButton_5.clicked.connect(self.ClusterizeClicked)
		#Save project
		self.pushButton_6.clicked.connect(self.SaveProject)	

		
		

#######################################################################################################################

	def OpenFile(self):
		try:
			#Open File explorer to select code
			self.OpenFilePath = easygui.fileopenbox(default='*.xlsx',filetypes ='*.xlsx')

			if not self.OpenFilePath:
				pass
			else:
				self.label_16.setText(self.OpenFilePath)
				self.threadpool.start(self.ShowData)
		except easygui.Error as e:
			QMessageBox.about(self, 'File Opening', 'File not found')

#######################################################################################################################

	def SaveProject(self):
		self.statusBar().showMessage("Saving Project...")
		self.SaveList.append(self.OpenFilePath)
		self.SaveList.append(self.comboBox_1.currentText())
		self.SaveList.append(self.comboBox_2.currentText())
		self.SaveList.append(self.comboBox_3.currentText())
		self.SaveList.append(self.comboBox_4.currentText())
		self.SaveList.append(self.comboBox_5.currentText())
		self.SaveList.append(self.comboBox_6.currentText())

		directory = easygui.diropenbox(msg='Choose folder to save to?')

		with open(directory + "\\file.txt", "w") as output:
			output.write(str(self.SaveList))

		src = "C:/Users/User/Documents/DIPLOMNAYA_PYQT/temp"
		src_files = os.listdir(src)
		for file_name in src_files:
		    full_file_name = os.path.join(src, file_name)
		    if os.path.isfile(full_file_name):
		        shutil.copy(full_file_name, directory)

		self.statusBar().showMessage("Project saved")

		self.DBConnection()



######################################################################################################################
	def OpenProject(self):
		try:
			pass
		except:
			pass

######################################################################################################################
	def DBConnection(self):	
		db = pyodbc.connect('Driver={SQL Server};'
						'Server=MEMTHEKILLER\\SQLEXPRESS;'
						'Database=ClusterPro;'
						'Trusted_Connection=yes;') 


######################################################################################################################
#Open file from recent files
	def Label19Clicked(self,event):
		try:
			self.OpenFilePath = self.label_19.text()
			self.label_16.setText(self.OpenFilePath)
			self.threadpool.start(self.ShowData)
		except:
			pass

	def Label20Clicked(self,event):
		try:
			self.OpenFilePath = self.label_20.text()
			self.label_16.setText(self.OpenFilePath)
			self.threadpool.start(self.ShowData)
		except:
			pass

	def Label21Clicked(self,event):
		try:
			self.OpenFilePath = self.label_21.text()
			self.label_16.setText(self.OpenFilePath)
			self.threadpool.start(self.ShowData) # use threads to run the showdata function so as not to pause the UI
		except:
			pass

	def AnalyzeButtonClicked(self):
		#self.threadpool.start(self.AnalyzeFunction)
		pass


####################################################################################################################
#Show recently open files
	def ShowRecents(self):
		a_file = open("C:/Users/User/Documents/DIPLOMNAYA_PYQT/Recently_Open_Files.txt")
		number_of_lines = 3
		for line in reversed(list(open("C:/Users/User/Documents/DIPLOMNAYA_PYQT/Recently_Open_Files.txt"))):
			self.Recently_Open_Files.append(line.rstrip()) #opened from the last to the top because file is appended

		#append labels with recent files from recent file
		try:
			self.label_19.setText(self.Recently_Open_Files[0])
			self.label_20.setText(self.Recently_Open_Files[1])
			self.label_21.setText(self.Recently_Open_Files[2])
		except:
			pass

	def ChangeTabFocusLeft(self):
		self.TabWidget.setCurrentIndex(self.TabWidget.currentIndex() - 1)

	def ChangeTabFocusRight(self):
		self.TabWidget.setCurrentIndex(self.TabWidget.currentIndex() + 1)


####################################################################################################################
#Show data from xls file in tableview
	@pyqtSlot() #Runs in a a differnet thread so as to stop the program from pausing when loading huge files
	def ShowData(self):
		self.ComponentsDisable()
		self.statusBar().showMessage("Loading...")

		#Show raw data in the table one(1)
		self.df = pd.read_excel(self.OpenFilePath, header=0,sheet_name = "Sheet1",dtype=None) # can also index sheet by name or fetch all sheets
		self.DisplayAnalyzeOptions(len(self.df.columns))
		self.DataInListForm = self.df.values.tolist()[:30]

		self.model = TableModeler(self.DataInListForm)

		self.tableView.setModel(self.model)

		self.tableView.resizeColumnsToContents()
		self.tableView.resizeRowsToContents()

		#set focus to the tab 2
		self.TabWidget.setCurrentIndex(2)

		self.statusBar().clearMessage()

		#print(self.df.dtypes)

		#code for recent files and reenabliing of components
		self.ComponentsEnable()
		self.AppendRecentFiles()
		self.ShowRecents()


#######################################################################################################################
#Function to run the analyze class
	#@pyqtSlot() #Runs in a a differnet thread so as to stop the program from pausing when loading huge files
	def AnalyzeFunction(self):
		self.statusBar().showMessage("Analyzing...")
		self.df_after_analysis = Analyze(self.df, self.comboBox_1.currentText(), self.comboBox_2.currentText(),self.comboBox_3.currentText()).ret()
		self.statusBar().showMessage("Analyzing complete")


########################################################################################################################
#run the main baoy

	def ClusterizeClicked(self):
		self.statusBar().showMessage("Clusterizing")
		Clusterize(int(self.comboBox_4.currentText()),int(self.comboBox_5.currentText()),int(self.comboBox_6.currentText()),self.df_after_analysis)
		self.statusBar().showMessage("Clusterization complete")
		#print(self.df_after_analysis)

####################################################################################################################
#Help functions to display the options in the comboboxes 
	def DisplayAnalyzeOptions(self, NoOfcolumns):
		tempList = list(map(str,range(0,NoOfcolumns + 1)))
		self.comboBox_1.addItems(tempList)
		self.comboBox_2.addItems(tempList)
		self.comboBox_3.addItems(tempList)

		tempList = list(map(str,range(0,10)))
		self.comboBox_4.addItems(tempList)
		self.comboBox_5.addItems(tempList)
		self.comboBox_6.addItems(tempList)

	def ComponentsDisable(self):
		self.TabWidget.setTabEnabled(2, False);
		self.frame_6.setEnabled(False)

	def ComponentsEnable(self):
		self.TabWidget.setTabEnabled(2, True);
		self.frame_6.setEnabled(True)

	def AppendRecentFiles(self):
		#Save File name to recently opened	
		#print(self.label_18.text())
		if(((self.OpenFilePath != self.label_19.text()) and (self.OpenFilePath != self.label_20.text()) and (self.OpenFilePath != self.label_21.text())) == True):
			with open("C:/Users/User/Documents/DIPLOMNAYA_PYQT/Recently_Open_Files.txt", "a") as f:
				f.write(self.OpenFilePath + " \n" ) 



#Main loop
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ui = Events()
    ui.show()
    app.exec_()