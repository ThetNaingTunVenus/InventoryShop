# Generated by Django 4.2.1 on 2023-05-24 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0028_damageitems_return_delivery_charge'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='wholesale_price',
            field=models.FloatField(default=0.0),
        ),
    ]
