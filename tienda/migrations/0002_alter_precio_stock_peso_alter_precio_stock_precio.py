# Generated by Django 4.2.5 on 2023-09-23 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='precio_stock',
            name='peso',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='precio_stock',
            name='precio',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
    ]
