import logging

from flask_restful import Resource, abort
from sqlalchemy.orm.exc import NoResultFound

from loan_app.models import LoanOffer
from loan_app.schemas import LoanOfferSchema

LOAN_OFFER_ENDPOINT = "/api/loan-offer"
logger = logging.getLogger(__name__)


class LoanOfferResource(Resource):
    """
    Expose GET endpoint for LoanOffer Resource.
    """

    def get(self, id=None):
        """
        LoanOfferResource GET method.

        If no parameter provided, retrieves all loans found in the database.

        If id is specified, then that specific loan instance is retrieved.

        :param id: LoanOffer ID to retrieve [optional]
        :return: LoanOffer, 200 HTTP status code
        """
        if not id:
            logger.info("Retrieving all loans")

            return self._get_all_loans(), 200

        logger.info(f"Retrieving loan by id {id}")

        try:
            return self._get_loan_by_id(id), 200
        except NoResultFound:
            abort(404, message=f"LoanOffer {id} not found")

    def _get_loan_by_id(self, loan_id):
        loan = LoanOffer.query.filter_by(id=loan_id).first()
        loan_json = LoanOfferSchema().dump(loan)

        if not loan_json:
            raise NoResultFound()

        logger.info(f"loan retrieved from database {loan_json}")
        return loan_json

    def _get_all_loans(self):
        loans = LoanOffer.query.all()

        loans_json = [LoanOfferSchema().dump(loan) for loan in loans]

        logger.info("Loan Offers successfully retrieved.")
        return loans_json
