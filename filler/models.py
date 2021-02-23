from django.db import models


# Create your models here.

class Department(models.Model):
    full_name = models.CharField(max_length=50, default=None)
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.full_name


class PolishDays(models.Model):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class PresenceSymbol(models.Model):
    symbol = models.CharField(max_length=5, null=False)
    full_name = models.CharField(max_length=30, null=False)

    def __str__(self):
        return self.full_name
