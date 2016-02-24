# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0012_auto_20150916_0342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='reply',
            field=redactor.fields.RedactorField(null=True, blank=True),
        ),
    ]
