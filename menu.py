from PyQt5 import QtWidgets, uic, QtCore

import sys
from game import Game
import psycopg2
from statistics import Statistics


class Menu(QtWidgets.QDialog):

    def __init__(self, name):
        self.name = name
        super(Menu, self).__init__()
        uic.loadUi('ui/menu_with_statics.ui', self)
        self.label_username.setText(self.name)
        self.pushButton.clicked.connect(self.play)
        self.progressBar_menu.setProperty(
            "value", self.total_progress())  # call menu progressBar -A
        self.quitButton_2.clicked.connect(self.quit)  # menu page-> quit -A
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)

        # Calculate and display the levels that have been played -A
        for i in range(1, self.level+1):
            levels = str(i)
            self.levelSelect.addItem(levels)  # display the levels

        # en son geldigi level'i gosteriyor dropdown menu da -A
        self.levelSelect.setCurrentIndex(self.level-1)
        # S harfi ustunde tooltip -A
        self.staticsButton.setToolTip("click hier go to statics page")
        # A harfi ustunde Tooltip -A
        self.label_2A_f.setToolTip("About\nProduced by 4DATA")

        # after clicked go to statistics page
        self.staticsButton.clicked.connect(self.statistics)
        self.show()

    def play(self):
        self.getComboxBoxValue()
        self.getlevelvalue()
        # self.level_1 = int(self.select_level)
        self.cams = Game(self.name, self.select_level,
                        self.count_t, self.select_value)
        self.cams.show()
        self.close()

    def statistics(self):
        self.cams = Statistics(self.name)
        self.cams.show()
        self.close()

    def total_progress(self):  # total progress for total level(database) -A
        conn = psycopg2.connect(database="flashcard",
                                user="postgres",
                                password="12345",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT player_level,player_time from PLAYERS where player_name ='{self.name}'
            """)
        from_db = cur.fetchone()
        self.level = from_db[0]
        self.count_t = from_db[1]
        return self.level*100/250


    def quit(self):  # quit methode-A
        self.close()

    def getComboxBoxValue(self):
        # bonus Timer
        self.select_value = self.setTime.currentText()

    def getlevelvalue(self):
        # level select
        self.select_level = int(self.levelSelect.currentText())
