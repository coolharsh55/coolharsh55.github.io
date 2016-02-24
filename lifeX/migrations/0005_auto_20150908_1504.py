# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0004_auto_20150814_0557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifexblog',
            name='body',
            field=redactor.fields.RedactorField(),
        ),
        migrations.AlterField(
            model_name='lifexidea',
            name='body',
            field=redactor.fields.RedactorField(),
        ),
        migrations.AlterField(
            model_name='lifexpost',
            name='body',
            field=redactor.fields.RedactorField(),
        ),
    ]
