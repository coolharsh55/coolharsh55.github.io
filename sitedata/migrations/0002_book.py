# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(max_length=200)),
                ('read', models.BooleanField(default=False, verbose_name=b'read?')),
                ('date_start', models.DateField(auto_now=True, verbose_name=b'Started')),
                ('date_end', models.DateField(verbose_name=b'Finished', blank=True)),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('title', 'date_start', 'date_end'),
            },
        ),
    ]
