# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 16:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20171130_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pollquestion',
            name='pub_date',
        ),
        migrations.AddField(
            model_name='pollquestion',
            name='choice',
            field=models.CharField(default=12, max_length=200),
            preserve_default=False,
        ),
    ]