# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-02 23:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_webgui', '0008_ipv6_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logical_interface',
            name='vlan',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]