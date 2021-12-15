from PyQt5 import QtWidgets, uic, QtCore

import sys
from game import Game
import menu
import psycopg2


class Statistics(QtWidgets.QDialog):

    def __init__(self, name):
        self.name = name
        super(Statistics, self).__init__()
        uic.loadUi('ui/statistics1.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        # quit and exit button
        self.quitButton.clicked.connect(self.back)
        self.exitButton.clicked.connect(self.exit)
        self.levelchoise()
        self.loadButton.clicked.connect(self.loadlevelpercent)

        self.myinfo()  # achievements load user informatie -A
        self.total_time()  # call total_time methode display total time -A

        self.levelranking()  # call methode for ranking in statistics page -A
        self.scoreboard() # call methode for score percentage in statistics page -A
        self.levelSelect.setCurrentIndex(self.level-2)

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
    

    def scoreboard(self):
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""SELECT player_name,average_percent, RANK() OVER (ORDER BY average_percent DESC) FROM PLAYERS
                    """)
        score = cur.fetchall()

        self.scoreRanking1.setText(
            f'{str(score[0][2])} . {str(score[0][0])}   ({str(score[0][1])}%)')
        self.scoreRanking2.setText(
            f'{str(score[1][2])} . {str(score[1][0])}   ({str(score[1][1])}%)')
        self.scoreRanking3.setText(
            f'{str(score[2][2])} . {str(score[3][0])}   ({str(score[2][1])}%)')
        self.scoreRanking4.setText(
            f'{str(score[3][2])} . {str(score[4][0])}   ({str(score[3][1])}%)')
        self.scoreRanking5.setText(
            f'{str(score[4][2])} . {str(score[5][0])}   ({str(score[4][1])}%)')
        my_score = ''
        for i in score:
            if i[0] == self.name:
                my_score = i[2]
                my_percent = i[1]
        self.scoreRankingU.setText(f'You are {str(my_score)} th\ntotal score is {my_percent}% ')  # my position--
        conn.commit()
        conn.close()



    def myinfo(self):
        # connetct database and display info ss
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
        self.myLevel.setText(f'{str(self.level)} / 250')  # display level -A
        
        cur.execute(f"""select level_id,level_percent DESC from LEVELS  Where player_name='{self.name}' ORDER BY level_percent DESC NULLS last
            """)
        max= cur.fetchone()
        self.high_score1.setText(f'Level {str(max[0])}')
        self.high_score2.setText(f'{str(max[1])} %')

        
        cur.execute(f"""select level_id,level_percent DESC from LEVELS  Where player_name='{self.name}' ORDER BY level_percent ASC NULLS last
                    """)
        min= cur.fetchone()
        self.low_score1.setText(f'Level {str(min[0])}')
        self.low_score2.setText(f'{str(min[1])} %')


        conn.commit()
        conn.close()

    def getlevelvalue(self):
        # level select
        self.select_level = self.levelSelect.currentText()

    def levelchoise(self):#display dropdown
        # self.levelSelect.clear()
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT level_id FROM levels where player_name ='{self.name}' and level_percent IS NOT NULL ORDER BY level_id
            """)
        my_levels = cur.fetchall()
        for i in my_levels:
            self.levelSelect.addItem(str(i[0]))

    def loadlevelpercent(self):
        self.getlevelvalue()
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""select level_id,level_percent 
        from LEVELS  Where player_name='{self.name}' and level_id ={self.select_level} 
                    """)
        slc= cur.fetchone()
        
        self.slcLevel.setText(f'Level {str(slc[0])}')
        self.slcPercent.setText(f'{str(slc[1])} %')