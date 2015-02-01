# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Song',
            fields=[
                ('url', models.CharField(max_length=200, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('year', models.CharField(max_length=200)),
                ('genre', models.CharField(max_length=200)),
                ('artist', models.CharField(max_length=200)),
                ('plays', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uni', models.CharField(max_length=10, serialize=False, primary_key=True)),
                ('major', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='song',
            name='owner',
            field=models.ManyToManyField(to='roary.User'),
            preserve_default=True,
        ),
    ]
