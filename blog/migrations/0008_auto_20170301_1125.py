# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-01 09:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_auto_20170226_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='post',
        ),
        migrations.DeleteModel(
            name='Image',
        ),
    ]
