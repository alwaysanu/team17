
from django.core.validators import validate_comma_separated_integer_list
from django.contrib.auth.models import AbstractUser
from django.db import models


class Activity(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, blank=True)
    category = models.CharField(max_length=20)
    link = models.CharField(max_length=500, blank=True)
    participants = models.IntegerField(default=0)
    description = models.TextField(max_length=2000, blank=True)
    thumb = models.CharField(max_length=500, blank=True)
    key = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class BoredUser(AbstractUser):
    REQUIRED_FIELDS = ('email',)
    email = models.EmailField(max_length=50, unique=True)
    last_activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING,
                    null=True, blank=True, related_name='last_activity')
    category_weights = models.CharField(max_length=500,validators=[validate_comma_separated_integer_list],
                    blank=True)
    saved_activities = models.ManyToManyField(Activity, related_name='saved_activities', blank=True)


    def __str__(self):
        return self.email
