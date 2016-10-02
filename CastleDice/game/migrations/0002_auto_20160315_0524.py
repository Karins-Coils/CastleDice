# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedeck',
            name='game',
        ),
        migrations.AddField(
            model_name='game',
            name='is_solo_game',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='GameDeck',
        ),
    ]
