# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0005_auto_20150611_1737'),
    ]

    operations = [
        migrations.AddField(
            model_name='lifexcategory',
            name='slug',
            field=models.SlugField(max_length=250, blank=True),
        ),
    ]
