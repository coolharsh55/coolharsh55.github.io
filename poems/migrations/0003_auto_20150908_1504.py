# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('poems', '0002_auto_20150813_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poem',
            name='body',
            field=redactor.fields.RedactorField(),
        ),
    ]
