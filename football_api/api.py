# flake8: noqa: E402
import logging
import sys
from os import path

from flask import Flask
from flask_restful import Api

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from football_api.constants import FANTASY_FOOTBALL_DATABASE, PROJECT_ROOT
from football_api.database import db
from football_api.resources.application_resource import APPLICATION_ENDPOINT, ApplicationResource
from football_api.resources.loan_offer_resource import LOAN_OFFER_ENDPOINT, LoanOfferResource
from football_api.resources.players_resource import PLAYERS_ENDPOINT, PlayersResource
from football_api.resources.seasons_resource import SEASONS_ENDPOINT, SeasonsResource
from football_api.resources.stats_resources import (
    STATS_ENDPOINT,
    STATS_PLAYER_ENDPOINT,
    STATS_SEASON_ENDPOINT,
    StatsPlayerResource,
    StatsResource,
    StatsSeasonResource,
)
from football_api.resources.teams_resource import TEAMS_ENDPOINT, TeamsResource
from football_api.resources.user_resource import USER_ENDPOINT, UserResource


def create_app(db_location):
    """
    Function that creates our Flask application.
    This function creates the Flask app, Flask-Restful API,
    and Flask-SQLAlchemy connection

    :param db_location: Connection string to the database
    :return: Initialized Flask app
    """
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(name)-12s %(levelname)-8s %(message)s",
        datefmt="%m-%d %H:%M",
        handlers=[logging.FileHandler("football_api.log"), logging.StreamHandler()],
    )

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_location

    with app.app_context():
        db.init_app(app)
        db.create_all()

    api = Api(app)
    api.add_resource(PlayersResource, PLAYERS_ENDPOINT, f"{PLAYERS_ENDPOINT}/<id>")
    api.add_resource(SeasonsResource, SEASONS_ENDPOINT)
    api.add_resource(StatsResource, STATS_ENDPOINT)
    api.add_resource(StatsPlayerResource, STATS_PLAYER_ENDPOINT)
    api.add_resource(StatsSeasonResource, STATS_SEASON_ENDPOINT)
    api.add_resource(TeamsResource, TEAMS_ENDPOINT, f"{TEAMS_ENDPOINT}/<id>")
    api.add_resource(UserResource, USER_ENDPOINT, f"{USER_ENDPOINT}/<id>")
    api.add_resource(ApplicationResource, APPLICATION_ENDPOINT, f"{APPLICATION_ENDPOINT}/<id>")
    api.add_resource(LoanOfferResource, LOAN_OFFER_ENDPOINT, f"{LOAN_OFFER_ENDPOINT}/<id>")

    return app


if __name__ == "__main__":
    app = create_app(f"sqlite:////{PROJECT_ROOT}/{FANTASY_FOOTBALL_DATABASE}")
    app.run(debug=True)
