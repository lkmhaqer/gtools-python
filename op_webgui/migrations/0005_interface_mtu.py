# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-02 23:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('op_webgui', '0004_interface'),
    ]

    operations = [
        migrations.AddField(
            model_name='interface',
            name='mtu',
            field=models.BigIntegerField(default=1500),
        ),
    ]