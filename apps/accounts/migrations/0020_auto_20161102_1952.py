# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-11-02 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20161102_1931'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='remaining_user_invites',
            field=models.IntegerField(default=1),
        ),
    ]
