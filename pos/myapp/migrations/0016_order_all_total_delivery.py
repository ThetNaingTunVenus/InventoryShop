# Generated by Django 4.1.7 on 2023-04-14 09:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_order_delivery_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='all_total_delivery',
            field=models.IntegerField(default=0),
        ),
    ]
