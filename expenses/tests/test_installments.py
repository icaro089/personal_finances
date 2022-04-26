from collections import namedtuple

import pytest
from dateutil.relativedelta import relativedelta

from expenses.factories import ExpenseFactory
from expenses.models import Expense

Installments = namedtuple("Installments", "this total")
installments_to_try = (Installments(1, 10), Installments(3, 5), Installments(8, 8))


@pytest.fixture(name="expense", params=installments_to_try)
def expense_with_installments(request):
    expense = ExpenseFactory(
        installments=True,
        this_installment=request.param.this,
        number_of_installments=request.param.total,
    )
    return expense


@pytest.mark.django_db(transaction=True)
def test_qnt_of_installments(expense):
    """Tests if the other expenses will be automatically created"""
    # Search for the other installments
    number_expenses = Expense.objects.filter(
        category=expense.category,
        store=expense.store,
        comments=expense.comments,
        value=expense.value,
    )
    # Checks if the number of installments is correct
    assert len(number_expenses) == (
        expense.number_of_installments - expense.this_installment + 1
    )


@pytest.mark.django_db(transaction=True)
def test_last_installment(expense):
    """Tests if the last installment is equal to the total number of installments"""
    # Get the last created expense
    last_installment = Expense.objects.last()
    # Checks if the last installment is equal to the total installments
    assert last_installment.this_installment == last_installment.number_of_installments


@pytest.mark.django_db(transaction=True)
def test_last_installment_date(expense):
    """Tests if the last installment has the correct date"""
    # Get the first date and the number of remaining installments
    first_date = expense.date
    qnt_installments = expense.number_of_installments - expense.this_installment

    # Get the last created expense
    last_installment = Expense.objects.last()

    # The last installment date must be equal to the first installment date
    # plus the number of remaining installments (months)
    assert last_installment.date == first_date + relativedelta(
        months=(qnt_installments)
    )
