#### Loan Application REST API with Flask, Flask-RESTful and SQLAlchemy
---

Jane Upshur's submission for the Tenet Back End Technical Assignment.

Based off of flask tutorial from [Building a RESTful API with Flask, Flask-RESTful, SQLAlchemy and pytest](https://ericbernier.com/flask-restful-api) blog post.


## Prerequisites
- Python 3.9 installed
- pipenv installed
```bash
pip install pipenv
```

## Set Up

#. Install python dependencies with pipenv
```bash
pipenv install
```

#. Run the flask app
To start the Flask-RESTFul API run the following from the command line:
```bash
$ python football_api/api.py
```

## TODOs / Future Work:
- change the URLS to be better resource scoped, for ex. namespacing the
applications and loan offers under the user they belong to
- use UUIDs instead of integer IDs
- unit tests
- validations around user input. There's currently no validation around the
data, for ex. that the loan_amount be greater than 0 or credit score be in the
valid range.
