# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-05-06 14:37
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='aut_num',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asn', models.BigIntegerField(unique=True)),
                ('name', models.CharField(max_length=255)),
                ('contact', models.EmailField(blank=True, max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('mtu', models.BigIntegerField(default=1514)),
                ('dot1q', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ipv4_address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.GenericIPAddressField(unpack_ipv4=True)),
                ('cidr', models.PositiveSmallIntegerField(default=24)),
            ],
        ),
        migrations.CreateModel(
            name='ipv6_address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.GenericIPAddressField()),
                ('cidr', models.PositiveSmallIntegerField(default=64)),
            ],
        ),
        migrations.CreateModel(
            name='logical_interface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=1024)),
                ('mtu', models.BigIntegerField(default=1500)),
                ('vlan', models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(4096)])),
                ('physical_interface', models.BooleanField(default=False)),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='op_webgui.interface')),
            ],
        ),
        migrations.CreateModel(
            name='neighbor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peer_ip', models.GenericIPAddressField(unpack_ipv4=True)),
                ('soft_inbound', models.BooleanField(default=True)),
                ('aut_num', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='op_webgui.aut_num')),
            ],
        ),
        migrations.CreateModel(
            name='network_os',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='router',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('routing_id', models.GenericIPAddressField(unpack_ipv4=True)),
                ('hostname', models.CharField(max_length=255)),
                ('ibgp', models.BooleanField()),
                ('service_ssh', models.BooleanField(default=True)),
                ('service_netconf', models.BooleanField(default=True)),
                ('network_os', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='op_webgui.network_os')),
            ],
        ),
        migrations.AddField(
            model_name='neighbor',
            name='router',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='op_webgui.router'),
        ),
        migrations.AddField(
            model_name='ipv6_address',
            name='interface',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='op_webgui.logical_interface'),
        ),
        migrations.AddField(
            model_name='ipv4_address',
            name='interface',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='op_webgui.logical_interface'),
        ),
        migrations.AddField(
            model_name='interface',
            name='router',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='op_webgui.router'),
        ),
    ]
