# Generated by Django 4.2.7 on 2023-11-20 19:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_alter_customer_address_alter_customer_country'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
