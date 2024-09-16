# Generated by Django 5.0.7 on 2024-09-16 08:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0019_alter_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PromoCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10, unique=True, verbose_name='Промокод')),
                ('valid_from', models.DateTimeField(verbose_name='Начало действия')),
                ('valid_to', models.DateTimeField(verbose_name='Конец действия')),
                ('discount', models.IntegerField(help_text='Процент скидки', verbose_name='Скидка')),
                ('active', models.BooleanField(default=False, verbose_name='Активен')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='promo_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.promocode'),
        ),
    ]
