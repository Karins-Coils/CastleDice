# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import annoying.fields


class Migration(migrations.Migration):

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Game",
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
                ("current_turn", models.PositiveSmallIntegerField(default=1)),
                ("current_phase", models.PositiveSmallIntegerField(default=1)),
                ("choice_dice", annoying.fields.JSONField(null=True, blank=True)),
                ("gather_dice", annoying.fields.JSONField(null=True, blank=True)),
                ("true_porkchop_used", models.BooleanField(default=False)),
                (
                    "current_player",
                    models.ForeignKey(
                        related_name="+",
                        on_delete=models.CASCADE,
                        blank=True,
                        to=settings.AUTH_USER_MODEL,
                        null=True,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="GameDeck",
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
                    "deck",
                    models.CharField(
                        max_length=12,
                        choices=[
                            (b"castle", b"castle"),
                            (b"villager", b"villager"),
                            (b"market", b"market"),
                        ],
                    ),
                ),
                ("draw_pile", models.CharField(max_length=500)),
                ("discard_pile", models.CharField(max_length=500)),
                ("game", models.ManyToManyField(to="game.Game")),
            ],
        ),
    ]
