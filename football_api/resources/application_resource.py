import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from football_api.database import db
from football_api.models import Application
from football_api.schemas import ApplicationSchema

APPLICATION_ENDPOINT = "/api/application"
logger = logging.getLogger(__name__)


class ApplicationResource(Resource):
    def get(self, id=None):
        """
        ApplicationResource GET method.

        If no parameter provided, retrieves all users found in the database.

        If id is specifiecd, then that specific user instance is retrieved.

        :param id: Application ID to retrieve [optional]
        :return: Application, 200 HTTP status code
        """
        if not id:
            logger.info("Retrieving all applications")

            return self._get_all_applications(), 200

        logger.info(f"Retrieving application by id {id}")

        try:
            return self._get_application_by_id(id), 200
        except NoResultFound:
            abort(404, message=f"Application {id} not found")

    def _get_application_by_id(self, app_id):
        app = Application.query.filter_by(id=app_id).first()
        app_json = ApplicationSchema().dump(app)

        if not app_json:
            raise NoResultFound()

        logger.info(f"Application retrieved from database {app_json}")
        return app_json

    def _get_all_applications(self):
        apps = Application.query.all()

        apps_json = [ApplicationSchema().dump(app) for app in apps]

        logger.info("Applications successfully retrieved.")
        return apps_json

    def post(self):
        """
        ApplicationsResource POST method. Adds a new Application to the database.

        :return: Application.id, 201 HTTP status code.
        """
        app = ApplicationSchema().load(request.get_json())

        try:
            db.session.add(app)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this application is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            return app.id, 201
