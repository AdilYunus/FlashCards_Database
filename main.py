from PyQt5 import QtWidgets, uic
import sys
import os
import loading


app = QtWidgets.QApplication(sys.argv)
window = loading.Loading()
app.exec_()
