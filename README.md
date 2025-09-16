# api_sql_db

first steps

configure the data structure and create the ignore of data folder in gitignore

TO DO LIST

- Section 1: API
Created a function to post every table
created a function to erase data in tables in aim to test


- Section 2: SQL
Create metrics to see stats

- Bonus track
create test for all functions

1. Create the environtment with
 'python -m venv venv'
 to activate this: with 'source venv/bin/activate'

to run main.py FAST API REST API use
 uvicorn app.main:app --reload
use this to access swagger in whatever nav while running hte app:
 http://localhost:8000/docs


TO EXPLORE DB
sqlite3 test.db
SELECT * FROM departments;

HOW TO RUN DOCKER

docker build -t fastapi-app .
docker run -p 8000:8000 fastapi-app