from django.db import models
from dateutil.relativedelta import relativedelta
from subdomains.utils import reverse
from django.utils import timezone

from utils.models import get_unique_slug


class FinanceAccount(models.Model):
    """FinanceAccount (Finance)

    Indicates a finance account. Could be a bank account or a cash account
    such as having cash in a wallet."""

    # FinanceAccount types
    CASH = 0
    CURRENT = 1
    SAVINGS = 2
    FIXED_DEPOSIT = 3
    ACCOUNT_TYPES = (
        (CASH, 'Cash'), (CURRENT, 'Current'),
        (SAVINGS, 'Savings'), (FIXED_DEPOSIT, 'Fixed Deposit'))

    name = models.CharField(max_length=250)
    account_type = models.PositiveSmallIntegerField(
        default=CASH, choices=ACCOUNT_TYPES, db_index=True)
    amount = models.FloatField(default=0.0)

    slug = models.SlugField(
        max_length=256, unique=True, db_index=True, blank=True)

    class Meta(object):
        ordering = ['name', 'amount']
        verbose_name = 'Finance Account'
        verbose_name_plural = 'Finance Accounts'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                FinanceAccount, self, 'name', name=self.name)
        return super(FinanceAccount, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'finance:account', args=[self.slug], subdomain='finance')


class TransactionCategory(models.Model):
    """Transaction Category (Finance)

    Shows categories for transactions.
    Categories are groupings for transactions that are classified broadly.
    Categories are further expanded by tags that are not subcategories."""

    name = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=256, unique=True, db_index=True, blank=True)

    class Meta(object):
        ordering = ['name']
        verbose_name = 'Transaction Category'
        verbose_name_plural = 'Transaction Categories'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                TransactionCategory, self, 'name', name=self.name)
        return super(TransactionCategory, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'finance:category',
            args=[self.slug], subdomain='finance')


class TransactionTag(models.Model):
    """Transaction Tag (Finance)

    Describe financial transactions."""

    name = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=256, unique=True, db_index=True, blank=True)

    class Meta(object):
        ordering = ['name']
        verbose_name = 'Transaction Tag'
        verbose_name_plural = 'Transaction Tags'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.slug = get_unique_slug(
                TransactionTag, self, 'name', name=self.name)
        return super(TransactionTag, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'finance:transaction_tag',
            args=[self.slug], subdomain='finance')


class Transaction(models.Model):
    """Transaction (Finance)

    Transfer of money into or outside one of the accounts."""

    INCOME = 1
    EXPENSE = 2
    TRANSFERRED_INCOME = 3
    TRANSFERRED_EXPENSE = 4

    TRANSACTION_TYPES = (
        (INCOME, 'Income'), (EXPENSE, 'Expense'),
        (TRANSFERRED_INCOME, '(Transfer) Income'),
        (TRANSFERRED_EXPENSE, '(Transfer) Expense'))

    transaction_type = models.PositiveSmallIntegerField(
        default=EXPENSE, choices=TRANSACTION_TYPES, db_index=True)
    account = models.ForeignKey(FinanceAccount, related_name='transactions')
    date = models.DateField(blank=True, db_index=True)
    amount = models.FloatField()
    category = models.ForeignKey(
        TransactionCategory, related_name='transactions')
    tags = models.ManyToManyField(TransactionTag, related_name='transactions')
    note = models.TextField()

    class Meta(object):
        ordering = ['-date', 'id']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'

    def __str__(self):
        return '({account}) {date}: {amount}'.format(
            account=self.account.name, date=self.date, amount=self.amount)

    def save(self, *args, **kwargs):
        # first time save
        if self.pk is None:
            # set date to today
            if self.date is None:
                self.date = timezone.now().date()
            # check for negative amount
            if self.amount <= 0:
                raise ValueError('Transaction amount is not a positive value')
            # check for future date
            if self.date > timezone.now().date():
                raise ValueError(
                    'Future transactions are not allowed.'
                    'Use planned transactions.')
            # transact amount from account
            if self.transaction_type == Transaction.EXPENSE:
                self.account.amount -= self.amount
            elif self.transaction_type == Transaction.INCOME:
                self.account.amount += self.amount
            self.account.save()
            # transact amount from budget
            if self.transaction_type == Transaction.EXPENSE:
                budgets = Budget.objects.filter(
                    date_start__lte=timezone.now().date(),
                    date_end__gte=timezone.now().date())
                for budget in budgets:
                    budget.amount_remaining -= self.amount
                    budget.save()
        else:
            # check if amount has changed and update it
            this = Transaction.objects.get(pk=self.pk)
            if this.amount != self.amount:
                # amount has changed
                # re-enact transaction
                if self.transaction_type == Transaction.EXPENSE:
                    self.account.amount += this.amount
                    self.account.amount -= self.amount
                elif self.transaction_type == Transaction.INCOME:
                    self.account.amount -= this.amount
                    self.account.amount += self.amount
                self.account.save()
                # transact amount from budget
                if self.transaction_type == Transaction.EXPENSE:
                    budgets = Budget.objects.filter(
                        date_start__lte=timezone.now().date(),
                        date_end__gte=timezone.now().date())
                    for budget in budgets:
                        budget.amount_remaining += this.amount
                        budget.amount_remaining -= self.amount
                        budget.save()
        return super(Transaction, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'finance:transaction',
            args=[self.id], subdomain='finance')


class Budget(models.Model):
    """Budget (Finance)

    A budget is an allocation of funds from one or more accounts over a
    period of time that restricts the usage of expenditure."""

    ONCE = 0
    DAY = 1
    WEEK = 2
    MONTH = 3
    QUARTER = 4
    SEMI_ANNUAL = 5
    ANNUAL = 6

    BUDGET_PERIODS = (
        (DAY, 'Daily'), (WEEK, 'Weekly'), (MONTH, 'Monthly'),
        (QUARTER, 'Quarterly'), (SEMI_ANNUAL, 'Semi-Annually'),
        (ANNUAL, 'Annually'))

    name = models.CharField(max_length=256)
    amount = models.FloatField()
    amount_remaining = models.FloatField(blank=True)
    period = models.PositiveSmallIntegerField(
        default=MONTH, choices=BUDGET_PERIODS, db_index=True)
    # TODO: Budget types for considering only expenses or all transactions
    # type: absolute - only considers expenses
    # type: relative - considers incomes and expense
    date_start = models.DateField(db_index=True)
    date_end = models.DateField(blank=True, db_index=True)

    class Meta(object):
        ordering = ['-date_start', 'date_end']
        verbose_name = 'Budget'
        verbose_name_plural = 'Budgets'

    def __str__(self):
        return '{}: {} of {}'.format(
            self.name, self.amount_remaining, self.amount)

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError('Budget value should be positive')
        # NOTE: Keeping the budget start date check
        # in case I come back and say this is needed
        # if self.date_start > timezone.now().date():
        #     raise ValueError('Budget start date cannot be in the future')
        if self.pk is None:
            if self.amount_remaining is None:
                self.amount_remaining = self.amount
        if self.period == Budget.ONCE:
            if self.date_end is None:
                raise ValueError('Budget needs an ending date')
        elif self.period == Budget.DAY:
            self.date_end = self.date_start + relativedelta(days=1)
        elif self.period == Budget.WEEK:
            self.date_end = self.date_start + relativedelta(weeks=1)
        elif self.period == Budget.MONTH:
            self.date_end = self.date_start + relativedelta(months=1)
        elif self.period == Budget.QUARTER:
            self.date_end = self.date_start + relativedelta(months=3)
        elif self.period == Budget.SEMI_ANNUAL:
            self.date_end = self.date_start + relativedelta(months=6)
        elif self.period == Budget.ANNUAL:
            self.date_end = self.date_start + relativedelta(years=1)
        return super(Budget, self).save(*args, **kwargs)


class PlannedTransaction(models.Model):
    """Planned Transaction (Finance)

    A planned transaction is a transaction with its date set in the future.
    The transaction is automatically converted into a normal transaction
    on its given date. Planned transactions can include standing orders,
    rent payments, fees, etc. """

    ONCE = 0
    DAY = 1
    WEEK = 2
    MONTH = 3
    QUARTER = 4
    SEMI_ANNUAL = 5
    ANNUAL = 6

    REPEAT_PERIODS = (
        (ONCE, 'Once'),
        (DAY, 'Daily'), (WEEK, 'Weekly'), (MONTH, 'Monthly'),
        (QUARTER, 'Quarterly'), (SEMI_ANNUAL, 'Semi-Annually'),
        (ANNUAL, 'Annually'))

    transaction_type = models.PositiveSmallIntegerField(
        default=Transaction.EXPENSE,
        choices=Transaction.TRANSACTION_TYPES,
        db_index=True)
    account = models.ForeignKey(
        FinanceAccount, related_name='planned_transactions')
    date = models.DateField(blank=True, db_index=True)
    amount = models.FloatField()
    category = models.ForeignKey(
        TransactionCategory, related_name='planned_transactions')
    tags = models.ManyToManyField(
        TransactionTag, related_name='planned_transactions')
    note = models.TextField()

    repeat = models.PositiveSmallIntegerField(
        default=ONCE, choices=REPEAT_PERIODS, db_index=True)

    class Meta(object):
        ordering = ['-date']
        verbose_name = 'Planned Transaction'
        verbose_name_plural = 'Planned Transactions'

    def __str__(self):
        return '({account}) {date}: {amount}'.format(
            account=self.account.name, date=self.date, amount=self.amount)

    def save(self, *args, **kwargs):
        if self.amount <= 0:
            raise ValueError('Transaction amount should be a positive value')
        if self.date <= timezone.now().date():
            raise ValueError('Past transactions cannot be planned.')
        return super(PlannedTransaction, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'finance:planned_transaction',
            args=[self.id], subdomain='finance')

    def mark_complete(self):
        """mark the planned transaction as complete"""
        # instantiate the transaction
        transaction = Transaction()
        transaction.transaction_type = self.transaction_type
        transaction.account = self.account
        transaction.date = self.date
        transaction.amount = self.amount
        transaction.category = self.category
        transaction.note = self.note
        transaction.save()
        for tag in self.tags.all():
            transaction.tags.add(tag)
        transaction.save()

        # set next planned transaction date
        if self.repeat == PlannedTransaction.ONCE:
            self.delete()
        elif self.repeat == PlannedTransaction.DAY:
            self.date = self.date + relativedelta(days=1)
        elif self.repeat == PlannedTransaction.WEEK:
            self.date = self.date + relativedelta(weeks=1)
        elif self.repeat == PlannedTransaction.MONTH:
            self.date = self.date + relativedelta(months=1)
        elif self.repeat == PlannedTransaction.QUARTER:
            self.date = self.date + relativedelta(months=3)
        elif self.repeat == PlannedTransaction.SEMI_ANNUAL:
            self.date = self.date + relativedelta(months=6)
        elif self.repeat == PlannedTransaction.ANNUAL:
            self.date = self.date + relativedelta(years=1)


class TransferTransaction(models.Model):
    """Transfer Transaction (Finance)

    Money transferred from one account to another.
    Adds an expense in the first account,
    and an equivalent income in the second account."""

    account_from = models.ForeignKey(
        FinanceAccount, related_name='transfer_expenses')
    account_to = models.ForeignKey(
        FinanceAccount, related_name='transfer_incomes')
    date = models.DateField(blank=True, db_index=True)
    amount = models.FloatField()
    note = models.TextField()

    class Meta(object):
        ordering = ['-date']
        verbose_name = 'Transfer Transaction'
        verbose_name_plural = 'Transfer Transactions'

    def __str__(self):
        return '{}: {} {} to {}'.format(
            self.date, self.amount,
            self.account_from.name, self.account_to.name)

    def save(self, *args, **kwargs):
        if self.account_from == self.account_to:
            raise ValueError('Transfer cannot within the same accounts.')
        if self.date > timezone.now().date():
            raise ValueError('Transfer cannot have a future date.')
        if self.amount <= 0:
            raise ValueError('Transfer amount must be a positive value.')
        if self.pk is None:
            self.account_from.amount -= self.amount
            self.account_to.amount += self.amount
            self.account_from.save()
            self.account_to.save()
        return super(TransferTransaction, self).save(*args, **kwargs)
