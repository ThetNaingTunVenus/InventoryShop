# Generated by Django 4.1.7 on 2023-04-14 13:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0018_alter_order_shipping_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
