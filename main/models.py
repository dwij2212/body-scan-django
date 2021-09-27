from django.db import models

# Create your models here.
class Customer(models.Model):
    height = models.IntegerField(default=150)
    image = models.ImageField(upload_to='images/')