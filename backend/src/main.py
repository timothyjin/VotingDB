from flask import Flask, jsonify, request
from flask_cors import CORS
from .entities.entity import Session, engine, Base
from .entities.Voter import Voter, VoterSchema


app=Flask(__name__)
CORS(app)

# generate database schema
Base.metadata.create_all(engine)

@app.route('/')
def index():
    return jsonify("")

@app.route('/')
def add():
    pass
