# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0003_auto_20150814_0550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='date_end',
            field=models.DateField(null=True, verbose_name=b'Finished', blank=True),
        ),
        migrations.AlterField(
            model_name='tvshow',
            name='date_end',
            field=models.DateField(null=True, verbose_name=b'Finished', blank=True),
        ),
    ]
