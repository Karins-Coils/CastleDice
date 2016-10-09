# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playermat', '0004_auto_20160321_0530'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joanplayermat',
            name='primary_resource',
            field=models.CharField(blank=True, null=True, max_length=12, choices=[('iron', 'iron'), ('land', 'land'), ('gold', 'gold'), ('stone', 'stone'), ('wood', 'wood'), (None, None)]),
        ),
        migrations.AlterField(
            model_name='playerbuilt',
            name='adds_animal',
            field=models.CharField(max_length=16, choices=[('pig', 'pig'), ('horse', 'horse'), ('chicken', 'chicken'), ('cow', 'cow'), ('', '')]),
        ),
        migrations.AlterField(
            model_name='playermatresourcepeople',
            name='type',
            field=models.CharField(max_length=12, choices=[('guard', 'guard'), ('worker', 'worker'), ('barbarian', 'barbarian')]),
        ),
    ]
