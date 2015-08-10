# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brainbankidea',
            name='repo',
            field=models.URLField(max_length=500, null=True, blank=True),
        ),
    ]
