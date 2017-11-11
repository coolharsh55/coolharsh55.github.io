from django.shortcuts import render
import json
from utils.pagecommons import pagecommon


def gnib_appointments(request):
    with open('/tmp/gnib_appointments.json', 'r') as fd:
        appointments = json.load(fd)
    template_objects = {
        'timestamp': appointments['timestamp'],
        'GNIB_Study': appointments['study'],
        'GNIB_Work': appointments['work'],
        'GNIB_Other': appointments['other'],
        'VISA_Individual': appointments['individual'],
        'VISA_Family': appointments['family'],
        }
    pagecommon(request, template_objects)
    return render(
        request, 'dev/utils/gnib_appointments.html', template_objects)
