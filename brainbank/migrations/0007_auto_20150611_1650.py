# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0006_auto_20150601_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='brainbankdemo',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='brainbankidea',
            name='slug',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AddField(
            model_name='brainbankpost',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
