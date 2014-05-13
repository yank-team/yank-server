from django.db import models
from auth.models import YankUser

class Entity(models.Model):
    """
    this is a thing in the physical world. It has a name and a location
    """
    name = models.CharField(max_length=98)
    lat  = models.FloatField()
    lng  = models.FloatField()

class EntityNote(models.Model):
    """
    this is a note written by a user about a single entity. One user can have 
    one note about one entity.
    """
    owner   = models.ForeignKey(YankUser)
    target  = models.ForeignKey(Entity)
    content = models.CharField(max_length=140)

    class Meta:
        unique_together = ('owner', 'target')
