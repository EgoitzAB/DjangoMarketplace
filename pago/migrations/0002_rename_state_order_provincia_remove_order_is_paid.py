# Generated by Django 4.2.5 on 2023-09-25 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pago', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='state',
            new_name='provincia',
        ),
        migrations.RemoveField(
            model_name='order',
            name='is_paid',
        ),
    ]
