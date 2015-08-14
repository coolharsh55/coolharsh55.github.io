# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0002_auto_20150810_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 9, 262856, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 14, 770858, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 18, 851583, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='game',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 22, 391594, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 38, 965326, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='movie',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 43, 377263, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvshow',
            name='modified',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 47, 142091, tzinfo=utc), blank=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tvshow',
            name='published',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 14, 5, 50, 50, 225042, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
