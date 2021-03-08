from django.db import models

from base.models import Department
from django.contrib.auth.models import User


class RevalidationStudent(models.Model):
    name = models.CharField(max_length=50)
    department = models.ForeignKey(to=Department, on_delete=models.DO_NOTHING)
    teacher = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.name


class IndividualLessonPaymentType(models.Model):
    type = models.CharField(max_length=75)

    def __str__(self):
        return self.type
