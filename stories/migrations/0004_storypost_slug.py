# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0003_auto_20150516_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='storypost',
            name='slug',
            field=models.CharField(max_length=50, blank=True),
        ),
    ]
