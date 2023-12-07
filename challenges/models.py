from django.db import models
from django.forms.models import model_to_dict
import json


class Book(models.Model):
    title = models.CharField(max_length=256)
    author_full_name = models.CharField(max_length=256)
    isbn = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Laptop(models.Model):
    brand = models.CharField(
        max_length=20,
        choices=[('lenovo', 'Lenovo'), ('dell', 'Dell'), ('acer', 'Acer')]
    )
    production_date = models.DateField()
    ram_mb = models.PositiveIntegerField()
    hdd_mb = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    quantity = models.PositiveSmallIntegerField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def to_json(self):
        data = model_to_dict(self)
        data['created_at'] = self.created_at
        return json.dumps(data, default=str)


class Post(models.Model):
    class Status(models.TextChoices):
        PUBLISHED = "PUB", "опубликован"
        DRAFT = "DRAFT", "не опубликован"
        BANNED = "BANNED", "забанен"

    class Category(models.TextChoices):
        BOOKS = "BOOKS", "Книги"
        GAMES = "GAMES", "Игры"
        MUSIC = "MUSIC", "Музыка"

    title = models.CharField(max_length=256)
    text = models.CharField(max_length=2000)
    author = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10,
        choices=Status.choices
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )
    published_at = models.DateField()

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def to_json(self):
        data = model_to_dict(self)
        data['created_at'] = self.created_at
        return json.dumps(data, default=str)