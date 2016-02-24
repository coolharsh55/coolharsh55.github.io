# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifexblog',
            name='headerimage',
            field=models.URLField(blank=True),
        ),
    ]
