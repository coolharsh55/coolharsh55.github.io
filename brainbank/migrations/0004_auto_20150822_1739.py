# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0003_auto_20150813_1520'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brainbankdemo',
            old_name='tag',
            new_name='tags',
        ),
    ]
