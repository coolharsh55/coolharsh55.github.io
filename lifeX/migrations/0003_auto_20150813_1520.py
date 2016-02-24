# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0004_auto_20150810_0945'),
        ('lifeX', '0002_lifexblog_headerimage'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lifexblog',
            old_name='date',
            new_name='published',
        ),
        migrations.RenameField(
            model_name='lifexpost',
            old_name='date',
            new_name='published',
        ),
        migrations.AddField(
            model_name='lifexblog',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 15, 20, 42, 939630, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lifexidea',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='lifexpost',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 13, 15, 20, 46, 694771, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
    ]
