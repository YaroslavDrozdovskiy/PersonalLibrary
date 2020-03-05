from django.db import models
from django.utils import timezone

# Create your models here.


class Author(models.Model):
    full_name = models.TextField()
    birth_year = models.SmallIntegerField()
    country = models.CharField(max_length=2)

    def __str__(self):
        return self.full_name


class Friend(models.Model):
    name = models.CharField('Имя друга', max_length=30, unique=True)
    borrow_date = models.DateField(
        'Дата с момента одолжения',  default=timezone.now())

    def __str__(self):
        return self.name


class Book(models.Model):
    ISBN = models.CharField(max_length=13)
    title = models.CharField(max_length=50, unique=True,)
    description = models.TextField()
    year_release = models.SmallIntegerField()
    copy_count = models.SmallIntegerField(default=1)
    price = models.DecimalField(default=None, max_digits=19, decimal_places=2)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='author_books')
    friend = models.ForeignKey(Friend, on_delete=models.SET_NULL,
                               related_name='friend_books', null=True, blank=True)

    def __str__(self):
        return self.title