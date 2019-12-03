#!/bin/bash
export FLASK_APP=./src/main.py
conda.bat activate Databases
flask run -h 0.0.0.0