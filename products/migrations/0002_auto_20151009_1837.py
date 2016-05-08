# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Variation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=120)),
                ('price', models.DecimalField(max_digits=12, decimal_places=2)),
                ('sale_price', models.DecimalField(null=True, max_digits=12, decimal_places=2, blank=True)),
                ('active', models.BooleanField(default=True)),
                ('inventory', models.IntegerField(null=True, blank=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(max_digits=12, decimal_places=2),
        ),
        migrations.AddField(
            model_name='variation',
            name='product',
            field=models.ForeignKey(to='products.Product'),
        ),
    ]
