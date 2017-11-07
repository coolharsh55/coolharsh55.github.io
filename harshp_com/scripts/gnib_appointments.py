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
from datetime import datetime
import requests
import json

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


def get_gnib_appointments(appointment_type):
    params = (
        ('openpage', ''),  # BLANK
        ('dt', ''),  # PARSED, but is always blank
        ('cat', appointment_type),  # Category
        ('sbcat', 'All'),  # Sub-Category
        ('typ', 'Renewal'),  # Type
    )
    # make the request
    # verify=False --> disable SSL verification
    response = requests.get(
        'https://burghquayregistrationoffice.inis.gov.ie/'
        + 'Website/AMSREG/AMSRegWeb.nsf/(getAppsNear)',
        headers=headers, params=params, verify=False)

    # check if we have a good response
    if response.status_code != 200:
        return

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        return

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        return

    # There are appointments, and are in the key 'slots'
    data = data.get('slots', None)
    if data is None:
        return

    # This should not happen, but a good idea to check it anyway
    if len(data) == 0:
        return

    # print appointments
    # Format is:
    # {
    #   'id': 'str',
    #   'time': 'str'
    # }
    return [appointment['time'] for appointment in data]


def get_visa_appointments(appointment_type):
    # Parameters from the js script at
    # https://reentryvisa.inis.gov.ie
    # /website/INISOA/IOA.nsf/AppForm.js
    params = (
        ('openagent', ''),  # BLANK
        ('type', appointment_type)  # I signifies individual
    )

    # make the request
    # verify=False --> disable SSL verification
    response = requests.get(
        'https://reentryvisa.inis.gov.ie'
        + '/website/INISOA/IOA.nsf/(getDTAvail)',
        headers=headers, params=params, verify=False)

    # check if we have a good response
    if response.status_code != 200:
        return

    # sanity checks
    data = response.json()
    # error key is set
    if data.get('error', None) is not None:
        return

    # If there are no appointments, then the empty key is set
    if data.get('empty', None) is not None:
        return

    # There are appointments, and are in the key 'dates'
    data = data.get('dates', None)
    if data is None:
        return

    # This should not happen, but a good idea to check it anyway
    if len(data) == 0:
        return

    # print appointments
    # Format is:
    # {'dates': ['DD-MM-YYYY', ...]}
    url = 'https://reentryvisa.inis.gov.ie/website/inisoa/ioa.nsf/(getapps4dt)'
    visa_appointments = {}
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
        visa_appointments[date] = [appointment['time'] for appointment in data]
    return visa_appointments


def get_all_appointments():
    study = get_gnib_appointments('Study')
    if study is None:
        study = []
    work = get_gnib_appointments('Work')
    if work is None:
        work = []
    other = get_gnib_appointments('Other')
    if other is None:
        other = []
    individual = get_visa_appointments('I')
    if individual is None:
        individual = []
    else:
        individual = list(individual.items())
    family = get_visa_appointments('F')
    if family is None:
        family = []
    else:
        family = list(family.items())
    return {
        'study': study,
        'work': work,
        'other': other,
        'individual': individual,
        'family': family
    }


if __name__ == '__main__':
    appointments = get_all_appointments()
    appointments['timestamp'] = datetime.now().strftime('%H:%M')
    with open('/tmp/gnib_appointments.json', 'w') as fd:
        json.dump(appointments, fd)
