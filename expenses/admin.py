from django.contrib import admin

from .models import Account, Category, Event, Expense, Store

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
        "event",
        "account",
        "value",
    )
