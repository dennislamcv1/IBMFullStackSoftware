from django.db import models

# Test model
class Test(models.Model):
    name = models.CharField(max_length=30)