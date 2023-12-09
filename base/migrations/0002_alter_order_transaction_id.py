# Generated by Django 4.2.7 on 2023-11-30 10:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]