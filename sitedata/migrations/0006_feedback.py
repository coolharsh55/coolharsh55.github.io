# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0005_tag_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('text', ckeditor.fields.RichTextField()),
                ('published', models.DateTimeField()),
                ('user_name', models.CharField(max_length=250, verbose_name=b'Name', blank=True)),
                ('user_email', models.EmailField(max_length=150, null=True, verbose_name=b'Email', blank=True)),
                ('linked_post', models.URLField(max_length=250, null=True, verbose_name=b'Post URL', blank=True)),
                ('reply', ckeditor.fields.RichTextField(null=True, blank=True)),
                ('reply_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('-published',),
                'verbose_name': 'Anonymous Feedbacks',
            },
        ),
    ]
