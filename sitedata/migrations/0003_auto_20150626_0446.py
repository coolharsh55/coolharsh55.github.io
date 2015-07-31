# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0002_book'),
    ]

    operations = [
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
                'ordering': ('title', 'date_start', 'date_end', 'finished'),
                'verbose_name': 'Video Game',
                'verbose_name_plural': 'Video Games',
            },
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('date_seen', models.DateField(verbose_name=b'Seen on')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('title', 'date_seen'),
            },
        ),
        migrations.CreateModel(
            name='TVShow',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('date_start', models.DateField(verbose_name=b'Started')),
                ('date_end', models.DateField(verbose_name=b'Finished')),
                ('watched', models.BooleanField(default=False, verbose_name=b'Finished?')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('title', 'date_start', 'date_end', 'watched'),
                'verbose_name': 'TV Show',
                'verbose_name_plural': 'TV Shows',
            },
        ),
        migrations.AlterField(
            model_name='book',
            name='date_start',
            field=models.DateField(verbose_name=b'Started'),
        ),
        migrations.AlterField(
            model_name='book',
            name='slug',
            field=models.SlugField(unique=True, max_length=200),
        ),
    ]
