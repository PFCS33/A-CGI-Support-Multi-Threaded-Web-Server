# import pymysql
import sqlite3
import sys

ini = sys.argv[1]
sid = ini.split("=")[1]


db = sqlite3.connect('database/student.db')
cursor = db.cursor()


sql = "SELECT * from student where id = " + sid + ";"
cursor.execute(sql)

data = cursor.fetchone()
if (not data):
    data = ["Not Exist", "Not Exist", "Not Exist"]
output = ""
with open("cgi-bin/query_res.html", "r") as f:
    for line in f:
        output += line
    output = output.replace("$id", data[0])
    output = output.replace("$name", data[1])
    output = output.replace('$class', data[2])

print(output)
