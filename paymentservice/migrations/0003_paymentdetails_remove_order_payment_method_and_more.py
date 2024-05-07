# Generated by Django 5.0.4 on 2024-05-05 22:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paymentservice', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_method', models.CharField(max_length=50)),
                ('credit_card_number', models.CharField(max_length=16)),
                ('credit_card_expiry', models.DateField()),
                ('payment_date', models.DateTimeField()),
                ('payment_amount', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='payment_method',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_set',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='paymentservice.paymentdetails'),
        ),
    ]
