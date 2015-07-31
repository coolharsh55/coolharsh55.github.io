# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0009_auto_20150701_1835'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brainbankidea',
            name='slug',
            field=models.SlugField(),
        ),
    ]
