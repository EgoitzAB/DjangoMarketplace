# Generated by Django 4.2.5 on 2023-10-11 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pago', '0003_alter_order_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaygreenWebhookMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_at', models.DateTimeField(help_text='When we received the event.')),
                ('payload', models.JSONField(default=None, null=True)),
            ],
            options={
                'indexes': [models.Index(fields=['received_at'], name='pago_paygre_receive_7fdf16_idx')],
            },
        ),
    ]
