from PyQt5 import QtWidgets, uic, QtCore
import sys
import os
import menu
import psycopg2
import hashlib


class Login(QtWidgets.QDialog):

    user_name = ""

    def __init__(self):
        super(Login, self).__init__()
        uic.loadUi('ui/login1.ui', self)
        self.pushButton.clicked.connect(self.login)
        # enter tusuyla da sonraki ikrana gidebilir -A
        self.pushButton.setAutoDefault(True)
        # login page ->cancel button -A
        self.pushButton_2.clicked.connect(self.cancel)
        self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
        self.show()

    def login(self):
        # login methode

        self.user_name = self.lineEdit_username.text()
        self.password = self.lineEdit_password.text()

        h=hashlib.md5()
        h.update(self.password.encode("utf-8"))
        self.hash_password=h.hexdigest()


        conn = psycopg2.connect(database="flashcard",
                                user="postgres",
                                password="12345",
                                host="localhost",
                                port="5432")
        cur = conn.cursor()
        cur.execute(f"""SELECT player_name,player_password from "players" WHERE player_name = '{self.user_name}' 
            """)
        user_veri = cur.fetchone()

        if user_veri is None:

            self.signup()

        else:
            if user_veri[1] == str(self.hash_password):
                self.cams = menu.Menu(self.user_name)
                self.cams.show()
                self.close()
            elif self.password == "" and self.user_name == "":
                self.login_info.setText(
                    "Please enter your username & password")
            elif self.password == "":
                self.login_info.setText("Please enter your password")
            else:
                self.login_info.setText(
                    "Invalid username password combination")
        conn.commit()
        conn.close()

    def signup(self):

        if self.password == "" and self.user_name == "":
            self.login_info.setText("Please enter your username & password")
        elif self.password == "":
            self.login_info.setText("Please enter your password")
        elif self.user_name == "":
            self.login_info.setText("Please enter your username")

        else:
            conn = psycopg2.connect("dbname=flashcard user=postgres password=12345")
            cur = conn.cursor()
            cur.execute('INSERT INTO Players VALUES(%s,%s,%s,%s)', (self.user_name,self.hash_password,1,0))
            cur.close()
            conn.commit()
            conn.close()

    def cancel(self):  # quit
        self.close()
