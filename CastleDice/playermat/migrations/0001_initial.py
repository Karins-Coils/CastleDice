# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("game", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="PlayerBuilt",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("card", models.CharField(max_length=52)),
                ("count", models.PositiveSmallIntegerField(default=1)),
                (
                    "adds_animal",
                    models.CharField(
                        max_length=16,
                        choices=[
                            (b"pig", b"pig"),
                            (b"horse", b"horse"),
                            (b"chicken", b"chicken"),
                            (b"cow", b"cow"),
                            (b"", b""),
                        ],
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerMat",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                ("victory_points", models.PositiveSmallIntegerField(default=0)),
                ("player_hand", annoying.fields.JSONField(null=True, blank=True)),
                (
                    "player_merchant_hand",
                    annoying.fields.JSONField(null=True, blank=True),
                ),
                ("player_order", models.PositiveSmallIntegerField(default=0)),
                ("has_porkchopped", models.BooleanField(default=False)),
                ("has_first_gathered", models.BooleanField(default=False)),
                ("choice_dice", annoying.fields.JSONField(null=True, blank=True)),
                ("horses", models.PositiveSmallIntegerField(default=0)),
                ("pigs", models.PositiveSmallIntegerField(default=0)),
                ("cows", models.PositiveSmallIntegerField(default=0)),
                ("chickens", models.PositiveSmallIntegerField(default=0)),
                ("wood", models.PositiveSmallIntegerField(default=0)),
                ("stone", models.PositiveSmallIntegerField(default=0)),
                ("gold", models.PositiveSmallIntegerField(default=0)),
                ("land", models.PositiveSmallIntegerField(default=0)),
                ("iron", models.PositiveSmallIntegerField(default=0)),
                ("merchants", models.PositiveSmallIntegerField(default=0)),
                ("farmers", models.PositiveSmallIntegerField(default=0)),
                ("game", models.ForeignKey(to="game.Game", on_delete=models.CASCADE)),
                (
                    "player",
                    models.ForeignKey(
                        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayerMatResourcePeople",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        serialize=False,
                        auto_created=True,
                        primary_key=True,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        max_length=12,
                        choices=[
                            (b"guard", b"guard"),
                            (b"worker", b"worker"),
                            (b"barbarian", b"barbarian"),
                        ],
                    ),
                ),
                ("total", models.PositiveSmallIntegerField(default=0)),
                ("wood", models.PositiveSmallIntegerField(default=0)),
                ("stone", models.PositiveSmallIntegerField(default=0)),
                ("gold", models.PositiveSmallIntegerField(default=0)),
                ("land", models.PositiveSmallIntegerField(default=0)),
                ("iron", models.PositiveSmallIntegerField(default=0)),
                (
                    "player_mat",
                    models.ForeignKey(
                        to="playermat.PlayerMat", on_delete=models.CASCADE
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="playerbuilt",
            name="player_mat",
            field=models.ForeignKey(to="playermat.PlayerMat", on_delete=models.CASCADE),
        ),
    ]
