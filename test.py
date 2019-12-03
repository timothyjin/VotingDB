import sys
import inspect
import getpass
import mysql
import mysql.connector as driver

user = 'root'
passwd = getpass.getpass('MySQL user password: ')
db_name = 'voting_db'

connection = driver.connect(user=user, password=passwd, database=db_name)
cursor = connection.cursor()


def Find_Candidates(position, year):
    sql_command = f"""SELECT Candidate.SSN, Candidate.name_first, Candidate.name_last, Candidate.party FROM Candidate NATURAL JOIN RunsOn WHERE RunsOn.position = "{position}" AND RunsOn.year = {year};"""
    cursor.execute(sql_command)
    return cursor


def Create_Voter(SSN, first_name, middle_name, last_name, birthday, gender, ethnicity, income, party):
    sql_command = f"""INSERT INTO Voter VALUES ("{SSN}", "{first_name}", "{middle_name}", "{last_name}", "{birthday}", "{gender}", "{ethnicity}", {income}, "{party}")"""
    try:
        cursor.execute(sql_command)
        print(f"Voter {name} has been created")
    except mysql.connector.errors.ProgrammingError as e:
        print(e)


def Create_Ballot(voter_SSN, ID, position, year, submission_time, absentee, candidate_SSN):
    sql_command = f"""INSERT_INTO Ballot VALUES ({ID}, "{position}", {year}, {submission_time}, {absentee})"""
    cursor.execute(sql_command)
    print(f"Ballot with ID {ID} has been created")


def Participation_Rate(position, year, number, state):
    sql_command = f"""SELECT COUNT(*) / (SELECT MAX(d.population) FROM District d WHERE d.year = {year} AND d.number = {number} AND d.state = "{state}")
    FROM LocatedIn l NATURAL JOIN Ballot b
    WHERE l.position = "{position}" AND l.year = {year} AND l.number = {number} AND l.state = "{state}";"""
    cursor.execute(sql_command)
    return cursor


def Custom_Query():
    sql_command = str(input('Query: '))
    cursor.execute(sql_command)
    return cursor


def attributes(method):
    parameters = inspect.getfullargspec(method)[0]
    values = []
    for p in parameters:
        attr = input(p + ': ')
        values.append(attr)
    return values


menu = """
1. Insert voter
2. Insert ballot
3. Find candidates
4. Find election winner
5. Get participation rate
6. Custom SQL query
0. Exit
> """

options = {
    1: Create_Voter,
    2: Create_Ballot,
    3: Find_Candidates, #('Senator from Missouri', 2020)
    4: None, # Find election winner
    5: Participation_Rate, #('Ohio 3rd District Representative', 2020, 3, 'OH'):
    6: Custom_Query
}

while True:
    choice = int(input(menu))

    if choice == 0:
        break
    elif choice not in options:
        print('Not a valid option.')
        continue

    method = options[choice]
    attribute_values = attributes(method)
    result = getattr(sys.modules[__name__], method.__name__)(*attribute_values)
    if result:
        for t in result:
            print(t)
    # TODO this only needs to be called after inserting records
    # connection.commit()
    print('------------------------------')

# close the connection
connection.close()
