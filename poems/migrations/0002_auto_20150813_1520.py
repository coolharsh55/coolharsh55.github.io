# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='modified',
            field=models.DateTimeField(blank=True),
        ),
    ]
