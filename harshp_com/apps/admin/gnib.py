from django.contrib import admin

from apps.models.gnib import GNIBAppointment
from apps.models.gnib import VisaAppointment


@admin.register(GNIBAppointment)
class GNIBAppointmentAdmin(admin.ModelAdmin):
    list_display = [
        'timestamp', 'added_on', 'booked', 'category', 'category_type']
    list_filter = ['category', 'category_type']
    date_hierarchy = 'timestamp'


@admin.register(VisaAppointment)
class VisaAppointmentAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'added_on', 'booked', 'category']
    list_filter = ['category']
    date_hierarchy = 'timestamp'
