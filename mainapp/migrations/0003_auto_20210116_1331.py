# Generated by Django 3.1.5 on 2021-01-16 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_orders_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.CharField(default='default', max_length=20),
        ),
    ]