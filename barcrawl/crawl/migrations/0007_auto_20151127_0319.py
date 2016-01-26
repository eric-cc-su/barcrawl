# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0006_auto_20151127_0318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distance',
            name='end',
            field=models.ForeignKey(related_name='end', to='crawl.City'),
        ),
    ]
