# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'verbose_name': 'Article post', 'verbose_name_plural': 'Article posts'},
        ),
        migrations.AlterField(
            model_name='article',
            name='headerimage',
            field=models.URLField(verbose_name=b'Header Image', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='modified',
            field=models.DateTimeField(verbose_name=b'Last Modified'),
        ),
        migrations.AlterField(
            model_name='article',
            name='post_id',
            field=models.AutoField(serialize=False, verbose_name=b'Post #', primary_key=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='published',
            field=models.DateTimeField(verbose_name=b'Published'),
        ),
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='sitedata.Tag', verbose_name=b'Tags'),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=250, verbose_name=b'Article Title'),
        ),
    ]
