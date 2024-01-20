from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Flashcard(models.Model):
    difficulty_choices = (("E", "Easy"), ("M", "Medium"), ("H", "Hard"))
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    answer = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    difficulty = models.CharField(max_length=1, choices=difficulty_choices)

    def __str__(self):
        return self.question
