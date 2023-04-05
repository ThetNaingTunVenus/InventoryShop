# Generated by Django 4.1.7 on 2023-03-31 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=225)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=225)),
                ('category', models.CharField(max_length=225)),
                ('pruchase_price', models.FloatField(default=0.0)),
                ('sell_price', models.FloatField(default=0.0)),
                ('balance_qty', models.IntegerField(default=0)),
            ],
        ),
    ]