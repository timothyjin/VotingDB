from flask import Flask, jsonify, request
from .entities.entity import Session, engine, Base
from .entities.Voter import Voter, VoterSchema


app=Flask(__name__)

# generate database schema
Base.metadata.create_all(engine)

# start session
session = Session()

# check for existing data
voters = session.query(Voter).all()

if len(voters) == 0:
    # create and persist dummy exam
    python_voter = Voter()
    session.add(python_voter)
    session.commit()
    session.close()

    # reload exams
    voters = session.query(Voter).all()

# show existing exams
print('### Voters:')
for voter in voters:
    print(f'({voter.SSN}) {voter.name} - {voter.Party}')



@app.route('/')
def index():
    return jsonify("")