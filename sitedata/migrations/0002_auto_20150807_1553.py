# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='slug',
            field=models.SlugField(default='tag', max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='tagname',
            field=models.CharField(unique=True, max_length=150),
        ),
    ]
