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


def Create_Voter(SSN, name_first, name_middle, name_last, birthday, gender, ethnicity, income, party):
    sql_command = f"""INSERT INTO Voter VALUES ({SSN}, {name_first}, {name_middle}, {name_last}, {birthday}, {gender}, {ethnicity}, {income}, {party});"""
    status = execute(sql_command)
    if status:
        print(f"Voter with SSN {SSN} has been created")


def Create_Ballot(voter_SSN, ID, position, year, submission_time, absentee):
    # Read candidates and votes on the ballot
    votes = []
    print('(Hit enter without input to stop reading votes for candidates...)')
    while True:
        cand_vote = str(input('<candidate_SSN> <vote_for (yes: 1, no: 0)>: '))
        if not cand_vote:
            break
        votes.append(cand_vote)

    # Insert record into Ballot
    sql_command = f"""INSERT INTO Ballot VALUES ({ID}, {position}, {year}, {submission_time}, {absentee});"""
    status = execute(sql_command)
    if status:
        print(f"Ballot with ID {ID} has been created")

    # Insert records into RunsOn
    votes = [re.split(r'\s+', cand_vote) for cand_vote in votes]
    for v in votes:
        sql_command = f"""INSERT INTO RunsOn VALUES ({position}, {year}, "{v[0]}", {ID}, {v[1]});"""
        status = execute(sql_command)
        if status:
            print(f"Vote on candidate {v[0]} has been recorded")


def Update_Voter(SSN, name_first, name_middle, name_last, birthday, gender, ethnicity, income, party):
    # Check if given SSN exists
    sql_command = f"""SELECT * FROM Voter WHERE Voter.SSN = {SSN};"""
    execute(sql_command)
    matches = cursor.fetchall()
    if not matches:
        print(f"Voter with SSN {SSN} was not found")
        return None

    # Get all updated attributes
    attr_names = inspect.getfullargspec(Update_Voter)[0]
    updated_attributes = zip(attr_names, [SSN, name_first, name_middle, name_last, birthday, gender, ethnicity, income, party])
    updated_attribute_strings = [f"{attr[0]} = {attr[1]}" for attr in updated_attributes if attr[1]]

    sql_command = f"""UPDATE Voter SET {','.join(updated_attribute_strings)} WHERE SSN = {SSN};"""
    status = execute(sql_command)
    if status:
        print(f"Voter with SSN {SSN} updated")


def Update_Candidate(SSN, name_first, name_middle, name_last, birthday, gender, ethnicity, party):
    sql_command = f"""SELECT * FROM Candidate WHERE Candidate.SSN = {SSN};"""
    execute(sql_command)
    matches = cursor.fetchall()
    if not matches:
        print(f"Candidate with SSN {SSN} was not found")
        return None

    # Get all updated attributes
    attr_names = inspect.getfullargspec(Update_Candidate)[0]
    updated_attributes = zip(attr_names, [SSN, name_first, name_middle, name_last, birthday, gender, ethnicity, party])
    updated_attribute_strings = [f"{attr[0]} = {attr[1]}" for attr in updated_attributes if attr[1]]
    print(updated_attribute_strings)

    sql_command = f"""UPDATE Candidate SET {','.join(updated_attribute_strings)} WHERE SSN = {SSN};"""
    status = execute(sql_command)
    if status:
        print(f"Candidate with SSN {SSN} updated")


def Find_Candidates(position, year):
    sql_command = f"""SELECT Candidate.SSN, Candidate.name_first, Candidate.name_last, Candidate.party FROM Candidate NATURAL JOIN RunsOn WHERE RunsOn.position = {position} AND RunsOn.year = {year};"""
    execute(sql_command)
    return cursor


def Find_Election_Winner(position, year):
    sql_command = f"""
    SELECT SUM(RunsOn.vote_for), Candidate.name_first, Candidate.name_last, Candidate.party
    FROM Candidate NATURAL JOIN RunsOn
    WHERE RunsOn.position = {position} AND RunsOn.year = {year}
    GROUP BY Candidate.SSN
    ORDER BY SUM(RunsOn.vote_for) DESC;
    """
    execute(sql_command)
    return cursor


def Participation_Rate(position, year, number, state):
    sql_command = f"""SELECT COUNT(*) / (SELECT MAX(d.population) FROM District d WHERE d.year = {year} AND d.number = {number} AND d.state = {state})
    FROM LocatedIn l NATURAL JOIN Ballot b
    WHERE l.position = {position} AND l.year = {year} AND l.number = {number} AND l.state = {state};"""
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
            values.append(f'"{attr}"')
        else:
            values.append('NULL')
    return values


help_info = """
Create_*:
Enter relevant attribute values when prompted.
Any attribute values left blank will be NULL in the database.

Update_*:
Enter relevant attribute values when prompted.
Any attribute values left blank will remain the same as before.
However, non-null attributes must be re-entered.

Custom_Query:
Enter a valid SQL query command.
The results of that query will be displayed.

Enter 0 to save all changes and exit program.
Enter Ctrl+C to abort all changes and exit program.
"""

options = {
    '1': Create_Voter,
    '2': Create_Ballot,
    '3': Update_Voter,
    '4': Update_Candidate,
    '5': Find_Candidates, #('Senator from Missouri', 2020)
    '6': Find_Election_Winner,
    '7': Participation_Rate, #('Ohio 3rd District Representative', 2020, 3, 'OH'):
    '8': Custom_Query
}

# Main program loop
while True:

    for key in options:
        print(f'{key}. {options[key].__name__}')
    print('9. Help')
    print('0. Save & Exit')
    choice = input('> ')

    if choice == '9':
        print(help_info)
    elif choice == '0':
        break
    elif choice not in options:
        print('Not a valid option.')
    else: # Call corresponding method and print results if applicable
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
