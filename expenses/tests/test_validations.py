import pytest
from django.forms import ValidationError

from expenses.factories import ExpenseFactory, creditCardBillFactory


@pytest.fixture()
def expense_with_installments():
    expense_with_installments = ExpenseFactory(
        installments=True,
    )
    return expense_with_installments


@pytest.fixture()
def credit_card_expense():
    credit_card_expense = ExpenseFactory(
        credit_card_bill=creditCardBillFactory(),
    )
    credit_card_expense.account.account_type = "Credit Card"
    return credit_card_expense


@pytest.mark.django_db(transaction=True)
def test_installment_without_this_installment(expense_with_installments):
    """Tests if expense have a value for this_installment and number_of_installments"""
    with pytest.raises(ValidationError):
        expense_with_installments.full_clean()


@pytest.mark.django_db(transaction=True)
def test_this_installment_equal_or_below_zero(expense_with_installments):
    """Tests if this installment have a valid value"""
    expense_with_installments.this_installment = 0
    expense_with_installments.number_of_installments = 10
    with pytest.raises(ValidationError):
        expense_with_installments.full_clean()


@pytest.mark.django_db(transaction=True)
def test_number_of_installments_equal_or_below_zero(expense_with_installments):
    """Tests if number of installments have a valid value"""
    expense_with_installments.this_installment = 3
    expense_with_installments.number_of_installments = 0
    with pytest.raises(ValidationError):
        expense_with_installments.full_clean()


@pytest.mark.django_db(transaction=True)
def test_this_installment_greater_than_number_of_installments(
    expense_with_installments,
):
    """Tests if this installment is lower or equal to number of installments"""
    expense_with_installments.this_installment = 5
    expense_with_installments.number_of_installments = 1
    with pytest.raises(ValidationError):
        expense_with_installments.full_clean()


@pytest.mark.django_db(transaction=True)
def test_credit_card_bill_correct(credit_card_expense):
    assert credit_card_expense.full_clean() is None


@pytest.mark.django_db(transaction=True)
def test_credit_card_bill_incorrect(credit_card_expense):
    credit_card_expense.credit_card_bill = None
    with pytest.raises(ValidationError):
        credit_card_expense.full_clean()
