from django.db import models
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class To_fro(models.Model):
	fro=models.DateField()
	to=models.DateField(default=datetime.date.today)


class ulimit(models.Model):
	percentage=models.IntegerField(
        default=75,validators=[MaxValueValidator(100), MinValueValidator(1)]
     )