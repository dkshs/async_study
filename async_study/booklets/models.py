from django.contrib.auth.models import User
from django.db import models


class Booklet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to="booklets")

    def __str__(self):
        return self.title


class BookletView(models.Model):
    ip = models.GenericIPAddressField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    booklet = models.ForeignKey(Booklet, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.booklet.title} - {self.ip}"

    class Meta:
        verbose_name = "Booklet View"
        verbose_name_plural = "Booklet Views"
