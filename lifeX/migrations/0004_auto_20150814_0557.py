# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0003_auto_20150813_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifexidea',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 57, 52, 550450, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lifexidea',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 57, 56, 452312, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
