# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('devblog', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='devblogpost',
            options={'verbose_name': 'dev blog post', 'verbose_name_plural': 'dev blog posts'},
        ),
        migrations.AlterModelOptions(
            name='devblogseries',
            options={'verbose_name': 'dev blog series', 'verbose_name_plural': 'dev blog series'},
        ),
    ]
