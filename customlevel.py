from PyQt5 import QtWidgets, uic, QtCore

import sys
from game import Game
import menu
import psycopg2


class Customlevel(QtWidgets.QDialog):
    upload_list ={}
    def __init__(self, name):
        self.user_name = name
        super(Customlevel, self).__init__()
        uic.loadUi('ui/customlevel1.ui', self)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.uploadButton.clicked.connect(self.custom_level)
        self.uploadButton.setAutoDefault(True)
        # quit and exit button
        self.quitButton.clicked.connect(self.back)
        self.exitButton.clicked.connect(self.exit)
        self.levelchoise()
        self.loadButton.clicked.connect(self.loadwords)
        self.clearButton.clicked.connect(self.clear)
        self.deleteButton.clicked.connect(self.del_level)
        



        
        


    def back(self):  # back to memu
        self.cams = menu.Menu(self.user_name)
        self.cams.show()
        self.close()

    def exit(self):  # close the game
        self.close()
        
    def custom_level(self):  # level and game time update -A        
        lvl_name = self.customLevelname.text()
        nl1 = self.customNL1.text()
        en1 = self.customEN1.text()

        # -------------------------------------------
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT level_name from custom_level where player_name ='{self.user_name}' AND level_name ='{lvl_name}'
            """)
        custom_levels = cur.fetchall()
        if custom_levels is None or cur.rowcount <20:
            cur.execute(f"""INSERT INTO custom_level (player_name,dutch_word,english_word,level_name) \
                        VALUES ('{self.user_name}','{nl1}','{en1}','{lvl_name}')
                                """)
        self.clear()
        cur.execute(f"""
            SELECT dutch_word,english_word from custom_level where player_name ='{self.user_name}' AND level_name ='{lvl_name}'
            """)
        global load_words 
        load_words = cur.fetchall()
        # for i in range(cur.rowcount):
        if cur.rowcount <= 20:
            self.displayword(load_words)
        conn.commit()
        conn.close()
        self.levelchoise()

    def levelchoise(self):#display dropdown
        self.levelSelect.clear()
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT distinct level_name FROM custom_level where player_name ='{self.user_name}' ORDER BY level_name
            """)
        my_levels = cur.fetchall()
        for i in my_levels:
            self.levelSelect.addItem(str(i[0]))
        conn.commit()
        conn.close()
    def getlevelvalue(self):
        # level select
        self.select_level = self.levelSelect.currentText()
    
    def loadwords(self):
        self.clear()
        self.getlevelvalue()
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            SELECT dutch_word,english_word
            FROM custom_level WHERE CASE WHEN player_name ='{self.user_name}' and level_name ='{self.select_level}' then 0 else 1 end=0 ORDER BY id
            """)
        global load_words 
        load_words= cur.fetchall()
        if cur.rowcount <= 20:
            self.displayword(load_words)
        
        conn.commit()
        conn.close()   
        
        
    def displayword(self,load):
        self.load=load
        try:
            self.dutchWord1.setText(f'1. {self.load[0][0]}')
            self.englishWord1.setText(f'1. {self.load[0][1]}')

            self.dutchWord2.setText(f'2. {self.load[1][0]}')
            self.englishWord2.setText(f'2. {self.load[1][1]}') 
            
            self.dutchWord3.setText(f'3. {self.load[2][0]}')
            self.englishWord3.setText(f'3. {self.load[2][1]}')

            self.dutchWord4.setText(f'4. {self.load[3][0]}')
            self.englishWord4.setText(f'4. {self.load[3][1]}')

            self.dutchWord5.setText(f'5. {self.load[4][0]}')
            self.englishWord5.setText(f'5. {self.load[4][1]}')

            self.dutchWord6.setText(f'6. {self.load[5][0]}')
            self.englishWord6.setText(f'6. {self.load[5][1]}')

            self.dutchWord7.setText(f'7. {self.load[6][0]}')
            self.englishWord7.setText(f'7. {self.load[6][1]}') 

            self.dutchWord8.setText(f'8. {self.load[7][0]}')
            self.englishWord8.setText(f'8. {self.load[7][1]}')

            self.dutchWord9.setText(f'9. {self.load[8][0]}')
            self.englishWord9.setText(f'9. {self.load[8][1]}')

            self.dutchWord10.setText(f'10 .{self.load[9][0]}')
            self.englishWord10.setText(f'10 .{self.load[9][1]}')

            self.dutchWord11.setText(f'11 .{self.load[10][0]}')
            self.englishWord11.setText(f'11 .{self.load[10][1]}')

            self.dutchWord12.setText(f'12 .{self.load[11][0]}')
            self.englishWord12.setText(f'12 .{self.load[11][1]}')

            self.dutchWord13.setText(f'13 .{self.load[12][0]}')
            self.englishWord13.setText(f'13 .{self.load[12][1]}')

            self.dutchWord14.setText(f'14 .{self.load[13][0]}')
            self.englishWord14.setText(f'14 .{self.load[13][1]}')

            self.dutchWord15.setText(f'15 .{self.load[14][0]}')
            self.englishWord15.setText(f'15 .{self.load[14][1]}')

            self.dutchWord16.setText(f'16 .{self.load[15][0]}')
            self.englishWord16.setText(f'16 .{self.load[15][1]}')

            self.dutchWord17.setText(f'17 .{self.load[16][0]}')
            self.englishWord17.setText(f'17 .{self.load[16][1]}')

            self.dutchWord18.setText(f'18 .{self.load[17][0]}')
            self.englishWord18.setText(f'18 .{self.load[17][1]}')

            self.dutchWord19.setText(f'19 .{self.load[18][0]}')
            self.englishWord19.setText(f'19 .{self.load[18][1]}')

            self.dutchWord20.setText(f'20 .{self.load[19][0]}')
            self.englishWord20.setText(f'20 .{self.load[19][1]}')
        except Exception as e:
            pass
    
    def clear(self):
        clear=[]
        for i in range(20):
            clear.append(('',''))
        
        self.displayword(clear)


    def del_level(self):
        self.getlevelvalue()
        conn = psycopg2.connect(database="FlashCards",
                                user="postgres",
                                password="1234",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""
            DELETE FROM custom_level WHERE CASE WHEN player_name ='{self.user_name}' and level_name ='{self.select_level}' then 0 else 1 end=0 
            """)
        conn.commit()
        conn.close()   
        self.clear()
        self.levelchoise()




