# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roary', '0004_auto_20150207_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='spotify_music_time',
            field=models.CharField(default='0', max_length=120),
            preserve_default=False,
        ),
    ]
