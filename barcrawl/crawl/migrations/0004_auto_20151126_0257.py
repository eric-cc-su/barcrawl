# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0003_bar_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bar',
            name='address',
            field=models.CharField(max_length=400),
        ),
    ]
