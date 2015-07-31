# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stories', '0002_auto_20150502_1632'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='storypost',
            options={'verbose_name': 'Story', 'verbose_name_plural': 'Stories'},
        ),
    ]
