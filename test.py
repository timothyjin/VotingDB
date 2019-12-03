import sys
import re
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
    execute(sql_command)
    return cursor


def Create_Voter(SSN, first_name, middle_name, last_name, birthday, gender, ethnicity, income, party):
    sql_command = f"""INSERT INTO Voter VALUES ("{SSN}", "{first_name}", "{middle_name}", "{last_name}", "{birthday}", "{gender}", "{ethnicity}", {income}, "{party}");"""
    status = execute(sql_command)
    if status:
        print(f"Voter with SSN {SSN} has been created")


def Create_Ballot(voter_SSN, ID, position, year, submission_time, absentee):
    # Read candidates and votes on the ballot
    votes = []
    print('(Hit enter without input to stop reading votes for candidates...)')
    while True:
        cand_vote = str(input('<candidate_SSN> <vote_for (1 for yes, 0 for no)>: '))
        if not cand_vote:
            break
        votes.append(cand_vote)

    # Insert record into Ballot
    sql_command = f"""INSERT INTO Ballot VALUES ({ID}, "{position}", {year}, "{submission_time}", {absentee});"""
    status = execute(sql_command)
    if status:
        print(f"Ballot with ID {ID} has been created")

    # Insert records into RunsOn
    votes = [re.split(r'\s+', cand_vote) for cand_vote in votes]
    for v in votes:
        sql_command = f"""INSERT INTO RunsOn VALUES ("{position}", {year}, "{v[0]}", {ID}, {v[1]});"""
        status = execute(sql_command)
        if status:
            print(f"Vote on candidate {v[0]} has been recorded")


def Participation_Rate(position, year, number, state):
    sql_command = f"""SELECT COUNT(*) / (SELECT MAX(d.population) FROM District d WHERE d.year = {year} AND d.number = {number} AND d.state = "{state}")
    FROM LocatedIn l NATURAL JOIN Ballot b
    WHERE l.position = "{position}" AND l.year = {year} AND l.number = {number} AND l.state = "{state}";"""
    execute(sql_command)
    return cursor


def Custom_Query():
    sql_command = str(input('Query: '))
    execute(sql_command)
    return cursor


def execute(command):
    try:
        cursor.execute(command)
        return True
    except Exception as e:
        print(e)
    return False


def attribute_values(method):
    parameters = inspect.getfullargspec(method)[0]
    values = []
    for p in parameters:
        attr = input(p + ': ')
        if attr:
            values.append(attr)
        else:
            values.append(None)
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

# Main program loop
while True:
    choice = int(input(menu))

    if choice == 0:
        break
    elif choice not in options:
        print('Not a valid option.')
        continue

    # Call corresponding method and print results if applicable
    method = options[choice]
    result = getattr(sys.modules[__name__], method.__name__)(*attribute_values(method))
    if result:
        for t in result:
            print(t)
    print('------------------------------')

# close the connection
connection.commit()
connection.close()
print('Bye')
