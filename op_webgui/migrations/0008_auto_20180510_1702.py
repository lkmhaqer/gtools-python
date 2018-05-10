# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-10 17:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('op_webgui', '0007_ipv4_static_ipv6_static'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipv4_static',
            name='router',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='op_webgui.router'),
        ),
        migrations.AlterField(
            model_name='ipv6_static',
            name='router',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='op_webgui.router'),
        ),
    ]
