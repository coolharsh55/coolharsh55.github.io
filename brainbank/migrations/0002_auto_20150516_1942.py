# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='brainbankidea',
            options={'verbose_name': 'Brainbank idea', 'verbose_name_plural': 'Brainbank ideas'},
        ),
    ]
