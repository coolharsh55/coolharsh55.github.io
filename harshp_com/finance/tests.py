from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.test import TestCase

from .models import FinanceAccount
from .models import TransactionCategory
from .models import TransactionTag
from .models import Transaction
from .models import Budget
from .models import PlannedTransaction
from .models import TransferTransaction


class FinanceAccountTestCase(TestCase):
    """tests for Finance Account"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unique_names(self):
        account1 = FinanceAccount(
            name='name', account_type=FinanceAccount.CASH, amount=0)
        account1.save()
        account2 = FinanceAccount(
            name='name', account_type=FinanceAccount.CASH, amount=0)
        account2.save()
        self.assertNotEqual(account1.slug, account2.slug)


class TransactionCategoryTestCase(TestCase):
    """tests for Transaction Category"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unique_name(self):
        category1 = TransactionCategory(name='name')
        category1.save()
        category2 = TransactionCategory(name='name')
        category2.save()
        self.assertNotEqual(category1.slug, category2.slug)


class TransactionTagTestCase(TestCase):
    """tests for Transaction Tag"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_unique_name(self):
        tag1 = TransactionTag(name='name')
        tag1.save()
        tag2 = TransactionTag(name='name')
        tag2.save()
        self.assertNotEqual(tag1.slug, tag2.slug)


class TransactionTestCase(TestCase):
    """tests for Transaction"""

    def setUp(self):
        self.account = FinanceAccount(
            name='name', account_type=FinanceAccount.CASH, amount=0)
        self.account.save()
        self.category = TransactionCategory(name='name')
        self.category.save()
        self.tag = TransactionTag(name='name')
        self.tag.save()
        self.transaction = Transaction(
            transaction_type=Transaction.EXPENSE,
            account=self.account,
            date=timezone.now().date(),
            amount=1,
            category=self.category,
            note='note')

    def tearDown(self):
        pass

    def test_amount_positive(self):
        self.transaction.amount = -1
        with self.assertRaises(ValueError):
            self.transaction.save()

    def test_date_auto_set(self):
        self.transaction.date = None
        self.transaction.save()
        self.assertIsNotNone(self.transaction.date)

    def test_date_not_in_future(self):
        self.transaction.date = timezone.now().date() + relativedelta(days=1)
        with self.assertRaises(ValueError):
            self.transaction.save()

    def test_expense_amount_change(self):
        self.account.amount = 1
        self.account.save()
        self.transaction.save()
        self.assertEqual(self.account.amount, 0)

    def test_income_amount_change(self):
        self.account.amount = 0
        self.account.save()
        self.transaction.transaction_type = Transaction.INCOME
        self.transaction.save()
        self.assertEqual(self.account.amount, 1)

    def test_budget_amount_change(self):
        budget_current = Budget(
            name='current', amount=10, period=Budget.MONTH,
            date_start=timezone.now().date())
        budget_current.save()
        budget_expired = Budget(
            name='expired', amount=10, period=Budget.MONTH,
            date_start=timezone.now().date() - relativedelta(months=2))
        budget_expired.save()
        transaction = Transaction(
            transaction_type=Transaction.EXPENSE,
            account=self.account,
            date=timezone.now().date(),
            amount=10,
            category=self.category,
            note='note')
        transaction.save()
        self.assertEqual(
            Budget.objects.get(pk=budget_current.pk).amount_remaining, 0)
        self.assertEqual(
            Budget.objects.get(pk=budget_expired.pk).amount_remaining, 10)


class BudgetTestCase(TestCase):
    """tests for Budget"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_amount_positive(self):
        budget = Budget(
            name='name', amount=0, period=Budget.MONTH,
            date_start=timezone.now().date())
        with self.assertRaises(ValueError):
            budget.save()

    def test_budget_end_dates(self):
        # ONCE
        budget = Budget(
            name='name', amount=1, period=Budget.ONCE,
            date_start=timezone.now().date())
        with self.assertRaises(ValueError):
            budget.save()
        # DAILY
        budget = Budget(
            name='name', amount=1, period=Budget.DAY,
            date_start=timezone.now().date())
        budget.save()
        self.assertEqual(
            budget.date_end, budget.date_start + relativedelta(days=1))
        # WEEKLY
        budget = Budget(
            name='name', amount=1, period=Budget.WEEK,
            date_start=timezone.now().date())
        budget.save()
        self.assertEqual(
            budget.date_end, budget.date_start + relativedelta(weeks=1))
        # MONTHLY
        budget = Budget(
            name='name', amount=1, period=Budget.MONTH,
            date_start=timezone.now().date())
        budget.save()
        self.assertEqual(
            budget.date_end, budget.date_start + relativedelta(months=1))
        # QUARTERLY
        budget = Budget(
            name='name', amount=1, period=Budget.QUARTER,
            date_start=timezone.now().date())
        budget.save()
        self.assertEqual(
            budget.date_end, budget.date_start + relativedelta(months=3))
        # SEMI-ANNUALLY
        budget = Budget(
            name='name', amount=1, period=Budget.SEMI_ANNUAL,
            date_start=timezone.now().date())
        budget.save()
        self.assertEqual(
            budget.date_end, budget.date_start + relativedelta(months=6))
        # ANNUALLY
        budget = Budget(
            name='name', amount=1, period=Budget.ANNUAL,
            date_start=timezone.now().date())
        budget.save()
        self.assertEqual(
            budget.date_end, budget.date_start + relativedelta(years=1))


class PlannedTransactionTestCase(TestCase):
    """tests for Planned Transactions"""

    def setUp(self):
        self.account = FinanceAccount(
            name='name', account_type=FinanceAccount.CASH, amount=0)
        self.account.save()
        self.category = TransactionCategory(name='name')
        self.category.save()

    def tearDown(self):
        pass

    def test_amount_positive(self):
        transaction = PlannedTransaction(
            transaction_type=PlannedTransaction.ONCE,
            account=self.account,
            date=timezone.now().date() + relativedelta(days=1),
            amount=0,
            category=self.category,
            note='note')
        with self.assertRaises(ValueError):
            transaction.save()

    def test_date_future(self):
        transaction = PlannedTransaction(
            transaction_type=PlannedTransaction.ONCE,
            account=self.account,
            date=timezone.now().date(),
            amount=10,
            category=self.category,
            note='note')
        with self.assertRaises(ValueError):
            transaction.save()

    def test_mark_complete(self):
        transaction = PlannedTransaction(
            transaction_type=Transaction.EXPENSE,
            account=self.account,
            date=timezone.now().date() + relativedelta(days=1),
            amount=10,
            category=self.category,
            note='note',
            repeat=PlannedTransaction.ONCE)
        transaction.save()
        # FIXME: mark complete in future date for proper testing
        # transaction.mark_complete()
        # with self.assertRaises(PlannedTransaction.DoesNotExist):
        #     PlannedTransaction.objects.get(pk=transaction.pk)
        # inserted_transasction = Transaction.objects.order_by('-pk').first()
        # self.assertEqual(
        #     transaction.transaction_type,
        #     inserted_transasction.transaction_type)
        # self.assertEqual(transaction.amount, inserted_transasction.amount)
        # self.assertEqual(transaction.date, inserted_transasction.date)
        # self.assertEqual(transaction.account, inserted_transasction.account)
        # self.assertEqual(
        #     transaction.category, inserted_transasction.category)
        # self.assertEqual(transaction.note, inserted_transasction.note)
        # self.assertEqual(transaction.repeat, inserted_transasction.repeat)


class TransferTransactionTestCase(TestCase):
    """tests for Transfer Transactions"""

    def setUp(self):
        self.account1 = FinanceAccount(
            name='account1', account_type=FinanceAccount.CASH, amount=10)
        self.account1.save()
        self.account2 = FinanceAccount(
            name='account2', account_type=FinanceAccount.CASH, amount=10)
        self.account2.save()

    def tearDown(self):
        pass

    def test_same_account_transfer(self):
        transfer = TransferTransaction(
            account_from=self.account1, account_to=self.account1,
            date=timezone.now().date(), amount=10, note='note')
        with self.assertRaises(ValueError):
            transfer.save()

    def test_future_transfer(self):
        transfer = TransferTransaction(
            account_from=self.account1, account_to=self.account2,
            date=timezone.now().date() + relativedelta(days=1),
            amount=10, note='note')
        with self.assertRaises(ValueError):
            transfer.save()

    def test_amount_positive(self):
        transfer = TransferTransaction(
            account_from=self.account1, account_to=self.account2,
            date=timezone.now().date(), amount=0, note='note')
        with self.assertRaises(ValueError):
            transfer.save()

    def test_transfer_change(self):
        amount_1 = self.account1.amount
        amount_2 = self.account2.amount
        transfer = TransferTransaction(
            account_from=self.account1, account_to=self.account2,
            date=timezone.now().date(), amount=10, note='note')
        transfer.save()
        self.assertEqual(self.account1.amount, amount_1 - transfer.amount)
        self.assertEqual(self.account2.amount, amount_2 + transfer.amount)
