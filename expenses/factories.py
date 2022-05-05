import datetime
import decimal

import factory
import factory.fuzzy

from expenses.models import Account, Category, Event, Expense, Store


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Account

    name = factory.Sequence(lambda index: f"Account {index}")
    account_type = "Credit Card"
    opening_balance = factory.Sequence(lambda index: decimal.Decimal(10.5 * index))


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda index: f"Category {index}")
    category_type = "Expense"


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    name = factory.Sequence(lambda index: f"Event {index}")


class StoreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Store

    name = factory.Sequence(lambda index: f"Store {index}")


class ExpenseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Expense

    date = factory.fuzzy.FuzzyDate(datetime.date(2022, 4, 1))
    category = factory.SubFactory(CategoryFactory)
    store = factory.SubFactory(StoreFactory)
    comments = factory.fuzzy.FuzzyText(length=100, prefix="Comment Factory")
    value = factory.fuzzy.FuzzyDecimal(-1000, 0)
    account = factory.SubFactory(AccountFactory)
    event = factory.SubFactory(EventFactory)
    installments = False
    this_installment = None
    number_of_installments = None
    checked = False
