from entities.models import Entity, EntityNote
from auth.models import YankUser

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

from yank_server.helpers import screen_methods, screen_attrs, std_response
from entities.helpers import globe_distance_angle_threshold

import math, json

@csrf_exempt
class EntityView(View):
    """
    Either list or post entities to the DB
    """

    def get(self, request):

        # Serialize an entity list from the DB and return it
        res = std_response(success=True, data=[
            {'id': x.id, 'name': x.name, 'lat': x.lat, 'lng': x.lng}
            for x in Entity.objects.all()
        ])
        return HttpResponse(res)

    def post(self, request):

        data = json.loads(request.read())

        try:
            user = YankUser.objects.get(api_key=data['apik'])
        except ObjectDoesNotExist:
            res = std_response(success=False, msg='apik not supplied')
            return HttpResponse(res, 403)

        # create and save the object
        entity = Entity.objects.create(
            name=data['name'],
            lat=data['lat'],
            lng=data['lng']
        )
        entity.save()

        res = std_response(success=true, data={'eid': entity.id})
        return HttpResponse(res)

@csrf_exempt
class EntityNoteView(View):

    def get(self, request):
        """
        get a list of notes
        """
        data = json.loads(request.read())

        # serialize data from DB and return it
        res = std_response(success=True, data=[
            {'id': x.id, 'owner': x.owner, 'content': x.content}
            for x in EntityNote.objects.filter(target=entity)
        ])
        return HttpResponse(res)

    def post(self, request):
        """
        post a new note
        """
        try:
            user = YankUser.objects.get(api_key=data['apik'])
        except ObjectDoesNotExist:
            res = std_response(success=False, msg='apik invalid')
            return HttpResponse(res, 403)

        # attempt to create note. Note: this should fail gracefully thanks to 
        # Django's default behavior
        try:
            note = EntityNote.objects.create(
                owner=user,
                target=Entity.objects.get(id__exact=data['eid']),
                content=data['content']
                )
            note.save()
        except ObjectDoesNotExist:
            res = std_response(success=False, msg='eid invalid')
            return HttpResponse(res, status=404)

        res = std_response(success=True, data={'nid': note.id})
        return HttpResponse(res)

@csrf_exempt
class EntityRadiusView(View):

    """
    find entities within a given radius (in miles, because lol cubits) and list 
    them in much the same way we list them above.

    This call essentially implements the whole "nearby entities" feature
    """

    def get(self, request):
        data = json.loads(request.read())

        # ensure this is a valid user
        try:
            user = YankUser.objects.get(api_key=data['apik'])
        except ObjectDoesNotExist:
            return HttpResponse('given API key is invalid', 403)

"""
@csrf_exempt
def list_entities_inside_radius(request, radius='5'):

    # Calculate acceptable variation in degrees from the haversine formula
    radius = int(radius) 
    threshold = math.degrees(globe_distance_angle_threshold(radius))

    # now we let Django construct a SQL statement that will filter out the 
    # relevant data for us.
    entities = Entity.objects.filter(
            lat__lte=data['lat']+threshold,
            lng__lte=data['lng']+threshold 
        ).filter(
            lat__gte=data['lat']-threshold,
            lng__gte=data['lng']-threshold 
        )

    # The cool part of this is that these filters can catch the whole thing in
    # one SQL statement thanks to Django's lazy-loading ORM. Booyah!

    # Now we serialize and spit it all out
    # TODO: move these list comprehensions out into "serializers.py" to make 
    # everything more "DRY"
    ret      = [
        {'id': x.id, 'name': x.name, 'lat': x.lat, 'lng': x.lng}
        for x in entities
    ]
    return HttpResponse(json.dumps(ret))
"""
