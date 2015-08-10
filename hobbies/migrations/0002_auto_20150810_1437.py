# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hobbies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='headerimage',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='game',
            name='headerimage',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='movie',
            name='headerimage',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='tvshow',
            name='headerimage',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
    ]
