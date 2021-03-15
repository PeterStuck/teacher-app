from django.db import models
from django.contrib.auth.models import User


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


class SparedTime(models.Model):
    time = models.BigIntegerField(null=False)
    teacher = models.OneToOneField(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.teacher.get_full_name() + str(self.time)


class LessonCategory(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Lesson category'
        verbose_name_plural = 'Lesson categories'

    def __str__(self):
        return self.name


class LessonTopic(models.Model):
    topic = models.CharField(max_length=300)
    is_individual = models.BooleanField()
    teacher = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    category = models.ForeignKey(LessonCategory, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.topic