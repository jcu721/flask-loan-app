"""
SQLAlchemy Model Definitions.
"""
from football_api.database import db


class User(db.Model):
    """User model for loan applicants."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"{self.id} - {self.last_name}, {self.first_name}"


class Application(db.Model):
    """Loan Application model."""
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.relationship("User", back_populates="applications")

    credit_score = db.Column(db.Integer)
    bankruptcies = db.Column(db.Integer)
    delinquincies = db.Column(db.Integer)

    monthly_debt = db.Column(db.Float)
    monthly_income = db.Column(db.Float)
    vehicle_value = db.Column(db.Float)
    loan_amount = db.Column(db.Float)

    def __str__(self):
        return f"{self.id} for <User: {self.user.id}>"


class LoanOffer(db.Model):
    """Loan Offer model."""
    __tablename__ = "loan_offers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.relationship("User", back_populates='loan_offers')
    application = db.relationship("Application", back_populates='loan_offers')

    apr = db.Column(db.Float)
    monthly_payment = db.Column(db.Float)
    term_length_months = db.Column(db.Integer)

    accepted = db.Column(db.Boolean)
    rejection_reason = db.Column(db.String)  # comma separated list of rejection reasons

    def __str__(self):
        return f"{self.uuid}, user: {self.user.id}, application: {self.application.id}"
