#!/usr/bin/env python3

# author: Harshvardhan Pandit
# email: me@harshp.com

# Script to parse appointment timings from GNIB website
# https://burghquayregistrationoffice.inis.gov.ie/
# Reason: because filling out the ENTIRE form just to check for
# appointments is both silly and stupid. And on closer inspection,
# it is not like ALL the information is required for getting the
# appointments. Plus, it is never clear when the appointments will
# be available. Hence this script.

# EFFECTS
# This will create a JSON listing of all jobs in /tmp/gnib_appointments.json

# It assumes the request module is installed
import asyncio
from itertools import chain
import logging
import requests

logging.basicConfig(
    filename='gnib.log',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO)

logger = logging.getLogger('app.jobs.gnib')

# headers to send
# They don't really matter, except for the CORS bits
headers = {
    'User-agent': 'script/python',
    'Accept': '*/*',  # CORS
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Origin': 'null',  # CORS
    'Connection': 'keep-alive',
}

# Parameters from the js script at
# https://burghquayregistrationoffice.inis.gov.ie
# /Website/AMSREG/AMSRegWeb.nsf/AppForm.js

# Add cipher for request
# Looked up using curl --verbose
# requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':DES-CBC3-SHA'
# disable SSL warning
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)


async def get_gnib_appointments(appointment_type, renewal_type):
    default_response = {
        'type': 'GNIB',
        'category': appointment_type,
        'category_type': renewal_type,
        'data': [],
    }
    params = (
        ('openpage', ''),  # BLANK
        ('dt', ''),  # PARSED, but is always blank
        ('cat', appointment_type),  # Category
        ('sbcat', 'All'),  # Sub-Category
        ('typ', renewal_type),  # Type
    )
    # make the request
    # verify=False --> disable SSL verification
    try:
        response = requests.get(
            'https://burghquayregistrationoffice.inis.gov.ie/'
            + 'Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)',
            headers=headers, params=params, verify=False)
    except Exception as E:
        logger.error('Error in fetching GNIB appointment {} {} - {}'.format(
            appointment_type, renewal_type, E))
        return default_response

    # check if we have a good response
    if response.status_code != 200:
        logger.error('Response not 200 GNIB appointment {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        logger.error('Error GNIB appointment {} {} - {}'.format(
            appointment_type, renewal_type, data['error']))
        return default_response

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        logger.info('GNIB appointment empty {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # There are appointments, and are in the key 'slots'
    data = data.get('slots', None)
    if data is None:
        logger.info('GNIB appointment empty {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # This should not happen, but a good idea to check it anyway
    if not data:
        logger.info('GNIB appointment empty {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # print appointments
    # Format is:
    # {
    #   'id': 'str',
    #   'time': 'str'
    # }
    default_response['data'] = [appointment['time'] for appointment in data]
    return default_response


async def get_visa_appointments(appointment_type):
    default_response = {
        'type': 'Visa',
        'category': appointment_type,
        'category_type': None,
        'data': [],
    }

    # Parameters from the js script at
    # https://reentryvisa.inis.gov.ie
    # /website/INISOA/IOA.nsf/AppForm.js
    params = (
        ('openagent', ''),  # BLANK
        ('type', appointment_type)  # I signifies individual
    )

    # make the request
    # verify=False --> disable SSL verification
    try:
        response = requests.get(
            'https://reentryvisa.inis.gov.ie'
            + '/website/INISOA/IOA.nsf/(getDTAvail)',
            headers=headers, params=params, verify=False)
    except Exception as E:
        logger.error('Error in fetching VISA appointment {} {} - {}'.format(
            appointment_type, renewal_type, E))
        return default_response

    # check if we have a good response
    if response.status_code != 200:
        logger.error('Response not 200 VISA appointment {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        logger.error('Error VISA appointment {} {} - {}'.format(
            appointment_type, renewal_type, data['error']))
        return default_response

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        logger.info('Data empty VISA appointment {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # There are appointments, and are in the key 'dates'
    data = data.get('dates', None)
    if data is None:
        logger.info('Data empty VISA appointment {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # This should not happen, but a good idea to check it anyway
    if not data:
        logger.info('Data empty VISA appointment {} {}'.format(
            appointment_type, renewal_type))
        return default_response

    # print appointments
    # Format is:
    # {'dates': ['DD-MM-YYYY', ...]}
    url = 'https://reentryvisa.inis.gov.ie/website/inisoa/ioa.nsf/(getapps4dt)'
    visa_appointments = []
    for date in data:
        params = (
            ('openagent', ''),  # BLANK
            ('dt', '%s' % date),
            ('type', appointment_type),
            ('num', 1)
        )
        response = requests.get(
                url, headers=headers, verify=False,
                # parameters need to be specified this way to prevent
                # escaping them
                # This really shows the bad design on part of website devs
                params='openagent=&dt=' + date + '&type=' +
                appointment_type + '&num=1')
        data = response.json()
        if (data.get('empty', False)):
            # if there are no appointments on that day, do nothing
            continue
        if data.get('error', False):
            # if there is an error, do nothing, move on to next date
            continue
        if data.get('slots', None) is None:
            # this is an error, but lets move along
            continue
        data = data['slots']
        data = [appointment['time'] for appointment in data]
        visa_appointments = chain(visa_appointments, data)
    default_response['data'] = list(visa_appointments)
    return default_response


def get_tasks():
    return [
        get_gnib_appointments('Study', 'New'),
        get_gnib_appointments('Study', 'Renewal'),
        get_gnib_appointments('Work', 'New'),
        get_gnib_appointments('Work', 'Renewal'),
        get_gnib_appointments('Other', 'New'),
        get_gnib_appointments('Other', 'Renewal'),
        get_visa_appointments('I'),
        get_visa_appointments('F'),
    ]


async def get_all_appointments(callback=None):
    phases = get_tasks()
    completed, pending = await asyncio.wait(phases, timeout=2)
    # DEBUG
    # print('{} completed and {} pending'.format(
    #     len(completed), len(pending),
    # ))
    results = [task.result() for task in completed]
    if callback:
        callback(results)
    return results


def gather_appointments(callback=None):
    def default_callback(results):
        import pprint
        pprint.pprint(results)
    if callback is None:
        callback = default_callback

    event_loop = asyncio.get_event_loop()
    try:
        event_loop.run_until_complete(get_all_appointments(callback))
    finally:
        event_loop.close()


if __name__ == '__main__':
    gather_appointments()
