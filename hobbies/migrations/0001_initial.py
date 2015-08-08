# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0003_auto_20150808_0654'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('date_start', models.DateField(verbose_name=b'Started')),
                ('date_end', models.DateField(null=True, verbose_name=b'Completed', blank=True)),
                ('finished', models.BooleanField(default=False, verbose_name=b'Finished?')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('-date_start', '-date_end', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('date_start', models.DateField(verbose_name=b'Started')),
                ('date_end', models.DateField(verbose_name=b'Finished')),
                ('finished', models.BooleanField(default=False, verbose_name=b'Finished?')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('-date_start', '-date_end', 'title', 'finished'),
                'verbose_name': 'Video Game',
                'verbose_name_plural': 'Video Games',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('date_seen', models.DateField(verbose_name=b'Seen on')),
                ('finished', models.BooleanField(default=False, verbose_name=b'Finished?')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('-date_seen', 'title', 'finished'),
            },
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('date_start', models.DateField(verbose_name=b'Started')),
                ('date_end', models.DateField(verbose_name=b'Finished')),
                ('finished', models.BooleanField(default=False, verbose_name=b'Finished?')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('-date_start', '-date_end', 'title', 'finished'),
                'verbose_name': 'TV Show',
                'verbose_name_plural': 'TV Shows',
            },
        ),
    ]
