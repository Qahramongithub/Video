from django.conf import settings
from django.db import models


class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username


class ApplicationType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Application(models.Model):
    video = models.FileField(upload_to='videos/')
    description = models.TextField()
    number = models.IntegerField()
    ApplicationType = models.ForeignKey('apps.ApplicationType', on_delete=models.CASCADE)

    def stream_url(self):
        return f"{settings.MEDIA_URL}{self.video}"

    def __str__(self):
        return str(self.number)


class Employee(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    ApplicationType = models.ForeignKey('apps.ApplicationType', on_delete=models.CASCADE)

    def __str__(self):
        return self.username
