# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        ('playermat', '0003_auto_20160320_2030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playermat',
            name='choice_dice',
            field=annoying.fields.JSONField(default=[], null=True, blank=True),
        ),
    ]
