# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-04 01:19
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180103_1823'),
    ]

    operations = [
        migrations.CreateModel(
            name='OtherImportantContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=30)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex=b'^\\+?1?\\d{9,15}$')])),
                ('email', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.AlterField(
            model_name='importantdate',
            name='description',
            field=models.CharField(max_length=30),
        ),
    ]
