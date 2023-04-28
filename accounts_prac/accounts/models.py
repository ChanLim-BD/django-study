from django.db import models

class Account(models.Model):
    phone    = models.CharField(max_length = 45)
    password = models.CharField(max_length = 200)

