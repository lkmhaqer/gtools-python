# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-28 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netdevice', '0004_auto_20190328_0332'),
        ('static', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ipv4_static',
            name='vrf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='netdevice.vrf'),
        ),
        migrations.AddField(
            model_name='ipv6_static',
            name='vrf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='netdevice.vrf'),
        ),
    ]
