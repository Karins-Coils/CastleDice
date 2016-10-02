# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20160315_0524'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='choice_dice',
            field=annoying.fields.JSONField(default=[], null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='game',
            name='gather_dice',
            field=annoying.fields.JSONField(default={}, null=True, blank=True),
        ),
    ]
