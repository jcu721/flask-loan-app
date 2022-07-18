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
import numpy_financial as npf

from loan_app.models import LoanOffer

LOAN_OFFER_TERM_MONTHS = 72  # use 72 month term as default

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

    @param Application loan_application
    @returns LoanOffer for either accepted or rejected offer
    """
    user_id = loan_application.user_id
    decline_reasons = calculate_automatic_decline_reasons(loan_application)

    # if reasons to decline exist, return rejection info
    if decline_reasons:
        # create rejection LoanOffer
        rejected_offer = LoanOffer(
            accepted=False,
            user_id=user_id,
            application_id=loan_application.id,
            rejection_reason=", ".join(decline_reasons)
        )
        return rejected_offer

    # calculate terms of the loan: APR and monthly rate
    apr = calculate_apr_from_credit(loan_application.credit_score)
    monthly_payment = calculate_monthly_payment(loan_application, apr)

    # create accepted loan offer
    accepted_offer = LoanOffer(
        accepted=True,
        user_id=user_id,
        application_id=loan_application.id,
        apr=apr,
        monthly_payment=monthly_payment,
        term_length_months=LOAN_OFFER_TERM_MONTHS
    )
    return accepted_offer


def calculate_automatic_decline_reasons(loan_application):
    """
    Calculate if any automatic reasons to decline exist and return the reasons or empty array.

    @param LoanApplication loan_application
    @returns array decline_reasons
    """
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

    return decline_reasons


def calculate_apr_from_credit(credit_score):
    """
    Calculate APR rate for a given credit score.

    @param int credit_score
    @returns float APR in percentage points.
    """
    if credit_score >= 780:
        return 2.0
    elif credit_score >= 720:
        return 5.0
    elif credit_score >= 660:
        return 8.0


def calculate_monthly_payment(application, apr):
    """
    Calculate loan monthly payment using numpy-financial.

    @param Application application
    @param float apr: APR in percentage points
    """
    payment = npf.pmt(
        apr / 100 / 12,
        LOAN_OFFER_TERM_MONTHS,
        application.loan_amount
    )

    return abs(payment)
