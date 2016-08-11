from django.contrib import admin
from django.contrib import messages

from .models import FinanceAccount
from .models import TransactionCategory
from .models import TransactionTag
from .models import Transaction
from .models import Budget
from .models import PlannedTransaction
from .models import TransferTransaction


def calculate_expenditure(modeladmin, request, queryset):
    """calculate total expenditure (income - expense)"""
    total = 0
    for q in queryset:
        if q.transaction_type == Transaction.INCOME:
            total += q.amount
        elif q.transaction_type == Transaction.EXPENSE:
            total -= q.amount
    messages.add_message(
        request, messages.INFO, 'Total expenditure was {}'.format(total))


@admin.register(FinanceAccount)
class FinanceAccountAdmin(admin.ModelAdmin):
    """admin for Finance Accounts"""

    # date_hierarchy = ''
    fields = ('name', 'account_type', 'amount', 'slug')
    # filter_horizontal = ()
    list_display = ('name', 'account_type', 'amount')
    # list_display_editable = ()
    list_display_links = ('name', 'account_type', 'amount')
    list_filter = ('account_type',)
    # list_select_related = ()
    ordering = ('name', 'amount')
    prepopulated_fields = {'slug': ('name',)}
    radio_fields = {'account_type': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('name',)


@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    """admin for Transaction Category"""

    # date_hierarchy = ''
    fields = ('name', 'slug')
    # filter_horizontal = ()
    list_display = ('name',)
    # list_display_editable = ()
    list_display_links = ('name',)
    # list_filter = ()
    # list_select_related = ()
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # radio_fields = {'choice': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('name',)


@admin.register(TransactionTag)
class TransactionTagAdmin(admin.ModelAdmin):
    """admin for Transaction Tag"""

    # date_hierarchy = ''
    fields = ('name', 'slug')
    # filter_horizontal = ()
    list_display = ('name',)
    # list_display_editable = ()
    list_display_links = ('name',)
    # list_filter = ()
    # list_select_related = ()
    ordering = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    # radio_fields = {'choice': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """admin for Transaction"""

    actions = [calculate_expenditure]
    date_hierarchy = 'date'
    fields = (
        'transaction_type', 'account', 'date', 'amount',
        'category', 'tags', 'note')
    filter_horizontal = ('tags',)
    list_display = (
        'transaction_type', 'account', 'date', 'amount', 'category')
    # list_display_editable = ()
    list_display_links = (
        'transaction_type', 'account', 'date', 'amount', 'category')
    list_filter = ('transaction_type', 'account', 'category', 'tags')
    # list_select_related = ()
    ordering = ('-date', '-amount')
    # prepopulated_fields = {'slug': ('name')}
    radio_fields = {'transaction_type': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('note',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    """admin for Budget"""

    date_hierarchy = 'date_end'
    fields = (
        'name', 'amount', 'amount_remaining',
        'period', 'date_start', 'date_end')
    # filter_horizontal = ()
    list_display = ('name', 'amount', 'amount_remaining', 'date_end')
    # list_display_editable = ()
    list_display_links = list_display
    list_filter = ('period',)
    # list_select_related = ()
    ordering = ('-date_end',)
    # prepopulated_fields = {'slug': ('name')}
    radio_fields = {'period': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('name',)


@admin.register(PlannedTransaction)
class PlannedTransactionAdmin(admin.ModelAdmin):
    """admin for Planned Transaction"""

    date_hierarchy = 'date'
    fields = (
        'transaction_type', 'account', 'date', 'amount', 'repeat',
        'category', 'tags', 'note', )
    filter_horizontal = ('tags',)
    list_display = ('date', 'transaction_type', 'account')
    # list_display_editable = ()
    list_display_links = list_display
    list_filter = (
        'transaction_type', 'account', 'category', 'tags', 'repeat')
    # list_select_related = ()
    ordering = ('-date', '-amount')
    # prepopulated_fields = {'slug': ('name')}
    radio_fields = {
        'transaction_type': admin.HORIZONTAL,
        'repeat': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('account__name', 'category__name', 'note')


@admin.register(TransferTransaction)
class TransferTransactionAdmin(admin.ModelAdmin):
    """admin for Transfer Transaction"""

    date_hierarchy = 'date'
    fields = ('account_from', 'account_to', 'date', 'amount', 'note')
    # filter_horizontal = ()
    list_display = ('date', 'account_from', 'account_to', 'amount')
    # list_display_editable = ()
    list_display_links = list_display
    list_filter = ('account_from', 'account_to')
    # list_select_related = ()
    ordering = ('-date', '-amount')
    # prepopulated_fields = {'slug': ('name')}
    # radio_fields = {'choice': admin.HORIZONTAL}
    # readonly_fields = ()
    search_fields = ('note',)
