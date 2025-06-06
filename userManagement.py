import sqlite3 as sql
import bcrypt


# example
def getUsers():
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM id7-tusers")
    con.close()
    return cur


def insert_user(email, name, password):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO users (email,name,password,role) VALUES (?,?,?,'admin')",
                (email, name, password))
    con.commit()
    con.close()


def login(email, password):
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cur.fetchone()
    if user == None:
        con.close()
        return False
    else:
        hashed_password = user["password"]
        if bcrypt.checkpw(password.encode(), hashed_password):
            con.close()
            return user
