from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtCore import QTime, QTimer
import menu
import sys
import psycopg2
from datetime import datetime


class Customgame(QtWidgets.QDialog):

    def __init__(self, name, level, count_t, select_value):
        self.settime = select_value
        self.name = name
        self.level = level
        self.count_t = count_t
        self.count_s = '00:00:00'
        self.count = int(self.settime)
        super(Customgame, self).__init__()
        uic.loadUi('ui/game_screen.ui', self)
        # when click beck button call func. back
        self.quitButton.clicked.connect(self.back)
        self.exitButton.clicked.connect(self.exit)
        self.levelNumber.setText(str(self.level))
        # disable window close button
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # game time
        self.total_time()
        self.gameTime.setText(self.count_s)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.total_time)
        self.timer1.start(1000)

        # when the game begin true and false button are disable
        self.pushButton.setEnabled(False)
        self.pushButton.toggle()
        self.pushButton_2.setEnabled(False)
        self.pushButton_2.toggle()
        # in game when click true & false button call methode
        self.pushButton.clicked.connect(self.true)
        self.pushButton_2.clicked.connect(self.false)

        self.show()
        # ----------QTimer------
        self.sleeptime.setText(str(self.count))
        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.timer_TimeOut)
        self.timer2.start(1000)
        # -----call the game methode
        self.load_words()

    def total_time(self):
        # methode for game time

        self.count_t += 1
        self.time = self.count_t
        self.time = int(self.time)
        self.day = self.time // (24 * 3600)
        self.time = self.time % (24 * 3600)
        self.hour = self.time // 3600
        self.time %= 3600
        self.minutes = self.time // 60
        self.time %= 60
        self.seconds = self.time
        if self.day != 0:
            self.count_s = "%02d:%02d:%02d:%02d" % (
                self.day, self.hour, self.minutes, self.seconds)
        elif self.day == 0:
            self.count_s = "%02d:%02d:%02d" % (
                self.hour, self.minutes, self.seconds)
        self.gameTime.setText(self.count_s)

    def timer_TimeOut(self):
        # methode for sleep time
        self.count -= 1
        if self.count == 0:
            # show the english word
            self.words.setText(self.word_list[self.index][1])
            self.language.setText('English')
            # let sleep time stop en wait for click
            self.timer2.stop()
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)

        self.sleeptime.setText(str(self.count))

    def back(self):
        self.level_update() 
        self.cams = menu.Menu(self.name)
        self.cams.show()
        self.close()

    def exit(self):
        self.level_update() 
        self.close()
    def level_update(self):  # level and game time update -A
        # -------------------------------------------
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(
                f"UPDATE PLAYERS set player_time = {self.count_t} where player_name ='{self.name}' ")
        conn.commit()
        conn.close()

    def true(self):  # click True +1 to c_true
        # set button disable
        self.pushButton.setEnabled(False)
        self.pushButton_2.setEnabled(False)
        # start sleep time
        self.timer2.start(1000)
        self.count = int(self.settime)
        # update sleep time
        self.sleeptime.setText(str(self.count))
        self.index += 1
        self.c_true += 1

        if self.index > 20:
            self.c_false -= 1

        if self.c_true == self.word_count:  # if c_true = 20 level +1 and begin new level
            # self.back()
            

            # self.c_true = 0
            self.c_false = 0

            self.point2.setText(str(self.c_false))
            self.point1.setText(str(self.c_true))
            self.levelNumber.setText(str(self.level))
            self.progressBar_ingame.setProperty("value", self.c_true)
            self.index = 0
            self.word_list = []
            self.timer2.stop()

        else:
            # show dutch word
            self.words.setText(self.word_list[self.index][0])

            self.point1.setText(str(self.c_true))
            self.point2.setText(str(self.c_false))

            self.language.setText('Nederlands')
            # updat progresbar
            self.progressBar_ingame.setProperty("value", self.c_true)

    def false(self):  # click false +1 to c_false and append this word to word_list -A
        # set button disable
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.timer2.start(1000)
        self.count = int(self.settime)
        self.sleeptime.setText(str(self.count))
        # append words to last of list
        self.word_list.append(self.word_list[self.index])
        if self.index < 20:
            self.c_false += 1
        self.point2.setText(str(self.c_false))
        self.index += 1
        self.words.setText(self.word_list[self.index][0])
        self.language.setText('Nederlands')

    def load_words(self):

        self.index = 0
        self.levelNumber.setText(str(self.level))
        self.word_list = []
        # connect to database & load words
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT dutch_word,english_word
            FROM custom_level WHERE CASE WHEN player_name ='{self.name}' and level_name ='{self.level}' then 0 else 1 end=0 ORDER BY id
            """)
        num = cur.rowcount
        self.progressBar_ingame.setMaximum(num)

        self.word_list = cur.fetchall()  # Select all rows from words table
        self.word_count= cur.rowcount
        conn.commit()
        conn.close()

        self.c_true = 0
        self.c_false = 0
        self.point1.setText(str(self.c_true))
        self.point2.setText(str(self.c_false))

        self.words.setText(self.word_list[self.index][0])
        self.language.setText('Nederlands')

