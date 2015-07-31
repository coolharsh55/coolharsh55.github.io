# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0004_storypost_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='storypost',
            name='slug',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
