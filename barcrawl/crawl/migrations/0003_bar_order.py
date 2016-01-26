# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0002_auto_20151104_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='bar',
            name='order',
            field=models.IntegerField(default=0),
        ),
    ]
