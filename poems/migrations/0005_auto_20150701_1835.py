# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poems', '0004_poem_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='slug',
            field=models.CharField(unique=True, max_length=50),
        ),
    ]
