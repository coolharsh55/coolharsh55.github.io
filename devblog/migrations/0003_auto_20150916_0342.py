# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('devblog', '0002_auto_20150914_1328'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='devblogseries',
            name='posts',
        ),
        migrations.AddField(
            model_name='devblogpost',
            name='series',
            field=models.ForeignKey(blank=True, to='devblog.DevBlogSeries', null=True),
        ),
        migrations.AddField(
            model_name='devblogseries',
            name='description',
            field=redactor.fields.RedactorField(default=None),
            preserve_default=False,
        ),
    ]
