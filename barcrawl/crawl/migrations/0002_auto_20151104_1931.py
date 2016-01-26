# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='lat',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='bar',
            name='lng',
            field=models.FloatField(default=0.0),
        ),
    ]
