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
            name='Article',
            fields=[
                ('post_id', models.AutoField(serialize=False, verbose_name=b'Post #', primary_key=True)),
                ('title', models.CharField(max_length=250, verbose_name=b'Article Title')),
                ('body', ckeditor.fields.RichTextField()),
                ('published', models.DateTimeField(verbose_name=b'Published')),
                ('modified', models.DateTimeField(verbose_name=b'Last Modified')),
                ('slug', models.SlugField(unique=True)),
                ('headerimage', models.URLField(verbose_name=b'Header Image', blank=True)),
                ('tags', models.ManyToManyField(to='sitedata.Tag', verbose_name=b'Tags')),
            ],
            options={
                'verbose_name': 'Article post',
                'verbose_name_plural': 'Article posts',
            },
        ),
    ]
