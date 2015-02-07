# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roary', '0005_user_spotify_music_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='Queue',
            fields=[
                ('url', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('position', models.IntegerField()),
                ('plays', models.IntegerField()),
                ('users', models.IntegerField()),
                ('owner', models.ManyToManyField(to='roary.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='song',
            name='users',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
