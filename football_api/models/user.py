from football_api.database import db


class User(db.Model):
    """
    User Flask-SQLAlchemy Model for loan applicants.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.last_name}, {self.first_name}"
