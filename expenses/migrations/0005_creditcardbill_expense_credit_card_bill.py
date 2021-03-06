# Generated by Django 4.0.4 on 2022-05-10 14:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0004_expense_checked'),
    ]

    operations = [
        migrations.CreateModel(
            name='creditCardBill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
            ],
        ),
        migrations.AddField(
            model_name='expense',
            name='credit_card_bill',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='expenses.creditcardbill'),
        ),
    ]
