import arrow
import calendar
from dateutil.relativedelta import relativedelta
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from subdomains.utils import reverse
from django.utils import timezone
import random

from .models import FinanceAccount
# from .models import TransactionCategory
# from .models import TransactionTag
from .models import Transaction
from .models import Budget
# from .models import PlannedTransaction
from .models import TransferTransaction


def _random_8bit():
    return random.randint(100, 200)


def auth(request):
    """Authenticate access to Journal"""
    # check if password is supplied via form
    if request.method == 'POST':
        password = request.POST.get('password', None)
        if password is None:
            return render(request, 'finance/auth.html')
        # authenticate the user is ME
        user = authenticate(username='harsh', password=password)
        # login the user
        if user is not None:
            login(request, user)
            return redirect('finance:home')
    # for all other cases, show the journal auth page
    return render(request, 'finance/auth.html')


def logout_user(request):
    """Log out the user"""
    # log the user out IF they are logged in
    if request.user.is_authenticated():
        logout(request)
    return redirect(reverse('home', subdomain=None))


def home(request):
    """finance homepage
    all accounts and their balance
    all budgets and their balance
    recent transactions including transfers
    """
    if not request.user.is_authenticated():
        return auth(request)

    accounts = FinanceAccount.objects.order_by('name')
    budgets = Budget.objects.filter(
        date_start__lte=timezone.now().date(),
        date_end__gte=timezone.now().date())
    transactions = Transaction.objects.order_by('-date')[:20]
    transfers = TransferTransaction.objects.order_by('-date')[:5]
    today = timezone.now().date()
    monthly_transactions = Transaction.objects.\
        filter(date__lte=today.replace(
            day=calendar.monthrange(today.year, today.month)[1])).\
        filter(date__gte=today.replace(day=1)).\
        filter(transaction_type=Transaction.EXPENSE).\
        order_by('-date')
    monthly_data = {}
    for transaction in monthly_transactions:
        if transaction.category.name not in monthly_data:
            monthly_data[transaction.category.name] = 0
        monthly_data[transaction.category.name] += transaction.amount

    monthly_data = [
        [category, amount,
            '#%02X%02X%02X' % (
                _random_8bit(), _random_8bit(), _random_8bit())]
        for category, amount in monthly_data.items()]
    monthly_data.sort(key=lambda x: x[1], reverse=True)
    monthly_data = [
        [category, '%.2f' % amount, color]
        for category, amount, color in monthly_data]

    return render(request, 'finance/homepage.html', {
        'accounts': accounts,
        'budgets': budgets,
        'transactions': transactions,
        'transfers': transfers,
        'monthly_data': monthly_data
    })


def monthly_spendings_list(request):
    '''show all months for selecting monthly spending'''
    if not request.user.is_authenticated():
        return auth(request)

    transactions = list(Transaction.objects.order_by('date'))
    months = {}
    for transaction in transactions:
        # add month/year if it doesn't exist in dict
        date = transaction.date.year * 100 + transaction.date.month
        if date not in months:
            months[date] = {
                'expense': 0,
                'income': 0,
            }
        month = months[date]
        if transaction.transaction_type == Transaction.EXPENSE:
            month['expense'] += transaction.amount
        else:
            month['income'] += transaction.amount

    # calculate net expenditure and set labels
    labels = []
    months_list = []
    for month, items in months.items():
        date = arrow.get(month // 100, month % 100, 1)
        labels.append(date.format('MMM YY'))
        month = months[month]
        month['net'] = month['income'] - month['expense']
        months_list.append((date.format('MMM YY'), reverse(
            'finance:monthly-spendings', args=(date.year, date.month))))

    expenses = [m['expense'] for _, m in sorted(months.items())]
    income = [m['income'] for _, m in sorted(months.items())]
    net_expenses = [m['net'] for _, m in sorted(months.items())]

    datasets = [
        {
            'label': 'Expenses',
            'backgroundColor': 'rgba(250,50,50,0.1)',
            'pointBackgroundColor': 'rgba(250,50,50,0.4)',
            'pointHoverRaduis': 30,
            'data': expenses,
        },
        {
            'label': 'Income',
            'backgroundColor': 'rgba(50,250,50,0.1)',
            'pointBackgroundColor': 'rgba(50,250,50,0.4)',
            'pointHoverRaduis': 30,
            'data': income,
        },
        {
            'label': 'Net Expense',
            'backgroundColor': 'rgba(50,50,250,0.1)',
            'pointBackgroundColor': 'rgba(50,50,250,0.4)',
            'pointHoverRaduis': 30,
            'data': net_expenses,
        },
    ]

    return render(request, 'finance/monthly_spendings_list.html', {
        'months': months_list[::-1],
        'labels': labels,
        'datasets': datasets
    })


def monthly_spendings(request, year, month):
    '''show monthly spencding for specified year and month'''
    if not request.user.is_authenticated():
        return auth(request)
    # they are received as strings
    year = int(year)
    month = int(month)

    month_start = arrow.get(int(year), int(month), 1)
    month_end = month_start + relativedelta(months=1, days=-1)
    monthly_transactions = Transaction.objects.\
        filter(date__lte=month_end.format('YYYY-MM-DD')).\
        filter(date__gte=month_start.format('YYYY-MM-DD')).\
        order_by('date')
    # filter(transaction_type=Transaction.EXPENSE).\
    # TODO: map-reduce / functools
    total_expenditure = 0
    net_expenditure = 0
    income = 0
    for transaction in monthly_transactions:
        if transaction.transaction_type == Transaction.EXPENSE:
            total_expenditure += transaction.amount
            net_expenditure -= transaction.amount
        else:
            income += transaction.amount
            net_expenditure += transaction.amount

    category_data = {}
    for transaction in monthly_transactions:
        if transaction.transaction_type != Transaction.EXPENSE:
            continue
        if transaction.category.name not in category_data:
            category_data[transaction.category.name] = 0
        category_data[transaction.category.name] += transaction.amount

    category_data = [
        [category, amount,
            '#%02X%02X%02X' % (
                _random_8bit(), _random_8bit(), _random_8bit())]
        for category, amount in category_data.items()]
    category_data.sort(key=lambda x: x[1], reverse=True)
    category_data = [
        [category, '%.2f' % amount, color]
        for category, amount, color in category_data]

    tag_data = {}
    for transaction in monthly_transactions:
        if transaction.transaction_type != Transaction.EXPENSE:
            continue
        for tag in transaction.tags.all():
            if tag.name not in tag_data:
                tag_data[tag.name] = 0
            tag_data[tag.name] += transaction.amount

    tag_data = [
        [tag, amount,
            '#%02X%02X%02X' % (
                _random_8bit(), _random_8bit(), _random_8bit())]
        for tag, amount in tag_data.items()]
    tag_data.sort(key=lambda x: x[1], reverse=True)
    tag_data = [
        [tag, '%.2f' % amount, color]
        for tag, amount, color in tag_data]

    transfers = TransferTransaction.objects.\
        filter(date__lte=month_end.format('YYYY-MM-DD')).\
        filter(date__gte=month_start.format('YYYY-MM-DD')).\
        order_by('date')

    day_data = {}
    for date in range(1, month_end.day + 1):
        day_data[date] = 0
    for transaction in monthly_transactions:
        if transaction.transaction_type != Transaction.EXPENSE:
            continue
        day_data[transaction.date.day] += transaction.amount
    day_data = list(day_data.items())
    day_data.sort(key=lambda x: x[0], reverse=False)
    day_data = {
        'labels': [d[0] for d in day_data],
        'datasets': [{
            'label': 'Expenditure breakdown by Day',
            'backgroundColor': 'rgba(50,50,250,0.1)',
            'pointBackgroundColor': 'rgba(50,50,250,0.4)',
            'pointHoverRaduis': 30,
            'data': [d[1] for d in day_data],
        }]
    }

    return render(request, 'finance/monthly_spendings.html', {
        'title': month_start.format('MMM YY'),
        # TODO: format to two decimal places
        'total_expenditure': total_expenditure,
        'net_expenditure': net_expenditure,
        'income': income,
        'category_data': category_data,
        'tag_data': tag_data,
        'transactions': monthly_transactions,
        'transfers': transfers,
        'day_data': day_data,
    })


def accounts(request):
    """accounts summary
    accounts with their balance
    recent transactions including transfers"""
    return redirect('finance:home')


def account(request, slug):
    """finance account summary
    transaction history"""
    return redirect('finance:home')


def categories(request):
    """transaction categories"""
    return redirect('finance:home')


def category(request, slug):
    """transaction category"""
    return redirect('finance:home')


def tags(request):
    """transaction tags"""
    return redirect('finance:home')


def tag(request, slug):
    """transaction tag"""
    return redirect('finance:home')


def budgets(request):
    """budgets
    budgets and their remaining balance"""
    return redirect('finance:home')


def budget(request, pk):
    """budget
    budget with balance
    recent transactions"""
    return redirect('finance:home')


def transactions(request):
    """transactions
    all transaction history"""
    return redirect('finance:home')


def transaction(request, pk):
    """transaction"""
    return redirect('finance:home')


def planned_transactions(request):
    """planned transactions
    """
    return redirect('finance:home')


def planned_transaction(request, pk):
    """planned transaction"""
    return redirect('finance:home')


def transfers(request):
    """transfer transactions"""
    return redirect('finance:home')


def transfer(request, pk):
    """transfer"""
    return redirect('finance:home')


def monthly_report(request, month):
    """financial monthly report"""
    return redirect('finance:home')
