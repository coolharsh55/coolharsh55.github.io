import logging
import json
import redis
from telegram import ParseMode
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from django.contrib.sites.models import Site
from harshp_com.settings.auth import TELEGRAM_API_KEY

from apps.models.gnib_telegram_bot import TelegramUser

kvstore = redis.StrictRedis(
        host='localhost', port=6379, db=0, decode_responses=True)

logger = logging.getLogger('gnib')

_help_message = '''
/start - start notifications
/stop - stop notifications
/customise - customise notifications
/gnib - show GNIB appointments
/visa - show VISA appointments
/help - show this message
'''


# HELPER FUNCTIONS


def _start_notifications(bot, job):
    '''start notifications for this user'''
    user, _ = TelegramUser.objects.get_or_create(chat_id=job.context)
    link = user.get_absolute_url()
    link = 'https://' + Site.objects.get_current().domain + link
    bot.send_message(
        chat_id=job.context, 
        text=f'''Started notifications.
        You can [customise notifications (click here)]({link})
        to select type of appointment and date filters.''',
        parse_mode=ParseMode.MARKDOWN)


def _stop_notifications(bot, job):
    '''stop notifications for this user'''
    try:
        user = TelegramUser.objects.get(chat_id=job.context)
        user.appointment_gnib = None
        user.appointment_visa = None
        user.gnib_filter_date_start = None
        user.gnib_filter_date_end = None
        user.visa_filter_date_start = None
        user.visa_filter_date_end = None
        user.save()
        print(user.appointment_gnib, user.appointment_visa)
    except TelegramUser.DoesNotExist:
        pass
    bot.send_message(chat_id=job.context, text='notifications stopped')


# HANDLERS


def start(bot, update, job_queue):
    '''message to be shown at the start of conversation'''
    job_queue.run_once(
        _start_notifications, when=0, context=update.message.chat_id)
    return


def stop(bot, update, job_queue):
    '''message to be shown at the stop of conversation'''
    job_queue.run_once(
        _stop_notifications, when=0, context=update.message.chat_id)
    return


def customise(bot, update, job_queue):
    '''message containing link to customisation page'''
    job_queue.run_once(
        _start_notifications, when=0, context=update.message.chat_id)
    return


def help(bot, update):
    '''show help message'''
    bot.send_message(chat_id=update.message.chat_id, text=_help_message)
    return


def echo(bot, update):
    '''generic message that does not conform to other commands'''
    bot.send_message(chat_id=update.message.chat_id, text=_help_message)
    return


def _helper_message_list(message, key, text):
    appointments = json.loads(kvstore.get(key))
    if not appointments:
        return
    message.append(text)
    for appointment in appointments:
        message.append(appointment)


def appointments_gnib(bot, update):
    '''show GNIB appointments'''
    message = []
    _helper_message_list(message, 'gnib_Study_New', 'Study - New')
    _helper_message_list(message, 'gnib_Study_Renewal', 'Study - Renewal')
    _helper_message_list(message, 'gnib_Work_New', 'Work - New')
    _helper_message_list(message, 'gnib_Work_Renewal', 'Work - Renewal')
    _helper_message_list(message, 'gnib_Other_New', 'Other - New')
    _helper_message_list(message, 'gnib_Other_Renewal', 'Other - Renewal')
    if not message:
        message = 'no appointments available'
    else:
        temp = '\n'.join(message)
        message = temp

    bot.send_message(chat_id=update.message.chat_id, text=message)


def appointments_visa(bot, update):
    '''show VISA appointments'''
    message = []
    _helper_message_list(message, 'visa_I', 'Individual')
    _helper_message_list(message, 'visa_F', 'Family')
    if not message:
        message = 'no appointments available'
    else:
        temp = '\n'.join(message)
        message = temp
    bot.send_message(chat_id=update.message.chat_id, text=message)


def run():
    updater = Updater(token=TELEGRAM_API_KEY)
    dispatcher = updater.dispatcher

    # register handlers
    dispatcher.add_handler(CommandHandler('start', start, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler('stop', stop, pass_job_queue=True))
    dispatcher.add_handler(
            CommandHandler('customise', customise, pass_job_queue=True))
    dispatcher.add_handler(CommandHandler('gnib', appointments_gnib))
    dispatcher.add_handler(CommandHandler('visa', appointments_visa))
    dispatcher.add_handler(CommandHandler('help', help))
    dispatcher.add_handler(MessageHandler(Filters.text, echo))

    dispatcher.add_handler(MessageHandler(Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    run()
