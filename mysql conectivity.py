import mysql.connector as mc
con=mc.connect(host='localhost',user='root',passwd='root',database='project')
if con.is_connected():
    print("Successfully connected")
cur=con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS TEMPPLAYERS(PLAYER_NAME varchar(30),
USER_ID varchar(30)PRIMARY KEY,
PASSWORD varchar(30),
WORDS_GUESSED char(30),
LEVEL_CURSED int(2)DEFAULT 0,
LEVEL_GHOST int(2)DEFAULT 0,
LEVEL_PHANTOM int(2)DEFAULT 0)''')
con.commit()

def insert_player_info(playername,userid,password):
    query = "INSERT INTO TEMPPLAYERS (PLAYER_NAME, USER_ID, PASSWORD) VALUES (%s, %s, %s)"
    cur.execute(query, (playername, userid, password))
    con.commit()
    print("Data added successfully")
name=input("Enter player's name")
userid=input("Enter your game userid")
password=input("Enter your password")
insert_player_info(name,userid,password)

def leaderboard():
    cur.execute('''CREATE OR REPLACE VIEW LEADERBOARD AS
               SELECT PLAYER_NAME, USER_ID, WORDS_GUESSED, LEVEL_PHANTOM, LEVEL_GHOST, LEVEL_CURSED FROM TEMPPLAYERS
               ORDER BY 
                   CAST(WORDS_GUESSED AS UNSIGNED) DESC,
                   LEVEL_PHANTOM DESC,
                   LEVEL_GHOST DESC,
                   LEVEL_CURSED DESC
               LIMIT 5''')
    cur.execute("SELECT * FROM LEADERBOARD")
    leaderboard_data = cur.fetchall()
    print("Leaderboard:")
    print("(PLAYER NAME,USER ID,WORDS GUESSED,CURSED,GHOST,PHANTOM)")
    for row in leaderboard_data:
        print(row)
con.commit()
leaderboard()

def verifier(username,password):
    if not username or not password:
        print("All fields are mandatory!")
    query = "SELECT * FROM TEMPPLAYERS WHERE USER_ID = %s AND PASSWORD = %s"
    cur.execute(query, (username, password))
    result = cur.fetchone()
    if result==None:
        print("Incorrect password or username... Please try again")
    else:
        print("Login successful!")
loginname=input("please eneter your username")
loginpassword=input("Enter your password")
verifier(loginname,loginpassword)


