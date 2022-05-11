import datetime

import pytest
from dateutil.relativedelta import relativedelta

from expenses.factories import (
    AccountFactory,
    ExpenseFactory,
    creditCardBillFactory,
)
from expenses.models import creditCardBill


@pytest.fixture()
def credit_card_expense():
    credit_card_expense = ExpenseFactory()
    credit_card_expense.account.account_type = "Credit Card"
    return credit_card_expense


@pytest.mark.django_db(transaction=True)
def test_use_an_exising_credit_card_bill():
    "Tests if the credit_card_bill field in the model is automatically entered with the correct existing credit card bill"
    bill_correct = creditCardBillFactory.create(date=datetime.date(2022, 5, 9))
    creditCardBillFactory.create(date=datetime.date(2022, 4, 9))
    creditCardBillFactory.create(date=datetime.date(2022, 6, 9))

    new_account = AccountFactory(account_type="Credit Card")
    new_expense = ExpenseFactory(date=datetime.date(2022, 4, 15), account=new_account)

    assert new_expense.credit_card_bill == bill_correct
    assert len(creditCardBill.objects.all()) == 3


@pytest.mark.django_db(transaction=True)
def test_create_a_credit_card_bill(credit_card_expense):
    "Tests if the credit_card_bill is automatically created"
    new_date = credit_card_expense.date + relativedelta(months=1)
    bill_created = creditCardBill.objects.filter(
        date__year=new_date.year, date__month=new_date.month
    ).first()
    assert bill_created is not None
    assert credit_card_expense.credit_card_bill == bill_created
