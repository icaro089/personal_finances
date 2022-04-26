from dateutil.relativedelta import relativedelta
from django.db.models import signals
from django.dispatch import receiver

from expenses.models import Expense


@receiver(signals.post_save, sender=Expense)
def create_other_installments(sender, instance, created, **kwargs):
    """When the field installment field is True, it automatically creates the other expenses for each of the ramaining installments"""

    if not instance.installments or not created:
        return

    first_installment = instance.this_installment
    last_installment = instance.number_of_installments

    if first_installment == last_installment:
        return

    new_expense = Expense.objects.get(pk=instance.pk)
    new_expense.pk = None
    new_expense.date += relativedelta(months=1)
    new_expense.this_installment += 1
    new_expense.save()
