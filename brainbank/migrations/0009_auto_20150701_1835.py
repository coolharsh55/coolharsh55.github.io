# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0008_auto_20150622_1459'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brainbankdemo',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        # migrations.AlterField(
        #     model_name='brainbankidea',
        #     name='slug',
        #     field=models.SlugField(unique=True),
        # ),
        migrations.AlterField(
            model_name='brainbankpost',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
