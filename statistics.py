from PyQt5 import QtWidgets, uic, QtCore

import sys
from game import Game
import menu
import psycopg2


class Statistics(QtWidgets.QDialog):

    def __init__(self, name):
        self.name = name
        super(Statistics, self).__init__()
        uic.loadUi('ui/statistics.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # quit and exit button
        self.quitButton.clicked.connect(self.back)
        self.exitButton.clicked.connect(self.exit)

        self.myinfo()  # achievements load user informatie -A
        self.total_time()  # call total_time methode display total time -A

        self.levelranking()  # call methode for ranking in statistics page -A

    def back(self):  # back to memu
        self.cams = menu.Menu(self.name)
        self.cams.show()
        self.close()

    def exit(self):  # close the game
        self.close()

    def total_time(self):
        # methode for second conver to time -A
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
        self.gameTime.setText(self.count_s)  # display the total time -A

    def levelranking(self):
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""SELECT player_name, player_level, RANK() OVER (ORDER BY player_level DESC) FROM PLAYERS
                    """)
        ranking = cur.fetchall()
        # display total user in statistics page
        self.userCount.setText(str(cur.rowcount))
        # level ranking top 5
        self.levelRanking1.setText(
            f'{str(ranking[0][2])} . {str(ranking[0][0])}   ({str(ranking[0][1])})')
        self.levelRanking2.setText(
            f'{str(ranking[1][2])} . {str(ranking[1][0])}   ({str(ranking[1][1])})')
        self.levelRanking3.setText(
            f'{str(ranking[2][2])} . {str(ranking[2][0])}   ({str(ranking[2][1])})')
        self.levelRanking4.setText(
            f'{str(ranking[3][2])} . {str(ranking[3][0])}   ({str(ranking[3][1])})')
        self.levelRanking5.setText(
            f'{str(ranking[4][2])} . {str(ranking[4][0])}   ({str(ranking[4][1])})')
        my_rank = ''
        for i in ranking:
            if i[0] == self.name:
                my_rank = i[2]
        self.levelRankingU.setText(f'You are {str(my_rank)} th')  # my position
        conn.commit()
        conn.close()

    def myinfo(self):
        # connetct database and display info
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
        self.level = from_db[0]
        self.count_t = from_db[1]
        self.userName.setText(self.name)  # display user name -A
        self.myLevel.setText(str(self.level))  # display level -A
        conn.commit()
        conn.close()
