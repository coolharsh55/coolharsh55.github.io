# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('read', models.BooleanField(default=False, verbose_name=b'read?')),
                ('date_start', models.DateField(verbose_name=b'Started')),
                ('date_end', models.DateField(verbose_name=b'Finished', blank=True)),
            ],
            options={
                'ordering': ('title', 'date_start', 'date_end'),
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
            ],
            options={
                'ordering': ('title', 'date_seen'),
            },
        ),
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
        migrations.AddField(
            model_name='movie',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag'),
        ),
        migrations.AddField(
            model_name='game',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag'),
        ),
        migrations.AddField(
            model_name='book',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag'),
        ),
    ]
