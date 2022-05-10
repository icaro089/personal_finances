from django.contrib import admin

from .models import Account, Category, Event, Expense, Store, creditCardBill

# Register your models here.


admin.site.register(Event)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "account_type",
        "opening_balance",
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    ordering = (
        "category_type",
        "name",
    )


@admin.register(creditCardBill)
class creditCardBillAdmin(admin.ModelAdmin):
    ordering = ("-date",)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    ordering = ("name",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    ordering = (
        "-date",
        "category__category_type",
        "category",
    )
    list_display = (
        "date",
        "store",
        "category",
        "comments",
        "account",
        "value",
        "this_installment",
        "number_of_installments",
        "event",
        "checked",
        "credit_card_bill",
    )
    list_filter = (
        "date",
        "account",
        "category__category_type",
        "category",
        "installments",
        "credit_card_bill",
    )
    list_editable = ("checked", "credit_card_bill")
