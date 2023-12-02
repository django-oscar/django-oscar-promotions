# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-08-02 15:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oscar_promotions', '0007_imageextrainfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imageextrainfo',
            name='image',
        ),
        migrations.AddField(
            model_name='timebasedpromotion',
            name='icon_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.DeleteModel(
            name='ImageExtraInfo',
        ),
    ]