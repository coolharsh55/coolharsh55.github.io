# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0005_auto_20150908_1504'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifexblog',
            name='slug',
            field=models.SlugField(unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lifexidea',
            name='slug',
            field=models.SlugField(unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='lifexpost',
            name='slug',
            field=models.SlugField(unique=True, max_length=250),
        ),
    ]
