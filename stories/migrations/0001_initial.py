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
            name='StoryPost',
            fields=[
                ('post_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('published', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('slug', models.CharField(unique=True, max_length=50)),
                ('headerimage', models.URLField(blank=True)),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'verbose_name': 'Story',
                'verbose_name_plural': 'Stories',
            },
        ),
    ]
