# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0005_auto_20150908_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brainbankdemo',
            name='slug',
            field=models.SlugField(unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='brainbankidea',
            name='slug',
            field=models.SlugField(max_length=250),
        ),
        migrations.AlterField(
            model_name='brainbankpost',
            name='slug',
            field=models.SlugField(unique=True, max_length=250),
        ),
    ]
