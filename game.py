from PyQt5 import QtWidgets, uic, QtGui, QtCore,QtTest
from PyQt5.QtCore import QTime, QTimer
import menu
import sys
import psycopg2
from datetime import datetime


class Game(QtWidgets.QDialog):

    def __init__(self, name, level, count_t, select_value):
        self.settime = select_value
        self.name = name
        self.level = level
        self.count_t = count_t
        self.count_s = '00:00:00'
        self.count = int(self.settime)
        super(Game, self).__init__()
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
        self.level_update()  # call methode to level update -A
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
        cur.execute(f"""
            SELECT player_level from PLAYERS where player_name ='{self.name}'
            """)
        level_x = cur.fetchone()
        print('level-x=',level_x[0])
        print('self.level =',self.level)
        if level_x[0] < self.level:
            cur.execute(
                f"UPDATE PLAYERS set player_level = {self.level} where player_name ='{self.name}' ")
            print('112')
            cur.execute(
                f"UPDATE PLAYERS set player_time = {self.count_t} where player_name ='{self.name}' ")
            print('115')
            


            cur.execute(f"""SELECT player_name,CAST(AVG(level_percent) AS INTEGER) avg_percent 
                            FROM levels 
                            WHERE player_name = '{self.name}' 
                            GROUP BY player_name;""")
            my_avg = cur.fetchone()
            cur.execute(
                f"""UPDATE PLAYERS set player_level = {self.level},average_percent = {my_avg[1]},player_time = {self.count_t}
                where player_name ='{self.name}' """)
            print('126')

        else:
            cur.execute(
                f"UPDATE PLAYERS set player_time = {self.count_t} where player_name ='{self.name}' ")
            print('132')

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

        if self.c_true == 20:  # if c_true = 20 level +1 and begin new level

            self.percentupdate()
            #self.level += 1
            self.tebrik()#yeni eklendi

            self.c_true = 0
            self.c_false = 0

            self.point2.setText(str(self.c_false))
            self.point1.setText(str(self.c_true))
            self.levelNumber.setText(str(self.level))
            self.progressBar_ingame.setProperty("value", self.c_true)
            self.index = 0
            self.word_list = []
            if self.level == 251:
                self.timer2.stop()
                self.level = 1
                self.index = 0
                self.back()
                self.close()
            else:
                # call methode for begin new level
                self.load_words()

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
            SELECT dutch_word,english_word from "words" where word_level ={self.level} ORDER BY word_id LIMIT 20;
            """)
        self.word_list = cur.fetchall()  # Select all rows from words table
        conn.commit()
        conn.close()

        self.c_true = 0
        self.c_false = 0
        self.point1.setText(str(self.c_true))
        self.point2.setText(str(self.c_false))

        self.words.setText(self.word_list[self.index][0])
        self.language.setText('Nederlands')

    def percentupdate(self):
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT player_level from PLAYERS where player_name ='{self.name}'
            """)
        level_x = cur.fetchone()

        if level_x[0] == self.level:
            # 1 updat levels table -click_count and percentage
            # 2 insert new row to levels met level+=1 and nulls(click & percentage)
            # 3 update players table player_level and time and AVG_percentage
            cur.execute(
                f"UPDATE levels set click_count = {self.index} where case when player_name ='{self.name}' and level_id = {self.level} then 0 else 1 end=0; ")
            p = int(20/self.index*100)
            cur.execute(
                f"UPDATE levels set level_percent = {p} where case when player_name ='{self.name}' and level_id = {self.level} then 0 else 1 end=0; ")
            self.level += 1
            cur.execute(f"INSERT INTO levels (player_name,level_id) \
                        VALUES ('{self.name}', {self.level} )")
            # cur.execute(
            #     f"UPDATE PLAYERS set player_level = {self.level} where player_name ='{self.name}' ")
            # print('257')

            # cur.execute(f"""SELECT player_name,CAST(AVG(level_percent) AS INTEGER) avg_percent 
            #                 FROM levels 
            #                 WHERE player_name = '{self.name}' 
            #                 GROUP BY player_name;""")
            # my_avg = cur.fetchone()
            # cur.execute(
            #     f"""UPDATE PLAYERS set player_level = {self.level},average_percent = {my_avg[1]},player_time = {self.count_t}
            #     where player_name ='{self.name}' """)

            
            
        else:
            # 1 select click_count,if index < click_count
            # 2 update click_count and percentage
            # 3 level+=1
            cur.execute(f"""
                select click_count from levels where case when level_id ={self.level} and player_name ='{self.name}' then 0 else 1 end=0;
                """)
            click_x = cur.fetchone()

            if self.index < click_x[0]:
                p = int(20/self.index*100)
                cur.execute(
                    f"""UPDATE LEVELS set click_count = {self.index}, level_percent = {p}
                    where case when player_name ='{self.name}' and level_id = {self.level} then 0 else 1 end=0; """)
                cur.execute(f"""SELECT player_name,CAST(AVG(level_percent) AS INTEGER) avg_percent 
                            FROM levels 
                            WHERE player_name = '{self.name}' 
                            GROUP BY player_name;""")
                my_avg = cur.fetchone()
                cur.execute(
                        f"""UPDATE PLAYERS set player_level = {self.level},average_percent = {my_avg[1]},player_time = {self.count_t}
                        where player_name ='{self.name}' """)
                print('291')

                self.level += 1
                
            else:
                self.level += 1
                print('else')
        conn.commit()
        conn.close()

    def tebrik(self):
        self.pushButton_2.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.timer2.start(1000)
        self.count = int(self.settime)
        self.sleeptime.setText(str(self.count))
        # append words to last of list
        self.point2.setText(str(0))
        self.language.setText('Next')
