# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-04 07:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Stegano', '0005_auto_20171204_1609'),
    ]

    operations = [
        migrations.RenameField(
            model_name='saveinfo',
            old_name='ACCESS_TIME',
            new_name='access_time',
        ),
        migrations.RenameField(
            model_name='saveinfo',
            old_name='ENCRPY_KEY',
            new_name='input_key',
        ),
        migrations.RenameField(
            model_name='saveinfo',
            old_name='PLAIN_TEXT',
            new_name='input_msg',
        ),
        migrations.RenameField(
            model_name='saveinfo',
            old_name='USER_AGENT',
            new_name='user_agent',
        ),
        migrations.RenameField(
            model_name='saveinfo',
            old_name='USER_IP',
            new_name='user_ip',
        ),
    ]