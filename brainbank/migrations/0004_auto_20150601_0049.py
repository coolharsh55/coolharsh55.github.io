# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('brainbank', '0003_auto_20150601_0006'),
    ]

    operations = [
        migrations.CreateModel(
            name='BrainBankDemo',
            fields=[
                ('_id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('js', ckeditor.fields.RichTextField(verbose_name=b'javascript')),
                ('css', ckeditor.fields.RichTextField(verbose_name=b'CSS')),
                ('body', ckeditor.fields.RichTextField(verbose_name=b'content')),
            ],
            options={
                'verbose_name': 'BrainBank Idea Demo',
                'verbose_name_plural': 'BrainBank Ideas Demos',
            },
        ),
        migrations.CreateModel(
            name='BrainBankIdea',
            fields=[
                ('_id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
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
                ('_id', models.AutoField(serialize=False, verbose_name=b'ID', primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('body', ckeditor.fields.RichTextField()),
                ('published', models.DateField()),
                ('idea', models.ForeignKey(to='brainbank.BrainBankIdea')),
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
