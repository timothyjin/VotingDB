import getpass
import mysql.connector as driver

user = 'root'
passwd = getpass.getpass('MySQL user password: ')
db_name = 'voting_db'

connection = driver.connect(user=user, password=passwd, database=db_name)
cursor = connection.cursor()

# SQL command to create a table in the database
sql_command = """CREATE TABLE IF NOT EXISTS Election(
year INTEGER PRIMARY KEY,
month INTEGER,
day INTEGER);"""

# execute the statement
cursor.execute(sql_command)

# SQL command to insert the data in the table
sql_command = """INSERT INTO Election VALUES (2018, 11, 6);"""
cursor.execute(sql_command)

# another SQL command to insert the data in the table
sql_command = """INSERT INTO Election VALUES (2016, 11, 8);"""
cursor.execute(sql_command)

# another SQL command to retrieve data in the table
sql_command = """SELECT * FROM Election;"""
cursor.execute(sql_command)
for y, m, d in cursor:
    print(y, m, d)

# To save the changes in the files. Never skip this.
# If we skip this, nothing will be saved in the database.
connection.commit()

# close the connection
connection.close()
