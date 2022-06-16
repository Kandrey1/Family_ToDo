from datetime import date
from django.db import models
from django.urls import reverse
from autoslug import AutoSlugField


class TodoList(models.Model):
    title = models.CharField(max_length=120)
    time_create = models.DateField(auto_now_add=True)   # дата создания
    time_deadline = models.DateField(default=date.today)
    check = models.BooleanField()
    user_id = models.IntegerField()

    class Meta:
        verbose_name = "Список дел"
        ordering = ["time_deadline"]

    def __str__(self):
        return self.title


class ListProducts(models.Model):
    name_list = models.CharField(max_length=100)
    time_create = models.DateField(auto_now_add=True)
    slug = AutoSlugField(populate_from='name_list') # некорректно работает с кириллицей
    user_id = models.IntegerField()

    def get_absolute_url(self):
        return reverse('products', args=[str(self.slug)])

    class Meta:
        verbose_name = "Списки покупок"
        ordering = ["id"]

    def __str__(self):
        return self.name_list


class Products(models.Model):
    buy = models.CharField(max_length=150)
    time_create = models.DateField(auto_now_add=True)
    check = models.BooleanField()
    list_name = models.CharField(max_length=150)

    class Meta:
        verbose_name = "Покупки"
        ordering = ["id"]

    def __str__(self):
        return self.buy

    @staticmethod
    def get_path_redirect(slug):
        return reverse('products', args=[str(slug)])
