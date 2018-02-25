from django.db import models
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse


class TelegramUser(models.Model):
    '''Telegram User
    This is the user that interacts with the bot.
    '''

    GNIB_STUDY_NEW = 'GSN'
    GNIB_STUDY_RENEWAL = 'GSR'
    GNIB_WORK_NEW = 'GWN'
    GNIB_WORK_RENEWAL = 'GWR'
    GNIB_OTHER_NEW = 'GON'
    GNIB_OTHER_RENEWAL = 'GOR'
    VISA_INDIVIDUAL = 'VI'
    VISA_FAMILY = 'VF'

    GNIB_APPOINTMENT_TYPES = (
        (GNIB_STUDY_NEW, 'Study New'),
        (GNIB_STUDY_RENEWAL, 'Study Renewal'),
        (GNIB_WORK_NEW, 'Work New'),
        (GNIB_WORK_RENEWAL, 'Work Renewal'),
        (GNIB_OTHER_NEW, 'Other New'),
        (GNIB_OTHER_RENEWAL, 'Other Renewal'),
        )

    VISA_APPOINTMENT_TYPES = (
        (VISA_INDIVIDUAL, 'Individual'),
        (VISA_FAMILY, 'Family'),
        )

    chat_id = models.CharField(max_length=64, db_index=True, primary_key=True)
    appointment_gnib = models.CharField(
        max_length=64, db_index=True, choices=GNIB_APPOINTMENT_TYPES,
        blank=True, null=True)
    gnib_filter_date_start = models.DateField(blank=True, null=True)
    gnib_filter_date_end = models.DateField(blank=True, null=True)
    appointment_visa = models.CharField(
        max_length=64, db_index=True, choices=VISA_APPOINTMENT_TYPES,
        blank=True, null=True)
    visa_filter_date_start = models.DateField(blank=True, null=True)
    visa_filter_date_end = models.DateField(blank=True, null=True)
    # first_interaction = models.DateTimeField(auto_now_add=True, db_index=True)
    # last_interaction = models.DateTimeField(auto_now=True, db_index=True)

    def __str__(self):
        return self.chat_id

    def get_absolute_url(self):
        return reverse('dev:utils:gnib-notifications', args=(self.chat_id,))

    class Meta(object):
        ordering = ['chat_id']

    @classmethod
    def resolve_type(cls, key):
        if key == cls.GNIB_STUDY_NEW or key == 'SN':
            return 'Study - New'
        elif key == cls.GNIB_STUDY_RENEWAL or key == 'SR':
            return 'Study - Renewal'
        elif key == cls.GNIB_WORK_NEW or key == 'WN':
            return 'Work - New'
        elif key == cls.GNIB_WORK_RENEWAL or key == 'WR':
            return 'Work - Renewal'
        elif key == cls.GNIB_OTHER_NEW or key == 'ON':
            return 'Other - New'
        elif key == cls.GNIB_OTHER_RENEWAL or key == 'OR':
            return 'Other - Renewal'
        elif key == cls.VISA_INDIVIDUAL or key == 'VI':
            return 'Individual'
        elif key == cls.VISA_FAMILY or key == 'VF':
            return 'Family'
