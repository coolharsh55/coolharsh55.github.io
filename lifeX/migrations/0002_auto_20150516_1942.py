# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lifex',
            options={'verbose_name': 'Life Experiment', 'verbose_name_plural': 'Life Experiments'},
        ),
    ]
