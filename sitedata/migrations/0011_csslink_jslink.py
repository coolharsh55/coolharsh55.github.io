# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0010_fileupload_filefield'),
    ]

    operations = [
        migrations.CreateModel(
            name='CSSLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('link', models.URLField(unique=True)),
                ('dependency', models.ManyToManyField(to='sitedata.CSSLink')),
            ],
        ),
        migrations.CreateModel(
            name='JSLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=150)),
                ('link', models.URLField(unique=True)),
                ('dependency', models.ManyToManyField(to='sitedata.JSLink')),
            ],
        ),
    ]
