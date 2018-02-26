from django.contrib import admin

from apps.models.gnib_telegram_bot import TelegramUser


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = [
            'chat_id', 'appointment_gnib', 'appointment_visa',
            'gnib_filter_date_start', 'visa_filter_date_start']
    list_filter = ['appointment_gnib', 'appointment_visa']
