# Generated by Django 5.0.7 on 2024-07-22 08:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_product_ingredients_alter_product_toppings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='product_photos/', verbose_name='Фото'),
        ),
    ]
