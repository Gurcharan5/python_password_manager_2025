import sqlite3
import os
import getpass

######
###### NEED TO SWITCH FROM HASH AS THE VALUE CHANGES EVERY TIME THE PROGRAM IS RUN
######

def create_user_table():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    print("What do you want your master password to be?")
    masterPsw = getpass.getpass("")

    cur.execute("CREATE TABLE IF NOT EXISTS user(hash INTEGER PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS passwords(website STRING PRIMARY KEY, username STRING, password STRING)")
    
    masterHash = hash(masterPsw)
    print(masterHash)

    cur.execute("INSERT INTO user VALUES (?)", (masterHash,))#
    con.commit()
    con.close()
    

def delete_data():
    os.remove("database.db")
    sqlite3.connect('database.db')
    

def validate_user():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    print("Please enter your given password:")
    givenPsw = hash(getpass.getpass(""))
    print(givenPsw)

    row = cur.execute("SELECT hash FROM user WHERE hash = ?", (givenPsw,)).fetchone()
    if row:
        print("Password correct.")
        con.close()
    else:
        print("Password incorrect.")
        con.close()


def check_if_table():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    listOfTables = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'").fetchall()
    con.close()
    if len(listOfTables) >= 1:
        validate_user()
    else:
        create_user_table()


check_if_table()

