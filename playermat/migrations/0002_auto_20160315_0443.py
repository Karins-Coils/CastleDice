# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('playermat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JoanPlayerMat',
            fields=[
                ('playermat_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='playermat.PlayerMat')),
                ('primary_resource', models.CharField(blank=True, max_length=12, null=True, choices=[(b'Iron', b'Iron'), (b'Land', b'Land'), (b'Gold', b'Gold'), (b'Stone', b'Stone'), (b'Wood', b'Wood')])),
            ],
            bases=('playermat.playermat',),
        ),
        migrations.AlterField(
            model_name='playerbuilt',
            name='adds_animal',
            field=models.CharField(max_length=16, choices=[(b'Pig', b'Pig'), (b'Horse', b'Horse'), (b'Chicken', b'Chicken'), (b'Cow', b'Cow'), (b'', b'')]),
        ),
        migrations.AlterField(
            model_name='playermatresourcepeople',
            name='type',
            field=models.CharField(max_length=b'12', choices=[(b'Guard', b'Guard'), (b'Worker', b'Worker'), (b'Barbarian', b'Barbarian')]),
        ),
    ]
