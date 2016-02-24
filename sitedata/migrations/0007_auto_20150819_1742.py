# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0006_feedback'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='text',
            field=redactor.fields.RedactorField(),
        ),
    ]
