# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0011_csslink_jslink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='csslink',
            name='dependency',
            field=models.ManyToManyField(to='sitedata.CSSLink', blank=True),
        ),
        migrations.AlterField(
            model_name='jslink',
            name='dependency',
            field=models.ManyToManyField(to='sitedata.JSLink', blank=True),
        ),
    ]
