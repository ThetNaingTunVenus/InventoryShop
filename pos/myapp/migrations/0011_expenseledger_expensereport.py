# Generated by Django 4.1.7 on 2023-04-08 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_purchaselist'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExpenseLedger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=225, unique=True)),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense_type', models.CharField(max_length=225)),
                ('title', models.CharField(max_length=225)),
                ('category', models.CharField(max_length=225)),
                ('amount', models.IntegerField(default=0)),
                ('expense_date', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
