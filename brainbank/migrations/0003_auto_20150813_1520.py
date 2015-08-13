# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0004_auto_20150810_0945'),
        ('brainbank', '0002_brainbankidea_repo'),
    ]

    operations = [
        migrations.AddField(
            model_name='brainbankdemo',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 15, 20, 0, 108349, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brainbankdemo',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 15, 20, 24, 942614, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brainbankdemo',
            name='tag',
            field=models.ManyToManyField(to='sitedata.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='brainbankidea',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 15, 20, 31, 732923, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='brainbankidea',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='brainbankpost',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 15, 20, 37, 544830, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
