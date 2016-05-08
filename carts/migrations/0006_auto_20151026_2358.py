# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0005_cartitem_line_item_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='line_item_total',
            field=models.DecimalField(default=499.99, max_digits=10, decimal_places=2),
        ),
    ]
