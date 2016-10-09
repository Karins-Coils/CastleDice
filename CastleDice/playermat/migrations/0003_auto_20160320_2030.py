# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playermat', '0002_auto_20160315_0443'),
    ]

    operations = [
        migrations.AddField(
            model_name='playermat',
            name='has_farmered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='joanplayermat',
            name='primary_resource',
            field=models.CharField(blank=True, max_length=12, null=True, choices=[(b'iron', b'iron'), (b'land', b'land'), (b'gold', b'gold'), (b'stone', b'stone'), (b'wood', b'wood'), (None, None)]),
        ),
        migrations.AlterField(
            model_name='playerbuilt',
            name='adds_animal',
            field=models.CharField(max_length=16, choices=[(b'pig', b'pig'), (b'horse', b'horse'), (b'chicken', b'chicken'), (b'cow', b'cow'), (b'', b'')]),
        ),
        migrations.AlterField(
            model_name='playermatresourcepeople',
            name='type',
            field=models.CharField(max_length=12, choices=[(b'guard', b'guard'), (b'worker', b'worker'), (b'barbarian', b'barbarian')]),
        ),
        migrations.AlterUniqueTogether(
            name='playermatresourcepeople',
            unique_together=set([('player_mat', 'type')]),
        ),
    ]
