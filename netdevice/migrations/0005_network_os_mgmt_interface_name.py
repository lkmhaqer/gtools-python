# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-09 03:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netdevice', '0004_auto_20190328_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='network_os',
            name='mgmt_interface_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
