from django.db import models

# Create your models here.
class Customer(models.Model):
    ID =  models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=30,null=False)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=15)
