# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doi_suffix', models.CharField(max_length=100, verbose_name=b'DOI suffix - http://1234.5432.')),
                ('group', models.OneToOneField(to='auth.Group', on_delete=models.CASCADE)),
            ],
        ),
    ]
