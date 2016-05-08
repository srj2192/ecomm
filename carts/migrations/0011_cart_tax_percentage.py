# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0010_auto_20151028_0751'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax_percentage',
            field=models.DecimalField(default=0.085, max_digits=40, decimal_places=5),
        ),
    ]
