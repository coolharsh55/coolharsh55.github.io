import calendar
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

    def random_8bit():
        return random.randint(100, 200)

    monthly_data = [
        [category, amount,
            '#%02X%02X%02X' % (random_8bit(), random_8bit(), random_8bit())]
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
