# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2017-12-24 14:38
from __future__ import unicode_literals

import accounts.managers
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20171223_1012'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', accounts.managers.AccountsUserManager()),
            ],
        ),
    ]
