# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roary', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='major',
        ),
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.CharField(default='Industrial Engineering & Operations Research', max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='dorm',
            field=models.CharField(default='Watt', max_length=120),
            preserve_default=False,
        ),
    ]
