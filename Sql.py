import mysql.connector

con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)
cur = con.cursor()
cur.execute("SELECT * FROM Worker")
for row in cur.fetchall():
    print(row)
