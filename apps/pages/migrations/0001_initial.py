# Generated by Django 5.0.7 on 2024-07-22 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=123, null=True, verbose_name='Заголовок')),
                ('image_desktop', models.ImageField(upload_to='images/banners/desktop/%Y/%m/', verbose_name='Картинка круп')),
                ('image_mobile', models.ImageField(upload_to='images/banners/mobile/%Y/%m/', verbose_name='Картинка моб')),
                ('link', models.URLField(blank=True, null=True, verbose_name='ссылка')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активный')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Дата создания')),
            ],
            options={
                'verbose_name': 'Баннер',
                'verbose_name_plural': 'Баннеры',
                'ordering': ['is_active', '-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Контакты',
                'verbose_name_plural': 'Контакты',
            },
        ),
        migrations.CreateModel(
            name='MainPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(help_text='Иконка для главной страницы.', upload_to='images/icons', verbose_name='Иконка')),
                ('phone', models.CharField(help_text='Контактный телефон для главной страницы.', max_length=20, verbose_name='Телефон')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета заголовок')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета описание')),
                ('meta_image', models.ImageField(blank=True, null=True, upload_to='images/meta', verbose_name='Мета изображение')),
            ],
            options={
                'verbose_name': 'Главная страница',
                'verbose_name_plural': 'Главная страница',
            },
        ),
        migrations.CreateModel(
            name='StaticPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('title_ru', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('title_ky', models.CharField(max_length=255, null=True, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('description_ru', models.TextField(null=True, verbose_name='Описание')),
                ('description_ky', models.TextField(null=True, verbose_name='Описание')),
                ('slug', models.SlugField(blank=True, null=True, unique=True, verbose_name='Слоган')),
                ('meta_title', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета заголовок')),
                ('meta_description', models.CharField(blank=True, max_length=255, null=True, verbose_name='Мета описание')),
                ('meta_image', models.ImageField(blank=True, null=True, upload_to='images/meta', verbose_name='Мета изображение')),
            ],
            options={
                'verbose_name': 'Статическая страница',
                'verbose_name_plural': 'Статические страницы',
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=255)),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Адрес',
                'verbose_name_plural': 'Адреса',
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=255)),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Имейл',
                'verbose_name_plural': 'Имейлы',
            },
        ),
        migrations.CreateModel(
            name='DeliveryConditions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='delivery_conditions', to='pages.mainpage')),
            ],
        ),
        migrations.CreateModel(
            name='MethodsOfPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='methods_of_payment', to='pages.mainpage')),
            ],
        ),
        migrations.CreateModel(
            name='OrderTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Изображение')),
                ('title', models.CharField(max_length=255, verbose_name='Заголовок')),
                ('description', models.TextField(verbose_name='Описание')),
                ('page', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.mainpage')),
            ],
        ),
        migrations.CreateModel(
            name='PaymentMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('icon', models.FileField(upload_to='payment_icons')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Ссылка для оплаты',
                'verbose_name_plural': 'Ссылки для оплаты',
            },
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=100)),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Телефон',
                'verbose_name_plural': 'Телефоны',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('icon', models.FileField(upload_to='social_icons')),
                ('contacts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pages.contacts')),
            ],
            options={
                'verbose_name': 'Ссылка соцсети',
                'verbose_name_plural': 'Ссылки соцсетей',
            },
        ),
    ]
