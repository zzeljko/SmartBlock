# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 16:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20180103_1822'),
    ]

    operations = [
        migrations.RenameField(
            model_name='importantdate',
            old_name='text',
            new_name='description',
        ),
    ]