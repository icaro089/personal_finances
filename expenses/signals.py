import datetime

from dateutil.relativedelta import relativedelta
from django.db.models import signals
from django.dispatch import receiver

from expenses.models import Expense, creditCardBill


@receiver(signals.pre_save, sender=Expense)
def correct_expense_value(sender, instance, **kwargs):
    if instance.category.category_type == "Expense" and instance.value > 0:
        instance.value = instance.value * (-1)
    if instance.category.category_type == "Income" and instance.value < 0:
        instance.value = instance.value * (-1)


@receiver(signals.pre_save, sender=Expense)
def create_credit_card_bill(sender, instance, **kwargs):
    """When a credit card is saved without the credit card bill, completes this field automatically"""
    if instance.credit_card_bill is not None:
        return

    bill_month = instance.date + relativedelta(months=1)
    card_bill = creditCardBill.objects.filter(
        date__month=bill_month.month, date__year=bill_month.year
    ).first()

    if card_bill is not None:
        instance.credit_card_bill = card_bill
    else:

        new_card_bill = creditCardBill.objects.create(
            date=datetime.date(bill_month.year, bill_month.month, 7)
        )
        instance.credit_card_bill = new_card_bill


@receiver(signals.post_save, sender=Expense)
def create_other_installments(sender, instance, created, **kwargs):
    """When the field installment field is True, it automatically creates the other expenses for each of the ramaining installments"""

    if not instance.installments or not created:
        return

    first_installment = instance.this_installment
    last_installment = instance.number_of_installments

    if first_installment is None or first_installment <= 0:
        return

    if last_installment is None or last_installment <= 0:
        return

    if first_installment >= last_installment:
        return

    new_expense = Expense.objects.get(pk=instance.pk)
    new_expense.pk = None
    new_expense.date += relativedelta(months=1)
    new_expense.this_installment += 1
    new_expense.checked = False
    new_expense.save()
