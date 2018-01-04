# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-03 16:14
from __future__ import unicode_literals

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportantDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=20)),
                ('due_date', blog.models.IntegerRangeField()),
            ],
        ),
    ]
