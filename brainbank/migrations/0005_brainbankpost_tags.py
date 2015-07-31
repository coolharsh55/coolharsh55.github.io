# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0001_initial'),
        ('brainbank', '0004_auto_20150601_0049'),
    ]

    operations = [
        migrations.AddField(
            model_name='brainbankpost',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag'),
        ),
    ]
