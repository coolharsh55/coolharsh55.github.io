# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0005_brainbankpost_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='brainbankdemo',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='brainbankidea',
            old_name='_id',
            new_name='id',
        ),
        migrations.RenameField(
            model_name='brainbankpost',
            old_name='_id',
            new_name='id',
        ),
    ]
