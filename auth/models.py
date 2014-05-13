from django.db import models

class YankUser(models.Model):
    username        = models.CharField(max_length=98)
    password_digest = models.CharField(max_length=128)
    api_key         = models.CharField(max_length=128, null=True)
