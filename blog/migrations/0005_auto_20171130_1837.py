# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 16:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171130_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='key',
            name='is_used',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='key',
            name='owner',
            field=models.ForeignKey(default=12, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]