# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lifeX', '0006_lifexcategory_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lifex',
            name='tags',
        ),
        migrations.DeleteModel(
            name='LifeX',
        ),
    ]
