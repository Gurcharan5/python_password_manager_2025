import sqlite3
import os
import getpass
import hashlib

length = 0

def reverse_ceasure(text):
    global length
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    orginal_message = ""

    for x in text:
        if x in lowercase:
            orginal_message += lowercase[(lowercase.index(x) - length) % 26]
        elif x in uppercase:
            orginal_message += uppercase[(uppercase.index(x) - length) % 26]
        else:
            orginal_message += x

    return orginal_message


def ceasur(text):
    global length
    lowercase = 'abcdefghijklmnopqrstuvwxyz'
    uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    new_message = ""

    for x in text:
        if x in lowercase:
            new_message += lowercase[(lowercase.index(x) + length) % 26]
        elif x in uppercase:
            new_message += uppercase[(uppercase.index(x) + length) % 26]
        else:
            new_message += x

    return new_message


def view_records():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    listOfTables = cur.execute("SELECT * FROM passwords").fetchall()
    for i in range(len(listOfTables)):
        website = reverse_ceasure(listOfTables[i][0])
        username = reverse_ceasure(listOfTables[i][1])
        password = reverse_ceasure(listOfTables[i][2])

        print("Record " + str(i + 1))
        print("Website: " + website)
        print("Username: " + username)
        print("Password: " + password)
        print("")

    con.close()
    main_menu()


def add_record():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    website = input("What is the website name? ")
    username = input("What is your username? ")
    password = input("What is your password? ")

    encrypted_website = ceasur(website)
    encrypted_username = ceasur(username)
    encrypted_password = ceasur(password)

    cur.execute("INSERT INTO passwords VALUES (?,?,?)", (encrypted_website, encrypted_username, encrypted_password,))
    con.commit()
    con.close()

    main_menu()


def main_menu():
    print("Please select an option:")
    print("1. View password manager records")
    print("2. Add a new password record")
    print("3. Delete password database")
    print("4. Log out")
    choice = input("")
    if choice == "1":
        view_records()
    elif choice == "2":
        add_record()
    elif choice == "3":
        delete_data()
    elif choice == "4":
        return
    else:
        print("You did not choose a valid option")
        main_menu()

def create_user_table():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    print("What do you want your master password to be?")
    masterPsw = getpass.getpass("").encode('utf-8')

    cur.execute("CREATE TABLE IF NOT EXISTS user(hash TEXT PRIMARY KEY)")
    cur.execute("CREATE TABLE IF NOT EXISTS passwords(website STRING PRIMARY KEY, username STRING, password STRING)")
    
    masterHash = hashlib.sha256(masterPsw).hexdigest()

    cur.execute("INSERT INTO user VALUES (?)", (masterHash,))
    con.commit()
    con.close()
    

def delete_data():
    os.remove("database.db")
    sqlite3.connect('database.db')
    

def validate_user():
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    print("Please enter your given password:")
    givenPsw = getpass.getpass("").encode('utf-8')
    givenPswHash = hashlib.sha256(givenPsw).hexdigest()

    row = cur.execute("SELECT hash FROM user WHERE hash = ?", (givenPswHash,)).fetchone()
    if row:
        print("Password correct.")
        con.close()
        global length 
        length = len(givenPsw)
        main_menu()
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

if __name__ == "__main__":
    check_if_table()

