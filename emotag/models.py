from django.db import models

# Create your models here.

class Emotag(models.Model):
  firstname = models.CharField(max_length=255)
  lastname = models.CharField(max_length=255)


class testimonial(models.Model):
    name=models.CharField(max_length=20)
    comment=models.TextField()
    img = models.ImageField(upload_to = "images/")