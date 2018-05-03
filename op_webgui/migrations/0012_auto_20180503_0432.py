# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-03 04:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('op_webgui', '0011_auto_20180503_0028'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipv4_address',
            name='interface',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='op_webgui.logical_interface'),
        ),
        migrations.AlterField(
            model_name='ipv6_address',
            name='interface',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='op_webgui.logical_interface'),
        ),
    ]
