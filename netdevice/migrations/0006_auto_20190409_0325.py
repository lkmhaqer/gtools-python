# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-09 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netdevice', '0005_network_os_mgmt_interface_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='interface',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='logical_interface',
            name='disabled',
            field=models.BooleanField(default=False),
        ),
    ]