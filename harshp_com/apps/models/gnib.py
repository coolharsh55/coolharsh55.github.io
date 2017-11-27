from django.db import models
from django.contrib.postgres.fields import JSONField


class AppointmentSlot(models.Model):
    '''represents an appointment slot returned by the GNIB system
    timestamp(DateTimeField): appointment time
    added_on(DateTimeField): timestamp of entry into database
    booked(DateTimeField): timestamp of when the appointment was booked

    Abstract Class
    '''
    timestamp = models.DateTimeField(db_index=True)
    added_on = models.DateTimeField(auto_now_add=True)
    booked = models.DateTimeField(db_index=True, blank=True, null=True)


    class Meta(object):
        abstract = True
        ordering = ('-timestamp',)

    def __str__(self):
        return str(self.timestamp)

    def __repr__(self):
        return 'time: {} added: {}'.format(self.timestamp, self.added_on)


class GNIBAppointment(AppointmentSlot):
    '''GNIB Appointment'''
    CATEGORY_STUDY = 'Study'
    CATEGORY_WORK = 'Work'
    CATEGORY_OTHER = 'Other'
    CATEGORIES = (
        (CATEGORY_STUDY, 'GNIB Study Appointment'),
        (CATEGORY_WORK, 'GNIB Work Appointment'),
        (CATEGORY_OTHER, 'GNIB Other Appointment'),
    )
    CATEGORY_TYPE_NEW = 'New'
    CATEGORY_TYPE_RENEWAL = 'Renewal'
    CATEGORY_TYPES = (
        (CATEGORY_TYPE_NEW, 'GNIB New Appointment'),
        (CATEGORY_TYPE_RENEWAL, 'GNIB Renewal Appointment'),
    )

    category = models.CharField(
        max_length=8, db_index=True, choices=CATEGORIES)
    category_type = models.CharField(
        max_length=8, db_index=True, choices=CATEGORY_TYPES)

    class Meta(object):
        verbose_name = 'GNIB Appointment'
        verbose_name_plural = 'GNIB Appointments'


class VisaAppointment(AppointmentSlot):
    '''Visa Appointment'''
    CATEGORY_INDIVIDUAL = 'I'
    CATEGORY_FAMILY = 'F'
    CATEGORIES = (
        (CATEGORY_INDIVIDUAL, 'Visa Individual Appointment'),
        (CATEGORY_FAMILY, 'Visa Family Appointment'),
    )

    category = models.CharField(
        max_length=8, db_index=True, choices=CATEGORIES)

    class Meta(object):
        verbose_name = 'Visa Appointment'
        verbose_name_plural = 'Visa Appointments'


# class APIResponse(models.Model):
#     '''Stores raw JSON response from GNIB API'''
#     CATEGORIES = (*GNIBAppointment.CATEGORIES, *VisaAppointment.CATEGORIES)
#     CATEGORY_TYPES = (*GNIBAppointment.CATEGORY_TYPES, 'None')
#     category = models.CharField(
#             max_length=8, db_index=True, choices=CATEGORIES)
#     category_type = models.CharField(
#         max_length=8, db_index=True, choices=CATEGORY_TYPES)
#     added_on = models.DateTimeField(auto_now_add=True)
#     json = JSONField()

#     class Meta(object):
#         ordering = ('-added_on',)
#         verbose_name = 'API Response'
#         verbose_name_plural = 'API Responses'

#     def __str__(self):
#         return '{}-{} added:{}'.format(
#             self.category, self.category_type, self.added_on)
