# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0004_auto_20150818_1105'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='continuing',
            field=models.BooleanField(default=False, verbose_name=b'Continuing?'),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='season',
            field=models.IntegerField(default=0),
        ),
    ]
