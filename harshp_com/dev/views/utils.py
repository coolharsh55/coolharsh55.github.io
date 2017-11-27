from django.shortcuts import render
import redis
import json
from utils.pagecommons import pagecommon

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
