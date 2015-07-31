# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0002_auto_20150516_1942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brainbankidea',
            name='tags',
        ),
        migrations.DeleteModel(
            name='BrainbankIdea',
        ),
    ]
