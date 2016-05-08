# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0006_auto_20151026_2358'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='subtotal',
            field=models.DecimalField(default=0, max_digits=50, decimal_places=2),
        ),
    ]
