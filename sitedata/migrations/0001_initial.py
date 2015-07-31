# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('tagid', models.AutoField(serialize=False, primary_key=True)),
                ('tagname', models.CharField(max_length=150)),
            ],
            options={
                'ordering': ('tagname',),
            },
        ),
    ]
