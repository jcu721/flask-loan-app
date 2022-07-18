import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from loan_app.calculations import calculate_loan
from loan_app.database import db
from loan_app.models import Application
from loan_app.schemas import ApplicationSchema, LoanOfferSchema

APPLICATION_ENDPOINT = "/api/application"
logger = logging.getLogger(__name__)


class ApplicationResource(Resource):
    """
    Expose REST GET and POST endpoints for the Application Resource.
    """

    def get(self, id=None):
        """
        ApplicationResource GET method.

        If no parameter provided, retrieves all applications found in the database.

        If id is specified, then that specific application instance is retrieved.

        @param id: Application ID to retrieve [optional]
        @returns Application, 200 HTTP status code
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
        ApplicationsResource POST method.

        Adds a new Application to the database and synchronously calculates the
        LoanOffer.

        @returns [Application, LoanOffer], 201 HTTP status code
        """
        app = ApplicationSchema().load(request.get_json())

        # TODO get this into a single transaction
        try:
            db.session.add(app)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this application is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")

        # calculate loan offer, then add new obj to db
        # (must be done after creating the application so it has the reference)
        loan_offer = calculate_loan(app)

        try:
            db.session.add(loan_offer)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Something went wrong saving the loan offer to db. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            app_serialized = ApplicationSchema().dump(app)
            loan_offer_serialized = LoanOfferSchema().dump(loan_offer)
            logger.info(f"Created new Application: {app_serialized} and LoanOffer: {loan_offer_serialized}")

            return_val = [app_serialized, loan_offer_serialized]
            return return_val, 201
