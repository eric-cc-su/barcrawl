# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0005_auto_20151126_0309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distance',
            name='end',
            field=models.ForeignKey(related_name='end', to='crawl.Bar'),
        ),
        migrations.AlterField(
            model_name='distance',
            name='start',
            field=models.ForeignKey(related_name='start', to='crawl.Bar'),
        ),
    ]
