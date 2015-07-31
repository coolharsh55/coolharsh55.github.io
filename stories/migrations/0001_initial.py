# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StoryPost',
            fields=[
                ('post_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('published', models.DateTimeField()),
                ('modified', models.DateTimeField(auto_now=True)),
                ('headerimage', models.URLField(blank=True)),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'ordering': ('-published', 'title'),
            },
        ),
    ]
