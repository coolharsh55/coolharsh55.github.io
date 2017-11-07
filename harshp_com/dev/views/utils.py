from django.shortcuts import render
import json


def gnib_appointments(request):
    with open('/tmp/gnib_appointments.json', 'r') as fd:
        appointments = json.load(fd)
    return render(request, 'dev/utils/gnib_appointments.html', {
        'timestamp': appointments['timestamp'],
        'GNIB_Study': appointments['study'],
        'GNIB_Work': appointments['work'],
        'GNIB_Other': appointments['other'],
        'VISA_Individual': appointments['individual'],
        'VISA_Family': appointments['family'],
        })
