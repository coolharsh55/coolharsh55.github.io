# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0004_lifexidea_body'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifexblog',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='lifexidea',
            name='slug',
            field=models.SlugField(blank=True),
        ),
        migrations.AddField(
            model_name='lifexpost',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
