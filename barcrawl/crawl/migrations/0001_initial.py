# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bar',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=200)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('date', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Distance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('distance', models.PositiveIntegerField()),
                ('end', models.ForeignKey(related_name='end', to='crawl.City')),
                ('start', models.ForeignKey(related_name='start', to='crawl.City')),
            ],
        ),
        migrations.AddField(
            model_name='bar',
            name='city',
            field=models.ForeignKey(to='crawl.City'),
        ),
    ]
