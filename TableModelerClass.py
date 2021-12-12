####################################################################################################################
from PyQt5 import QtCore
#setup of table view, counting the columns and the rows

class TableModeler(QtCore.QAbstractTableModel):
	def __init__(self, data):
		super(TableModeler, self).__init__()
		self._data = data

	def data(self, index, role):
		if role == QtCore.Qt.DisplayRole: 
			# See below for the nested-list data structure.
 			# .row() indexes into the outer list,
			# .column() indexes into the sub-list
			try:
				return self._data[index.row()][index.column()]
			except:
				pass


	def rowCount(self, index):
		# The length of the outer list.
		#print(len(self._data))
		return len(self._data)

	def columnCount(self, index):
		# The following takes the first sub-list, and returns
 		# the length (only works if all rows are an equal length)
		#print(len(self._data[0]))
		return len(self._data[0])

###################################################################################################################