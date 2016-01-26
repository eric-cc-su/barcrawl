# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawl', '0004_auto_20151126_0257'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bar',
            old_name='order',
            new_name='priority',
        ),
    ]
