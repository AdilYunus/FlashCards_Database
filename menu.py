from PyQt5 import QtWidgets, uic, QtCore

import sys
from game import Game
from customgame import Customgame
import psycopg2
from statistics import Statistics
from customlevel import Customlevel


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

        self.levelchoise()

        # en son geldigi level'i gosteriyor dropdown menu da -A
        self.levelSelect.setCurrentIndex(self.level-1)
        # S harfi ustunde tooltip -A
        self.staticsButton.setToolTip("click hier go to statics page")
        # A harfi ustunde Tooltip -A
        self.label_2A_f.setToolTip("About\nProduced by 4DATA")

        # after clicked go to statistics page
        self.staticsButton.clicked.connect(self.statistics)
        self.customButton.clicked.connect(self.customlevel)
        
        self.show()

    def play(self):
        self.getComboxBoxValue()
        self.getlevelvalue()
        print(self.select_level)
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT level_id FROM levels where player_name ='{self.name}' ORDER BY level_id
            """)        
        my_levels = cur.fetchall()
        level_list=[]
        for i in my_levels:
            level_list.append(str(i[0]))
        if self.select_level in level_list:
            
            self.cams = Game(self.name, int(self.select_level),
                            self.count_t, self.select_value)
        else:
            self.cams = Customgame(self.name, self.select_level,
                            self.count_t, self.select_value)
        self.cams.show()
        self.close()

        conn.commit()
        conn.close()


    def statistics(self):
        self.cams = Statistics(self.name)
        self.cams.show()
        self.close()

    def customlevel(self):
        self.cams = Customlevel(self.name)
        self.cams.show()
        self.close()

    def total_progress(self):  # total progress for total level(database) -A
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT player_level,player_time from PLAYERS where player_name ='{self.name}'
            """)
        from_db = cur.fetchone()
        # print(from_db)
        self.level = from_db[0]
        self.count_t = from_db[1]
        

        conn.commit()
        conn.close()
        return self.level*100/250


    def quit(self):  # quit methode-A
        self.close()

    def getComboxBoxValue(self):
        # bonus Timer
        self.select_value = self.setTime.currentText()

    def getlevelvalue(self):
        # level select
        self.select_level = self.levelSelect.currentText()
    
    def levelchoise(self):
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT level_id FROM levels where player_name ='{self.name}' ORDER BY level_id
            """)
        my_levels = cur.fetchall()
        for i in my_levels:
            self.levelSelect.addItem(str(i[0]))
        cur.execute(f"""
            SELECT distinct level_name FROM custom_level where player_name ='{self.name}' ORDER BY level_name
            """)
        my_levels = cur.fetchall()
        for i in my_levels:
            self.levelSelect.addItem(str(i[0]))
            
        
        
        conn.commit()
        conn.close()

