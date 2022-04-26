# Generated by Django 4.0.4 on 2022-04-12 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='installments',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='expense',
            name='this_installment',
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
    ]
