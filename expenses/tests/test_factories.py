import pytest

from expenses.factories import (
    AccountFactory,
    CategoryFactory,
    EventFactory,
    ExpenseFactory,
    StoreFactory,
)
from expenses.models import Account, Category, Event, Expense, Store


@pytest.mark.django_db(transaction=True)
def test_creating_account():
    account = AccountFactory()
    assert Account.objects.get(pk=account.pk)


@pytest.mark.django_db(transaction=True)
def test_creating_category():
    account = CategoryFactory()
    assert Category.objects.get(pk=account.pk)


@pytest.mark.django_db(transaction=True)
def test_creating_event():
    account = EventFactory()
    assert Event.objects.get(pk=account.pk)


@pytest.mark.django_db(transaction=True)
def test_creating_store():
    account = StoreFactory()
    assert Store.objects.get(pk=account.pk)


@pytest.mark.django_db(transaction=True)
def test_creating_expense():
    account = ExpenseFactory()
    assert Expense.objects.get(pk=account.pk)
