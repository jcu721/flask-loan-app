# flake8: noqa: E402
import logging
import sys
from os import path

from flask import Flask
from flask_restful import Api

# TODO fix this local dependency namespace issue
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from loan_app.constants import LOAN_APP_DATABASE, PROJECT_ROOT
from loan_app.database import db
from loan_app.resources.application_resource import APPLICATION_ENDPOINT, ApplicationResource
from loan_app.resources.loan_offer_resource import LOAN_OFFER_ENDPOINT, LoanOfferResource
from loan_app.resources.user_resource import USER_ENDPOINT, UserResource


def create_app(db_location):
    """
    Creates the Flask app, Flask-Restful API, and Flask-SQLAlchemy connection.

    @param db_location: Connection string to the database
    @returns Initialized Flask app
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("loan_app.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location

    with app.app_context():
        db.init_app(app)
        db.create_all()

    api = Api(app)

    api.add_resource(UserResource, USER_ENDPOINT, f"{USER_ENDPOINT}/<id>")
    api.add_resource(ApplicationResource, APPLICATION_ENDPOINT, f"{APPLICATION_ENDPOINT}/<id>")
    api.add_resource(LoanOfferResource, LOAN_OFFER_ENDPOINT, f"{LOAN_OFFER_ENDPOINT}/<id>")

    return app


if __name__ == "__main__":
    app = create_app(f"sqlite:////{PROJECT_ROOT}/{LOAN_APP_DATABASE}")
    app.run(debug=True)
