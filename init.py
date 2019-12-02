import os
import getpass
import mysql
import mysql.connector as driver

user = 'root'
passwd = getpass.getpass('MySQL user password: ')
db_name = 'voting_db'
data_file = 'commands.txt'

with open(data_file, 'r') as reader:
    content = reader.read()
    content.replace('\n', '')
    init_commands = [command.strip() + ';' for command in content.split(';') if command.strip()]


def insert_command_of(table, *argv):
    values = ','.join(argv)
    return 'INSERT INTO ' + table + ' (' + values + ');'


# Hardcoding sample data for now...
voters = [
('847364857', 'Martin', 'Lawrence', 'Sandoval', '1951-12-12', 'M', 'Caucasian', 84575, 'R'),
('048739615', 'Juan', 'Enrique', 'Perez', '1952-01-09', 'M', 'Hispanic', 37947, 'D'),
('958305816', 'James', 'Titus', 'White', '1983-01-03', 'M', 'African American', 29475, 'R'),
('047630571', 'Elizabeth', 'Anne', 'McGuinty', '1985-08-02', 'F', 'Caucasian', 95738, 'D'),
('856821148', 'Mary', 'Jessica', 'Parker', '1988-05-16', 'F', 'Caucasian', 48375, 'R'),
('946740385', 'Amanda', 'Margaret', 'Chen', '1990-08-20', 'F', 'Asian American', 53464, None),
('024836182', 'Franklin', 'Omar', 'Nyaga', '1995-10-29', 'M', 'African American', 109583, 'D'),
]

districts = [
(2020, 1, 'OH', 720000, 45039),
(2020, 2, 'OH', 693947, 37299),
(2020, 3, 'OH', 710384, 32918),
(2020, 1, 'MO', 402934, 49823),
(2016, 1, 'OH', 719800, 46129),
]

elections = [
('Ohio 3rd District Representative', 2020, 11, 3),
('Senator from Missouri', 2020, 11, 3),
('Governor of Ohio', 2020, 11, 3),
('Ohio 1st District Representative', 2016, 11, 8),
]

ballots = [
(1, 'Governor of Ohio', 2020, '9:00', 1),
(2, 'Governor of Ohio', 2020, '15:00', 0),
(3, 'Governor of Ohio', 2020, '12:30', 0),
(4, 'Governor of Ohio', 2020, '19:00', 0),
(5, 'Governor of Ohio', 2020, '10:15', 0)
]

candidates = [
('846398465', 'Nancy', 'Grace', 'Stewart', '1958-05-30', 'F', 'Caucasian', 'R'),
('057380482', 'Hillary', 'Rodham', 'Clinton', '1947-10-26', 'F', 'Caucasian', 'D'),
('736498562', 'Taina', 'Yadira', 'Flores', '1956-04-23', 'F', 'Hispanic', 'R'),
('287461948', 'Elijah', None, 'Cummings', '1968-04-12', 'M', 'African American', 'D'),
('283746928', 'John', 'Tyler', 'McMaster', '1972-07-23', 'M', 'Caucasian', None)
]


connection = driver.connect(user=user, password=passwd, database=db_name)
cursor = connection.cursor()

# Create tables
for command in init_commands:
    cursor.execute(command)

# Fill sample data
cursor.executemany('INSERT INTO Voter VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)', voters)
cursor.executemany('INSERT INTO District VALUES (%s, %s, %s, %s, %s)', districts)
cursor.executemany('INSERT INTO Election VALUES (%s, %s, %s, %s)', elections)
cursor.executemany('INSERT INTO Ballot VALUES (%s, %s, %s, %s, %s)', ballots)
cursor.executemany('INSERT INTO Candidate VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', candidates)
connection.commit()

# close the connection
connection.close()
