from django.db import models


class Genre(models.Model):
    name = models.CharField(max_length=100)


class Author(models.Model):
    name = models.CharField(max_length=100)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    publication_date = models.DateField()
    stock_quantity = models.IntegerField()
