# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0004_auto_20150822_1739'),
    ]

    operations = [
        migrations.AlterField(
            model_name='brainbankdemo',
            name='body',
            field=redactor.fields.RedactorField(verbose_name=b'content'),
        ),
        migrations.AlterField(
            model_name='brainbankdemo',
            name='css',
            field=redactor.fields.RedactorField(verbose_name=b'CSS'),
        ),
        migrations.AlterField(
            model_name='brainbankdemo',
            name='js',
            field=redactor.fields.RedactorField(verbose_name=b'javascript'),
        ),
        migrations.AlterField(
            model_name='brainbankidea',
            name='body',
            field=redactor.fields.RedactorField(),
        ),
        migrations.AlterField(
            model_name='brainbankpost',
            name='body',
            field=redactor.fields.RedactorField(),
        ),
    ]
