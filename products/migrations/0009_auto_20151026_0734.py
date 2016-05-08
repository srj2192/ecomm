# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0008_productfeatured_text_css_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfeatured',
            name='text_css_color',
            field=models.CharField(max_length=16, null=True, blank=True),
        ),
    ]
