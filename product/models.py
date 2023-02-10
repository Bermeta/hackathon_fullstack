from django.contrib.auth import get_user_model
from django.db import models

from category.models import Category

User = get_user_model()
from ckeditor.fields import RichTextField


class Product(models.Model):
    STATUS_CHOICES = (
        ('in_stock', 'В наличии'),
        ('out_of_stock', 'Нет в наличии')
    )
    STATUS_CHOICES_SEX = (
        ('men', 'Мужской'),
        ('women', 'Женский'),
        ('unisex', 'Юнисекс')
    )
    STATUS_CHOICES_BRAND_NAME = (
        ('Nike', 'Nike'),
        ('adidas', 'adidas'),
        ('PUMA', 'PUMA'),
        ('Reebok', 'Reebok'),
        ('Timberland', 'Timberland'),
        ('YSL', 'YSL')
    )
    owner = models.ForeignKey(User, on_delete=models.RESTRICT, related_name='product')
    title = models.CharField(max_length=150)
    brand = models.CharField(choices=STATUS_CHOICES_BRAND_NAME, max_length=50)
    description = RichTextField()
    category = models.ForeignKey(Category, related_name='products', on_delete=models.RESTRICT)
    preview = models.ImageField(upload_to='images')
    image = models.ImageField(upload_to='images', blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.CharField(choices=STATUS_CHOICES, max_length=50)
    sex = models.CharField(choices=STATUS_CHOICES_SEX, max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

