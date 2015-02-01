# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roary', '0002_auto_20150131_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='duration',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
