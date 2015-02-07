# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roary', '0003_song_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='google_music_time',
            field=models.CharField(default=0, max_length=120),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='soundcloud_music_time',
            field=models.CharField(default='0', max_length=120),
            preserve_default=False,
        ),
    ]
