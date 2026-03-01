from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

# Модель категории
class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название категории')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Изображение')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE,
                               null=True, blank=True,
                               verbose_name='Категория', related_name='subcategories')

    def get_absolute_url(self):  # умная ссылка для переключения по категориям
        return reverse('category', kwargs={'slug': self.slug})

    # Метод для получения картинки категории
    def get_image(self):
        if self.image:
            return self.image.url
        else:
            return 'https://i.ytimg.com/vi/95wlHmvAz80/0.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Категория: pk={self.pk}, title={self.title}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


#  Модель продукта
class Product(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название продукта')
    price = models.FloatField(verbose_name='Цена')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    quantity = models.IntegerField(default=0, verbose_name='Количество на складе')
    description = models.TextField(default='Здесь скоро будит описание', verbose_name='Описание товара')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30, verbose_name='Размер в мм')
    color = models.CharField(default='Серебро', max_length=30, verbose_name='Цвет/Материал')

    def get_absolute_url(self):  # умная ссылка
        return reverse('product_detail', kwargs={'slug': self.slug})

    # Метод для получение 1 фото
    def get_first_photo(self):
        if self.images:
            try:
                return self.images.first().image.url
            except:
                return 'https://i.ytimg.com/vi/95wlHmvAz80/0.jpg'
        else:
            return 'https://i.ytimg.com/vi/95wlHmvAz80/0.jpg'

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'Товар: pk={self.pk}, title={self.title}, price={self.price}'

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


#  Моделька Галерея картинок
class Gallery(models.Model):
    image = models.ImageField(upload_to='products/', verbose_name='Изображение')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    class Meta:
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

# Моделька для коментариев
class Review(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата комента')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
