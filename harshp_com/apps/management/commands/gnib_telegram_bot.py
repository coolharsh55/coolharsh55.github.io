from django.core.management.base import BaseCommand
from apps.jobs.gnib_telegram_bot import run


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        run()
