from io import BytesIO
from PIL import Image
from colorfield.fields import ColorField
from django.core.files.base import ContentFile
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from unidecode import unidecode


class Size(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Название'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('Описание'))

    class Meta:
        verbose_name = "Размер"
        verbose_name_plural = "Размеры"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    text_color = ColorField(default='#FF0000', format='hex', verbose_name=_('Цвет текста'))
    background_color = ColorField(default='#FF0000', format='hex', verbose_name=_('Цвет фона'))

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Название'))
    description = models.CharField(max_length=100, blank=True, verbose_name=_('Описание'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Ссылка'), blank=True, null=True)
    image = models.FileField(upload_to='category_photos/', verbose_name=_('Фото'), blank=True, null=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/admin/product/category/{self.id}/change/"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(unidecode(self.name))
        super().save(*args, **kwargs)


class Product(models.Model):
    is_popular = models.BooleanField(default=False, verbose_name=_('Популярный'))
    is_new = models.BooleanField(default=False, verbose_name=_('Новинка'))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категория'),
                                 related_name='products', blank=True, null=True)
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)
    photo = models.FileField(upload_to='product_photos/', verbose_name=_('Фото'), blank=True, null=True)
    toppings = models.ManyToManyField('Topping', related_name='products', verbose_name=_('Добавки'), blank=True)
    bonuses = models.BooleanField(default=False, verbose_name=_('Можно оптатить бонусами'))
    tags = models.ManyToManyField('Tag', related_name='products', verbose_name=_('Теги'), blank=True)
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f"/admin/product/product/{self.id}/change/"

    def get_min_price(self):
        prices = [size.discounted_price if size.discounted_price else size.price for size in self.product_sizes.all()]
        return min(prices) if prices else None

    def save(self, *args, **kwargs):
        if self.photo and not self.photo.name.endswith('.webp'):
            image = Image.open(self.photo)

            max_width = 800
            max_height = 800

            # Получение оригинальных размеров изображения
            original_width, original_height = image.size
            ratio = min(max_width / original_width, max_height / original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)

            # Изменение размера изображения
            resized_image = image.resize((new_width, new_height), Image.LANCZOS)

            image_io = BytesIO()
            resized_image.save(image_io, format='WEBP', quality=85)

            # Сохранение обработанного изображения, изменение имени файла на .webp
            self.photo.save(f"{self.photo.name.rsplit('.', 1)[0]}.webp", ContentFile(image_io.getvalue()), save=False)

        super().save(*args, **kwargs)


class ProductSize(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_sizes',
                                verbose_name=_('Продукт'))
    size = models.ForeignKey(Size, on_delete=models.CASCADE, related_name='product_sizes', verbose_name=_('Размер'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена со скидкой'),
                                           blank=True, null=True)
    bonus_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Цена бонусами'))

    class Meta:
        verbose_name = "Цена продукта по размеру"
        verbose_name_plural = "Цены продуктов по размерам"

    def get_price(self):
        return self.discounted_price if self.discounted_price else self.price

    def __str__(self):
        return f"{self.product.name} - {self.size.name} - {self.get_price()}"



class Topping(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)

    class Meta:
        verbose_name = "Добавка"
        verbose_name_plural = "Добавки"

    def __str__(self):
        return self.name


class Set(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_('Категория'), related_name='sets')
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    description = models.TextField(verbose_name=_('Описание'), blank=True, null=True)
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)
    products = models.ManyToManyField(ProductSize, related_name='sets', verbose_name=_('Продукты'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    bonus_price = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name=_('Цена бонусами'))
    bonuses = models.BooleanField(default=False, verbose_name=_('Можно оптатить бонусами'))
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена со скидкой'),
                                           blank=True, null=True)

    class Meta:
        verbose_name = "Сет"
        verbose_name_plural = "Сеты"

    def __str__(self):
        return self.name

    def get_price(self):
        return self.discounted_price if self.discounted_price else self.price


class Ingredient(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Название'))
    photo = models.ImageField(upload_to='topping_photos/', verbose_name=_('Фото'), blank=True, null=True)
    possibly_remove = models.BooleanField(default=False, verbose_name=_('Возможность удаления'))

    class Meta:
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты"

    def __str__(self):
        return self.name
