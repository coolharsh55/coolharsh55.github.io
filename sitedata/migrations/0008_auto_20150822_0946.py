# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import redactor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sitedata', '0007_auto_20150819_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='linked_post',
            field=models.URLField(help_text=b'(optional) URL of the post/page you wish to give your feedback on. Leave it blank for a general feedback.', max_length=250, null=True, verbose_name=b'Post URL', blank=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='text',
            field=redactor.fields.RedactorField(help_text=b'Enter the text of the feedback here.'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='title',
            field=models.CharField(help_text=b'A title is needed for the feedback you wish to give.', max_length=250),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='user_email',
            field=models.EmailField(help_text=b'Email (optional) will be used to send you the reply to this feedback. Replies will also be published on site without any personal details such as name/email.', max_length=150, null=True, verbose_name=b'Email', blank=True),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='user_name',
            field=models.CharField(default=b'Anonymous', help_text=b'Leave name blank for an Anonymous feedback. If you enter your name, only I will be able to see it.', max_length=250, verbose_name=b'Name', blank=True),
        ),
    ]
