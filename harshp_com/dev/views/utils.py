from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib import messages
import arrow
import redis
import json
from utils.pagecommons import pagecommon
from apps.models.gnib_telegram_bot import TelegramUser


kvstore = redis.StrictRedis(
    host='localhost', port=6379, db=0, decode_responses=True)


def gnib_appointments(request):
    template_objects = {
        'gnib_Study_New': json.loads(kvstore.get('gnib_Study_New')),
        'gnib_Study_Renewal': json.loads(kvstore.get('gnib_Study_Renewal')),
        'gnib_Work_New': json.loads(kvstore.get('gnib_Work_New')),
        'gnib_Work_Renewal': json.loads(kvstore.get('gnib_Work_Renewal')),
        'gnib_Other_New': json.loads(kvstore.get('gnib_Other_New')),
        'gnib_Other_Renewal': json.loads(kvstore.get('gnib_Other_Renewal')),
        'visa_I': json.loads(kvstore.get('visa_I')),
        'visa_F': json.loads(kvstore.get('visa_F')),
        'last_update': kvstore.get('gnib_last_run'),
    }
    pagecommon(request, template_objects)
    return render(
        request, 'dev/utils/gnib_appointments.html', template_objects)


def gnib_notifications(request, chat_id):

    def _datestring(date):
        if date is not None:
            return date.strftime('%Y-%m-%d')
        return ''

    user = get_object_or_404(TelegramUser, chat_id=chat_id)
    error_flag = False

    if request.method == 'POST':
        today = arrow.now()

        gnib_type = request.POST['gnib-type']
        visa_type = request.POST['visa-type']

        gnib_start_date = request.POST['gnib-start-date']
        if gnib_start_date:
            gnib_start_date = arrow.get(gnib_start_date).datetime
            if gnib_start_date < today:
                messages.error(
                        request, 'GNIB start date cannot be before today')
                error_flag = True
        else:
            gnib_start_date = None
        gnib_end_date = request.POST['gnib-end-date']
        if gnib_end_date:
            if not gnib_start_date:
                messages.error(
                  request, 'GNIB end date should have a start date')
                error_flag = True
            gnib_end_date = arrow.get(gnib_end_date).datetime
            if gnib_end_date <= today:
                messages.error(
                  request, 'GNIB end date should be atleast tomorrow')
                error_flag = True
        else:
            gnib_end_date = None

        visa_start_date = request.POST['visa-start-date']
        if visa_start_date:
            visa_start_date = arrow.get(visa_start_date).datetime
            if visa_start_date < today:
                messages.error(
                  request, 'VISA start date cannot be before today')
                error_flag = True
        else:
            visa_start_date = None
        visa_end_date = request.POST['visa-end-date']
        if visa_end_date:
            if not visa_start_date:
                messages.error(
                  request, 'VISA end date should have a start date')
                error_flag = True
            visa_end_date = arrow.get(visa_end_date).datetime
            if visa_end_date <= today:
                messages.error(
                  request, 'VISA end date should be atleast tomorrow')
                error_flag = True
        else:
            visa_end_date = None

        if not error_flag:
            user.appointment_gnib = gnib_type
            user.gnib_filter_date_start = gnib_start_date
            user.gnib_filter_date_end = gnib_end_date
            user.appointment_visa = visa_type
            user.visa_filter_date_start = visa_start_date
            user.visa_filter_date_end = visa_end_date
            user.save()
            messages.success(request, "Your preferences have been saved")
    else:
        pass

    gnib_type = user.appointment_gnib
    gnib_start_date = _datestring(user.gnib_filter_date_start)
    gnib_end_date = _datestring(user.gnib_filter_date_end)
    visa_type = user.appointment_visa
    visa_start_date = _datestring(user.visa_filter_date_start)
    visa_end_date = _datestring(user.visa_filter_date_end)
    items = {
            'gnib_types': TelegramUser.GNIB_APPOINTMENT_TYPES,
            'visa_types': TelegramUser.VISA_APPOINTMENT_TYPES,
            'gnib_set': gnib_type,
            'visa_set': visa_type,
            'gnib_date_start': gnib_start_date,
            'gnib_date_end': gnib_end_date,
            'visa_date_start': visa_start_date,
            'visa_date_end': visa_end_date,
            }

    return render(
        request, 'dev/utils/gnib_notifications.html', items)
