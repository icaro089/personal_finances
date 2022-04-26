import pytest
from django.forms import ValidationError

from expenses.factories import ExpenseFactory


@pytest.fixture(name="expense")
def expense_with_installments():
    expense = ExpenseFactory(
        installments=True,
    )
    return expense


@pytest.mark.django_db(transaction=True)
def test_installment_without_this_installment(expense):
    """Tests if expense have a value for this_installment and number_of_installments"""
    with pytest.raises(ValidationError):
        expense.full_clean()


@pytest.mark.django_db(transaction=True)
def test_this_installment_equal_or_below_zero(expense):
    """Tests if this installment have a valid value"""
    expense.this_installment = 0
    expense.number_of_installments = 10
    with pytest.raises(ValidationError):
        expense.full_clean()


@pytest.mark.django_db(transaction=True)
def test_number_of_installments_equal_or_below_zero(expense):
    """Tests if number of installments have a valid value"""
    expense.this_installment = 3
    expense.number_of_installments = 0
    with pytest.raises(ValidationError):
        expense.full_clean()


@pytest.mark.django_db(transaction=True)
def test_this_installment_greater_than_number_of_installments(expense):
    """Tests if this installment is lower or equal to number of installments"""
    expense.this_installment = 5
    expense.number_of_installments = 1
    with pytest.raises(ValidationError):
        expense.full_clean()
