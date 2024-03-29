# Generated by Django 3.1.13 on 2021-10-03 05:26

import annoying.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import json


class Migration(migrations.Migration):

    replaces = [('playermat', '0001_initial'), ('playermat', '0002_auto_20160315_0443'), ('playermat', '0003_auto_20160320_2030'), ('playermat', '0004_auto_20160321_0530'), ('playermat', '0005_auto_20161009_0505'), ('playermat', '0006_auto_20191130_0425'), ('playermat', '0007_auto_20211002_1940'), ('playermat', '0008_auto_20211002_2220')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerMat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('victory_points', models.PositiveSmallIntegerField(default=0)),
                ('player_hand', annoying.fields.JSONField(blank=True, deserializer=json.loads, null=True, serializer=annoying.fields.dumps)),
                ('player_merchant_hand', annoying.fields.JSONField(blank=True, deserializer=json.loads, null=True, serializer=annoying.fields.dumps)),
                ('player_order', models.PositiveSmallIntegerField(default=0)),
                ('has_porkchopped', models.BooleanField(default=False)),
                ('has_first_gathered', models.BooleanField(default=False)),
                ('choice_dice', annoying.fields.JSONField(blank=True, default=[], deserializer=json.loads, null=True, serializer=annoying.fields.dumps)),
                ('horses', models.PositiveSmallIntegerField(default=0)),
                ('pigs', models.PositiveSmallIntegerField(default=0)),
                ('cows', models.PositiveSmallIntegerField(default=0)),
                ('chickens', models.PositiveSmallIntegerField(default=0)),
                ('wood', models.PositiveSmallIntegerField(default=0)),
                ('stone', models.PositiveSmallIntegerField(default=0)),
                ('gold', models.PositiveSmallIntegerField(default=0)),
                ('land', models.PositiveSmallIntegerField(default=0)),
                ('iron', models.PositiveSmallIntegerField(default=0)),
                ('merchants', models.PositiveSmallIntegerField(default=0)),
                ('farmers', models.PositiveSmallIntegerField(default=0)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('has_farmered', models.BooleanField(default=False)),
                ('barbarians', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='JoanPlayerMat',
            fields=[
                ('playermat_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='playermat.playermat')),
                ('primary_resource', models.CharField(blank=True, choices=[('iron', 'iron'), ('land', 'land'), ('gold', 'gold'), ('stone', 'stone'), ('wood', 'wood'), (None, None)], max_length=12, null=True)),
            ],
            bases=('playermat.playermat',),
        ),
        migrations.CreateModel(
            name='PlayerBuilt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(max_length=52)),
                ('count', models.PositiveSmallIntegerField(default=1)),
                ('adds_animal', models.CharField(choices=[('pig', 'pig'), ('horse', 'horse'), ('chicken', 'chicken'), ('cow', 'cow'), ('', '')], max_length=16)),
                ('player_mat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playermat.playermat')),
            ],
        ),
        migrations.CreateModel(
            name='PlayerMatResourcePeople',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(51, 'GUARD'), (50, 'WORKER')])),
                ('total', models.PositiveSmallIntegerField(default=0)),
                ('wood', models.BooleanField(default=False)),
                ('stone', models.BooleanField(default=False)),
                ('gold', models.BooleanField(default=False)),
                ('land', models.BooleanField(default=False)),
                ('iron', models.BooleanField(default=False)),
                ('player_mat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playermat.playermat')),
            ],
            options={
                'unique_together': {('player_mat', 'type')},
            },
        ),
    ]
