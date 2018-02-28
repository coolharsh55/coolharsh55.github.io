import arrow
import json
import logging
import redis
import telegram
from apps.models.gnib_telegram_bot import TelegramUser
from harshp_com.settings.auth import TELEGRAM_API_KEY


logger = logging.getLogger('gnib')


kvstore = redis.StrictRedis(
    host='localhost', port=6379, db=0, decode_responses=True)


def retrieve_users_for_gnib_appointments(aptype, available):
    datified = [arrow.get(item, 'D MMMM YYYY - HH:mm') for item in available]
    users = TelegramUser.objects.filter(appointment_gnib=aptype)
    selected_users = []
    for user in users:
        if user.gnib_filter_date_start is None:
            selected_users.append((user.chat_id, available))
        else:
            dates_to_send = []
            for date in datified:
                if user.gnib_filter_date_start >= date:
                    if user.gnib_filter_date_end is None or\
                            user.gnib_filter_date_end <= date:
                        dates_to_send.append(date)
            if dates_to_send:
                selected_users.append((user.chat_id, dates_to_send))
    logger.info(f'found {len(selected_users)} users for gnib type {aptype}')
    return selected_users


def retrieve_users_for_visa_appointments(aptype, available):
    datified = [
        (arrow.get(item, 'DD/MM/YYYY HH:mm'), item)
        for item in available]
    users = TelegramUser.objects.filter(appointment_visa=aptype)
    selected_users = []
    for user in users:
        if user.visa_filter_date_start is None:
            selected_users.append((user.chat_id, available))
        else:
            dates_to_send = []
            for date, msg in datified:
                if user.visa_filter_date_start >= date:
                    if user.visa_filter_date_end is None or\
                            user.visa_filter_date_end <= date:
                        dates_to_send.append(msg)
            if dates_to_send:
                selected_users.append((user.chat_id, dates_to_send))
    logger.info(f'found {len(selected_users)} users for visa type {aptype}')
    return selected_users


async def send_notification_to_users(users, category, aptype, last_update):
    '''send notification to users via Telegram'''
    async def _send_notification(bot, chat_id, text):
        bot.send_message(chat_id=chat_id, text=text)
        logger.info(f'send message to {chat_id} - {text}')

    telegrambot = telegram.Bot(token=TELEGRAM_API_KEY)
    for user, appointments in users:
        message = 'New appointments for {} {}: {}. Last updated at {}'.format(
            category, TelegramUser.resolve_type(aptype),
            ', '.join(appointments), last_update)
        await _send_notification(telegrambot, user, message)


async def job():
    # retrieve added appointment for every type from database
    gnib_appointments = {
        TelegramUser.GNIB_STUDY_NEW: json.loads(
            kvstore.get('gnib_Study_New_added')),
        TelegramUser.GNIB_STUDY_RENEWAL: json.loads(
            kvstore.get('gnib_Study_Renewal_added')),
        TelegramUser.GNIB_WORK_NEW: json.loads(
            kvstore.get('gnib_Work_New_added')),
        TelegramUser.GNIB_WORK_RENEWAL: json.loads(
            kvstore.get('gnib_Work_Renewal_added')),
        TelegramUser.GNIB_OTHER_NEW: json.loads(
            kvstore.get('gnib_Other_New_added')),
        TelegramUser.GNIB_OTHER_RENEWAL: json.loads(
            kvstore.get('gnib_Other_Renewal_added')),
    }
    logger.debug(f'gnib appointments: {gnib_appointments}')
    visa_appointments = {
        TelegramUser.VISA_INDIVIDUAL: json.loads(
            kvstore.get('visa_I_added')),
        TelegramUser.VISA_FAMILY: json.loads(
            kvstore.get('visa_F_added')),
    }
    last_update = kvstore.get('gnib_last_run')

    # retrieve users that want notifications for this appointment type
    for type, available in gnib_appointments.items():
        if available:
            logger.debug(f'handling notifications for {type}, {available}')
            users = retrieve_users_for_gnib_appointments(type, available)
            logger.debug(f'available users for {type}: {users}')
            try:
                await send_notification_to_users(users, 'gnib', type, last_update)
            except Exception as E:
                logger.error(E, exc_info=True)
    for type, available in visa_appointments.items():
        if available:
            users = retrieve_users_for_visa_appointments(type, available)
            logger.debug(f'available users for {type}: {users}')
            await send_notification_to_users(users, 'visa', type, last_update)
