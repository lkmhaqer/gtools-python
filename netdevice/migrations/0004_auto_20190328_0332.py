# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-03-28 03:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('netdevice', '0003_create_network_os'),
    ]

    operations = [
        migrations.CreateModel(
            name='vrf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vrf_name', models.CharField(max_length=255)),
                ('vrf_target', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='logical_interface',
            name='vrf',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='netdevice.vrf'),
        ),
    ]