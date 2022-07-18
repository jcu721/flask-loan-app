# Loan Application REST API
Based off of the flask tutorial from [Building a RESTful API with Flask, Flask-RESTful, SQLAlchemy and pytest](https://ericbernier.com/flask-restful-api) blog post.

This app is a simple flask REST app backed by a SQLite database.
The app is a POC for a loan application that generates loan application
approvals and rejections based on the application criteria.

The app exposes the following three endpoints:
- GET, POST /api/user
- GET, POST /api/application
- GET /api/loan-offer

Users and loan applications can be created from the API using POST commands.
A valid loan application POST request will also create and calculate the
Loan Offer and return whether the application is rejected or approved.

A GET request for each resource yields all of the objects of that type
currently in the database.

## Prerequisites
- Python 3.9 installed
- pipenv installed
```bash
pip install pipenv
```

## Set Up

1. Install python dependencies with pipenv
```bash
pipenv install
```

2. Run the flask app

To start the Flask-RESTFul API run the following from the command line:
```bash
pipenv run python loan_app/api.py
```

This should create the SQLite database in a file named `loan_app.db` and start
a flask server running on port 5000.

## Entity Relation Diagram
Created with [ERAlchemy](https://pypi.org/project/ERAlchemy/).

![ERD](/erd_from_sqlite.pdf?raw=true)

## Using the API

A Postman json export has been provided,
![Postman JSON Export](/loan_app.postman_collection.json?raw=true), for ease of
playing around with the api.

Alternatively, use the following curl examples to add and inspect data:

Get all users:
`curl --location --request GET 'http://127.0.0.1:5000/api/user'`

Create user:
```bash
curl --location --request POST 'http://127.0.0.1:5000/api/user' \
--header 'Content-Type: application/json' \
--data-raw '{
    "first_name": "Nigel",
    "last_name": "Thornberry"
}'
```

Get Loan Applications:
```bash
curl --location --request GET 'http://127.0.0.1:5000/api/application'
```

Create Loan Application:
```bash
curl --location --request POST 'http://127.0.0.1:5000/api/application' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_id": 1,
    "credit_score": 820,
    "bankruptcies": 0,
    "delinquincies": 0,
    "monthly_debt": 3000,
    "monthly_income": 15000,
    "vehicle_value": 73000,
    "loan_amount": 55000
}'
```

Get Loan Offers:
```bash
curl --location --request GET 'http://127.0.0.1:5000/api/loan-offer'
```

## TODOs / Future Work:
- change the URLS to be better resource scoped, for ex. namespacing the
applications and loan offers under the user they belong to
- use UUIDs instead of integer IDs
- unit tests
- validations around user input. There's currently no validation around the
data, for ex. that the loan_amount be greater than 0 or credit score be in the
valid range.
