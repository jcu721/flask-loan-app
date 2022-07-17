"""
Module for calculating whether Loan Applications are accepted or denied.

Using the following criteria for decision making:
    Credit bands for risk based pricing:
        Credit score	APR
        780+	        2.0%
        720-779	        5.0%
        660-719	        8.0%
        <660	        Decline

    Decline if:
    - Any bankruptcies reported
    - More than one delinquency reported
    - Debt-to-income ratio exceeds 60% (i.e. monthly debt payments including new loan offer monthly payment exceeds 60% of monthly income)
    - Loan-to-value ratio exceeds 100% (i.e. trying to borrow more money than the vehicle is currently worth)
"""
from football_api.models import LoanOffer

LOAN_OFFER_TERM = 72  # use 72 month term as default

LOAN_TO_VALUE_RATIO_THRESHOLD = 100  # decline beyond this threshold
DEBT_TO_INCOME_RATIO_THRESHOLD = 60  # decline beyond this threshold
BANKRUPTCY_LIMIT = 0
DELINQUENCY_LIMIT = 1
MINIMUM_CREDIT_SCORE = 660  # Minimum credit score for an application to be approved

# Official reasons to decline loan application
DECLINE_BANKRUPTCY = "Too many bankruptcies"
DECLINE_DELINQUENCY = "Too many delinquincies"
DECLINE_DEBT_TO_INCOME = "Debt to income ratio exceeds threshold"
DECLINE_LOAN_TO_VALUE = "Loan to value ratio exceeds threshold"
DECLINE_LOW_CREDIT_SCORE = "Credit score below threshold"


def calculate_loan(loan_application):
    """
    Calculate application accept/reject decision and calculate loan terms.
    """
    user_id = loan_application.user_id
    decline_reasons = []

    debt_to_income_ratio = (loan_application.monthly_debt / loan_application.monthly_income) * 100
    loan_to_value_ratio = (loan_application.loan_amount / loan_application.vehicle_value) * 100

    if loan_application.bankruptcies > BANKRUPTCY_LIMIT:
        decline_reasons.append(DECLINE_BANKRUPTCY)
    if loan_application.delinquincies > DELINQUENCY_LIMIT:
        decline_reasons.append(DECLINE_DELINQUENCY)
    if debt_to_income_ratio > DEBT_TO_INCOME_RATIO_THRESHOLD:
        decline_reasons.append(DECLINE_DEBT_TO_INCOME)
    if loan_to_value_ratio > LOAN_TO_VALUE_RATIO_THRESHOLD:
        decline_reasons.append(DECLINE_LOAN_TO_VALUE)
    if loan_application.credit_score < MINIMUM_CREDIT_SCORE:
        decline_reasons.append(DECLINE_LOW_CREDIT_SCORE)

    # if reasons to decline exist, return rejection info
    if decline_reasons:
        # create rejection LoanOffer
        # APR	monthly_payment	term_length_months	accept	reasons
        rejected_offer = LoanOffer(
            accepted=False,
            user_id=user_id,
            application_id=loan_application.id,
            rejection_reason=", ".join(decline_reasons)
        )
        return rejected_offer

    # calculate terms of the loan: APR and monthly rate
    # TODO credit bands, financial library
    accepted_offer = LoanOffer(
        accepted=True,
        user_id=user_id,
        application_id=loan_application.id,
        apr=2.5,
        monthly_payment=12
    )
    return accepted_offer
