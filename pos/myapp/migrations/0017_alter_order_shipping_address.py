# Generated by Django 4.1.7 on 2023-04-14 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0016_order_all_total_delivery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_address',
            field=models.CharField(default='YGN', max_length=255),
        ),
    ]
