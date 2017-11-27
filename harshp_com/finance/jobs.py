from django_rq import job
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Budget


@job
def renew_budgets():
    '''renew budgets that expire (today)
    Meant to be run daily'''
    today = timezone.now().date()
    budgets = Budget.objects.filter(
        date_end=today - relativedelta(days=1))
    for budget in budgets:
        new_budget = Budget()
        new_budget.name = budget.name
        new_budget.amount = budget.amount
        new_budget.amount_remaining = budget.amount_remaining
        new_budget.period = budgets.period
        new_budget.date_start = today
        new_budget.save()
