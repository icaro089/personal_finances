import datetime

import pytest

from expenses.factories import ExpenseFactory, creditCardBillFactory
from expenses.models import creditCardBill


@pytest.fixture()
def credit_card_expense():
    credit_card_expense = ExpenseFactory(date=datetime.date(2022, 4, 15))
    credit_card_expense.account.account_type = "Credit Card"
    return credit_card_expense


@pytest.mark.django_db(transaction=True)
def test_use_an_exising_credit_card_bill(credit_card_expense):
    "Tests if the credit_card_bill field in the model is automatically entered with the correct existing credit card bill"

    bill_correct = creditCardBillFactory.create(date=datetime.date(2022, 5, 9))
    creditCardBillFactory.create(date=datetime.date(2022, 4, 9))
    creditCardBillFactory.create(date=datetime.date(2022, 6, 9))
    credit_card_expense.save()
    assert credit_card_expense.credit_card_bill == bill_correct


@pytest.mark.django_db(transaction=True)
def test_create_a_credit_card_bill(credit_card_expense):
    "Tests if the credit_card_bill is automatically created"
    # bill_correct = creditCardBillFactory.create(date=datetime.date(2022, 5, 9))
    # credit_card_expense.credit_card_bill = bill_correct
    credit_card_expense.save()

    bill_created = creditCardBill.objects.filter(
        date__month=(credit_card_expense.date.month) + 1
    ).first()
    assert bill_created is not None
    assert credit_card_expense.credit_card_bill == bill_created
