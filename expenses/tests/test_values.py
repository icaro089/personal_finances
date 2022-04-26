import pytest

from expenses.factories import CategoryFactory, ExpenseFactory


@pytest.mark.django_db(transaction=True)
def test_expense_with_positive_value():
    """Tests if an expense with positive value is converted to negative"""
    expense = ExpenseFactory(value=1000)
    assert expense.value == -1000


@pytest.mark.django_db(transaction=True)
def test_income_with_negative_value():
    """Tests if an income with negative value is converted to positive"""
    category = CategoryFactory(category_type="Income")
    expense = ExpenseFactory(category=category, value=-1000)
    assert expense.value == 1000
