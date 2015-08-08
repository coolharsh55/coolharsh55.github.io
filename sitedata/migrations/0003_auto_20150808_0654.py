# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0002_auto_20150807_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='game',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='movie',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='tvshow',
            name='tags',
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.DeleteModel(
            name='Game',
        ),
        migrations.DeleteModel(
            name='Movie',
        ),
        migrations.DeleteModel(
            name='TVShow',
        ),
    ]
