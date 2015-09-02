# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.file


class Migration(migrations.Migration):

    dependencies = [
        ('filer', '0002_auto_20150606_2003'),
        ('sitedata', '0009_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='filefield',
            field=filer.fields.file.FilerFileField(default=None, to='filer.File'),
            preserve_default=False,
        ),
    ]
