# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0011_csslink_jslink'),
    ]

    operations = [
        migrations.CreateModel(
            name='DevBlogPost',
            fields=[
                ('post_id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', redactor.fields.RedactorField()),
                ('published', models.DateTimeField()),
                ('modified', models.DateTimeField(blank=True)),
                ('slug', models.SlugField(unique=True, max_length=250, blank=True)),
                ('headerimage', models.URLField(null=True, blank=True)),
                ('draft', models.BooleanField(default=False)),
                ('future', models.DateTimeField(null=True, blank=True)),
                ('css', models.ManyToManyField(to='sitedata.CSSLink', blank=True)),
                ('js', models.ManyToManyField(to='sitedata.JSLink', blank=True)),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='DevBlogSeries',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=250)),
                ('slug', models.SlugField(unique=True, max_length=250)),
                ('posts', models.ManyToManyField(to='devblog.DevBlogPost')),
            ],
        ),
    ]
