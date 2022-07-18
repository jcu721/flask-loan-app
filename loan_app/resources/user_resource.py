import logging

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from loan_app.database import db
from loan_app.models import User
from loan_app.schemas import UserSchema

USER_ENDPOINT = "/api/user"
logger = logging.getLogger(__name__)


class UserResource(Resource):
    def get(self, id=None):
        """
        UserResource GET method.

        If no parameter provided, retrieves all users found in the database.

        If id is specified, then that specific user instance is retrieved.

        @param id: User ID to retrieve [optional]
        @returns User, 200 HTTP status code
        """
        if not id:
            logger.info("Retrieving all users")

            return self._get_all_users(), 200

        logger.info(f"Retrieving user by id {id}")

        try:
            return self._get_user_by_id(id), 200
        except NoResultFound:
            abort(404, message=f"User {id} not found")

    def _get_user_by_id(self, user_id):
        user = User.query.filter_by(id=user_id).first()
        user_json = UserSchema().dump(user)

        if not user_json:
            raise NoResultFound()

        logger.info(f"User retrieved from database {user_json}")
        return user_json

    def _get_all_users(self):
        users = User.query.all()

        users_json = [UserSchema().dump(user) for user in users]

        logger.info("Users successfully retrieved.")
        return users_json

    def post(self):
        """
        UsersResource POST method. Adds a new User to the database.

        @returns User (json serialized), 201 HTTP status code
        """
        user = UserSchema().load(request.get_json())

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError as e:
            logger.warning(
                f"Integrity Error, this user is already in the database. Error: {e}"
            )

            abort(500, message="Unexpected Error!")
        else:
            logger.info(f"Created new user: {UserSchema().dump(user)}")
            return UserSchema().dump(user), 201
