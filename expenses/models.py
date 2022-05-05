from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Account(models.Model):
    ACCOUNT_TYPES = [
        ("Cash", "Cash"),
        ("Bank Account", "Bank Account"),
        ("Credit Card", "Credit Card"),
    ]

    name = models.CharField(max_length=25, unique=True)
    account_type = models.CharField(
        choices=ACCOUNT_TYPES, default="Cash", max_length=25
    )
    opening_balance = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return self.name


class Category(models.Model):
    CATEGORY_TYPES = [
        ("Expense", "Expense"),
        ("Income", "Income"),
        ("Transfer", "Transfer"),
    ]

    name = models.CharField(max_length=25, unique=True)
    category_type = models.CharField(
        choices=CATEGORY_TYPES, default="Expense", max_length=25
    )

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=125)

    def __str__(self):
        return self.name


class Expense(models.Model):
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    store = models.ForeignKey(Store, on_delete=models.SET_NULL, null=True)
    comments = models.CharField(max_length=125)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)
    installments = models.BooleanField(default=False)
    this_installment = models.IntegerField(default=None, null=True, blank=True)
    number_of_installments = models.IntegerField(default=None, null=True, blank=True)
    checked = models.BooleanField(default=False)

    def clean(self):
        if self.installments:
            if not self.this_installment:
                raise ValidationError(
                    _("Please, inform witch installment is this"),
                    code="this_installment_none",
                )
            if self.this_installment <= 0:
                raise ValidationError(
                    _("Field This Installment must be greater than zero"),
                    code="this_installment_number_error",
                )

            if not self.number_of_installments:
                raise ValidationError(
                    _("Please, inform the total number of installments"),
                    code="number_of_installments_none",
                )

            if self.number_of_installments <= 0:
                raise ValidationError(
                    _("Field Number Of Installments must be greater than zero"),
                    code="number_of_installments_number_error",
                )
            if self.number_of_installments < self.this_installment:
                raise ValidationError(
                    _(
                        "Number Of Installments must be equal or greater than This Installment"
                    ),
                    code="this_installment_greater_than_number_of_installments",
                )
