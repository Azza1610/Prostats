import sqlite3 as sql
import bcrypt


# example
def getUsers():
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM id7-tusers")
    con.close()
    return cur


def insert_driver(name, age, team_id):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("INSERT INTO drivers (name,age,team_id) VALUES (?,?,?)",
                (name, age, team_id))
    con.commit()
    con.close()


def list_drivers():
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT drivers.*, teams.*, SUM(race_results.points) AS total_points FROM drivers INNER JOIN teams ON drivers.team_id = teams.id LEFT JOIN race_results ON race_results.driver_id=drivers.id GROUP BY drivers.id ORDER BY total_points DESC").fetchall() 
    con.close()
    return data

def search_drivers(query):
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT * FROM drivers WHERE name LIKE ?",('%' + query + '%',)).fetchall() 
    con.close()
    return data

def delete_driver(driver_id):
    con = sql.connect("databaseFiles/database.db")
    cur = con.cursor()
    cur.execute("DELETE FROM drivers WHERE id = ?", (driver_id,))
    con.commit()
    con.close()

def search_races(query):
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT * FROM races WHERE race_name LIKE ? OR year LIKE?",('%' + query + '%','%' + query + '%')).fetchall() 
    con.close()
    return data

def get_driver(driver_id):
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT drivers.*, teams.*, SUM(race_results.points) AS total_points FROM drivers INNER JOIN teams ON drivers.team_id = teams.id LEFT JOIN race_results ON race_results.driver_id=drivers.id WHERE drivers.id = ? GROUP BY drivers.id", (driver_id,)).fetchone()
    con.close()
    return data

def list_races():
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT * FROM races").fetchall()
    con.close()
    return data

def get_races(driver_id):
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT * FROM race_results INNER JOIN races ON races.id=race_results.race_id WHERE driver_id = ?", (driver_id,)).fetchall()
    con.close()
    return data

def list_teams():
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT * FROM teams").fetchall()
    print(data)
    con.close()
    return data


def get_result(race_id):
    con = sql.connect("databaseFiles/database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    data = cur.execute("SELECT * FROM race_results INNER JOIN drivers ON race_results.driver_id=drivers.id INNER  JOIN races ON race_results.race_id = races.id WHERE race_id = ? ORDER BY position", (race_id,)).fetchall()
    print(data)
    con.close()
    return data

def search_player():
    pass
