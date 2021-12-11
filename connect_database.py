from sys import int_info
import psycopg2

conn = psycopg2.connect(database="FlashCards",
                        user="postgres", 
                        password="1234",
                        host="localhost", 
                        port="5432")

print("Opened database successfully")

cur = conn.cursor()
""" cur.execute("INSERT INTO Players (player_name,player_password,player_level,player_time) \
        VALUES ('cowboy', '123456', 98, 999 )");

cur.execute("INSERT INTO Players (player_name,player_password,player_level,player_time) \
        VALUES ('istanbul', '123456', 150, 99 )");

cur.execute("INSERT INTO Players (player_name,player_password,player_level,player_time) \
        VALUES ('dolar', '123456', 86, 363 )"); """



# cur.execute("""
#             SELECT player_name from "players" WHERE player_name = 'adil';
#             """)
# # display the result of executed SQL query
# info = cur.fetchall() # Select all rows from actor table
# # info = cur.fetchmany(50)
# for i in info:
#     print(i)

# cur.execute("""
#             SELECT dutch_word,english_word from "words" where word_level ='4' ORDER BY word_id LIMIT 20;
#             """)

name ='adil'

# cur.execute(f"""
#             SELECT player_level from PLAYERS where player_name ='{name}' 
#             """)

# cur.execute(f"UPDATE PLAYERS set player_level = 33 where player_name ='{name}'")
# count_t = 1000
# cur.execute(f"UPDATE PLAYERS set player_time = {count_t} where player_name ='{name}'")


# cur.execute(f"""
#             SELECT player_level,player_time from PLAYERS where player_name ='{name}'
#             """)
# info = cur.fetchone() 

# SELECT *  FROM PLAYERS WHERE AGE IN (19, 21);


# """ """ cur.execute(f"""SELECT player_name, player_level, RANK() OVER (ORDER BY player_level DESC) FROM PLAYERS
#                     """)
# info = cur.fetchall()
# for i in info:
#     print(i) """ """


""" cur.execute(f"SELECT player_name, player_level, RANK() OVER (ORDER BY player_level DESC) FROM PLAYERS") 
myranking = cur.fetchall()

dic_rank = {}
for i in myranking:
    if i[0] == name:
        my_rank = i[2] """
# print(my_rank)

# try:
cur = conn.cursor()
cur.execute(f"""SELECT player_name,player_password from "players" WHERE player_name = '{name}' 
            """)

user_list = cur.fetchone()
naam= 'adil'
password = '123456'
# if user_list[1] == password :
#     print("toghra pass") 
# else:
#     print(user_list[1])

# if userlist[0][1]
for i in user_list:
    popo = user_list[0]
print(popo)

if naam not in user_list:
    print('asadasd')
else:
    print('emes')






# print(myranking['adil'][2])
# cur.execute("SELECT COUNT(player_name) FROM PLAYERS")# cur.execute("""
# #             SELECT * from "players";
# #             """)
# info = cur.fetchone() 
# print(info)


# if name == info:
#     print("baken")
# else:
#     print("yokken")

# print(info[0])
# print(info[1])
# display the result of executed SQL query
# info = cur.fetchall() # Select all rows from actor table
# info = cur.fetchmany()



""" cur.execute('''CREATE TABLE COMPANY
        (ID INT PRIMARY KEY     NOT NULL,
        NAME           TEXT    NOT NULL,
        AGE            INT     NOT NULL,
        ADDRESS        CHAR(50),
        SALARY         REAL);''')
print("Table created successfully") """

conn.commit()
conn.close()


