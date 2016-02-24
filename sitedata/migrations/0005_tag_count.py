# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0004_auto_20150810_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
