from django.db import models
from django.contrib.auth.models import User 

class YEntity (models.Model):
    '''
    An Entity represents a "thing" in the physical world. This is the body of 
    a yank. It posesses a name, and a location. 
    '''
    name = models.CharField(max_length="96")

    # Location is represented in terms of latitude and longitude
    lat  = models.FloatField(null=False)
    lng  = models.FloatField(null=False)

class YNote (models.Model):
    '''
    A Note is a user's post which lies on top of an entity. The user searches 
    for an entity nearby. If such an entity is found, the user writes a note 
    tied to that entity. The entity and the user's note together represent a 
    "yank".

    The user can also see the body of collected notes relating to said entity by 
    virtue of the fact that the entity is now part of the user's collection.
    '''
    owner   = models.ForeignKey(User)
    entity  = models.ForeignKey(YEntity)
    content = models.CharField(max_length=140)

    class Meta:
        # ensure the user only posesses one note per entity at any given time
        unique_together = (('owner', 'entity'))
