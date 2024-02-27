from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Student(models.Model):
    name = models.CharField(max_length=30, )
    lastname = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.IntegerField()

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank="true")
    content = models.CharField(max_length=400)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'id': self.pk, 'author': self.author.username})
