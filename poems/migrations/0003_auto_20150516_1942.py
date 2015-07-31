# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('poems', '0002_auto_20150502_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='poem',
            options={'verbose_name': 'Poem', 'verbose_name_plural': 'Poems'},
        ),
    ]
