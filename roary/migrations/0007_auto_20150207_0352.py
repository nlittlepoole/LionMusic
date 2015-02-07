# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roary', '0006_auto_20150207_0236'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='art',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queue',
            name='timestamp',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='art',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
