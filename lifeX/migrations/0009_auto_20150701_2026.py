# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0008_auto_20150701_1835'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lifexidea',
            options={'ordering': ['title'], 'verbose_name': 'LifeX Idea', 'verbose_name_plural': 'LifeX Ideas'},
        ),
    ]
