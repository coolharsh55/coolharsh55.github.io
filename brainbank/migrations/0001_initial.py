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
            name='BrainBankDemo',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('js', ckeditor.fields.RichTextField(verbose_name=b'javascript')),
                ('css', ckeditor.fields.RichTextField(verbose_name=b'CSS')),
                ('body', ckeditor.fields.RichTextField(verbose_name=b'content')),
                ('slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'BrainBank Idea Demo',
                'verbose_name_plural': 'BrainBank Ideas Demos',
            },
        ),
        migrations.CreateModel(
            name='BrainBankIdea',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('slug', models.SlugField()),
                ('published', models.DateField()),
            ],
            options={
                'verbose_name': 'BrainBank Idea',
                'verbose_name_plural': 'BrainBank Ideas',
            },
        ),
        migrations.CreateModel(
            name='BrainBankPost',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('published', models.DateField()),
                ('slug', models.SlugField(unique=True)),
                ('idea', models.ForeignKey(to='brainbank.BrainBankIdea')),
                ('tags', models.ManyToManyField(to='sitedata.Tag')),
            ],
            options={
                'verbose_name': 'BrainBank Idea Post',
                'verbose_name_plural': 'BrainBank Idea Posts',
            },
        ),
        migrations.AddField(
            model_name='brainbankdemo',
            name='idea',
            field=models.ForeignKey(to='brainbank.BrainBankIdea'),
        ),
    ]
