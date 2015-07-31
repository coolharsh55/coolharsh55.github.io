# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0003_auto_20150531_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifexidea',
            name='body',
            field=ckeditor.fields.RichTextField(default='NA'),
            preserve_default=False,
        ),
    ]
