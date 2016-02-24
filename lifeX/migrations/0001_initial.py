# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='LifeXBlog',
            fields=[
                ('post_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateField()),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'verbose_name': 'LifeX Blog',
                'verbose_name_plural': 'LifeX Blog',
            },
        ),
        migrations.CreateModel(
            name='LifeXCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250)),
            ],
            options={
                'verbose_name': 'LifeX Idea Category',
                'verbose_name_plural': 'LifeX Idea Categories',
            },
        ),
        migrations.CreateModel(
            name='LifeXIdea',
            fields=[
                ('idea_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(unique=True)),
                ('experimented', models.BooleanField(default=False, verbose_name=b'tried')),
                ('retry', models.BooleanField(default=False, verbose_name=b'retry?')),
                ('category', models.ForeignKey(to='lifeX.LifeXCategory')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'LifeX Idea',
                'verbose_name_plural': 'LifeX Ideas',
            },
        ),
        migrations.CreateModel(
            name='LifeXPost',
            fields=[
                ('post_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField(unique=True)),
                ('date', models.DateField()),
                ('idea', models.ForeignKey(to='lifeX.LifeXIdea')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'verbose_name': 'LifeX Post',
                'verbose_name_plural': 'LifeX Posts',
            },
        ),
        migrations.CreateModel(
            name='LifeXWeek',
            fields=[
                ('number', models.AutoField(serialize=False, verbose_name=b'Week#', primary_key=True)),
            ],
            options={
                'verbose_name': 'LifeX Week',
                'verbose_name_plural': 'LifeX Weeks',
            },
        ),
        migrations.AddField(
            model_name='lifexpost',
            name='week',
            field=models.ForeignKey(to='lifeX.LifeXWeek'),
        ),
    ]
