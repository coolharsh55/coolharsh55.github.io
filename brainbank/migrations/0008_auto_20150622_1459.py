# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0007_auto_20150611_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brainbankidea',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
