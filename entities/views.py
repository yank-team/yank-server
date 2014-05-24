from entities.models import Entity, EntityNote
from auth.models import YankUser

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.core.exceptions import ObjectDoesNotExist

from yank_server.helpers import screen_methods, screen_attrs, std_response
from entities.helpers import globe_distance_angle_threshold

import math, json


class EntityView(View):

    # Generate a list of entities
    @csrf_exempt
    def get(self, request):
        res = std_response(success=True, data=[
            {'id': x.id, 'name': x.name, 'lat': x.lat, 'lng': x.lng}
            for x in Entity.objects.all()
        ])
        return HttpResponse(res)

    def post(self, request):

        data = json.loads(request.read())

        try:
            user = YankUser.objects.get(api_key=data['apik'])

            # create and save the object
            entity = Entity.objects.create(
                name=data['name'],
                lat=data['lat'],
                lng=data['lng']
            )
            entity.save()

            res = std_response(success=true, data={'eid': entity.id})
            return HttpResponse(res)

        except ObjectDoesNotExist:
            res = std_response(success=False, msg='apik not supplied')
            return HttpResponse(res, 403)

@csrf_exempt
def list_entities_inside_radius(request, radius='5'):
    """
    find entities within a given radius (in miles, because lol cubits) and list 
    them in much the same way we list them above.

    This call essentially implements the whole "nearby entities" feature
    """
    # only GET allowed here
    if not screen_methods(request, ['POST']):
        return HttpResponse(status=405)

    data = json.loads(request.read())
    if not screen_attrs(data, ['apik', 'lat', 'lng']):
            return HttpResponse('improperly formatted request', status=400)

    # ensure this is a valid user
    try:
        user = YankUser.objects.get(api_key=data['apik'])
    except ObjectDoesNotExist:
        return HttpResponse('given API key is invalid', 403)
        
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


@csrf_exempt
def list_entity_notes(request, eid='1'):
    """
    list notes tied to a given entity 
    """
    if not screen_methods(request):
        return HttpResponse(status=405)

    # find entity from eid 
    try:
        entity = Entity.objects.get(id__exact=int(eid))
    except ObjectDoesNotExist:
        return HttpResponse('entity does not exist', 404)

    # list all notes associated with this entity
    notes = EntityNote.objects.filter(target=entity)

    ret = {
        'entity' : entity.id,
        'notes'  : [
            {
                'owner'   : x.id,
                'content' : x.content
            }
            for x in notes
        ]
    }

    return HttpResponse(json.dumps(ret))


@csrf_exempt
def post_entity_note(request):
    """ 
    create a new note from a given user for a given entity 
    """
    if not screen_methods(request, ['POST']):
        return HttpResponse(status=405)

    # create a new note 
    data = json.loads(request.read())

    if not screen_attrs(data, ['apik', 'eid', 'note']):
        return HttpResponse('improperly formatted request', status=400)

    # find user from APIK 
    try:
        user = YankUser.objects.get(api_key=data['apik'])
    except ObjectDoesNotExist:
        return HttpResponse('given API key is invalid', 403)

    # find entity from eid 
    try:
        entity = Entity.objects.get(id__exact=data['eid'])
    except ObjectDoesNotExist:
        return HttpResponse('entity does not exist', 404)

    # attempt to create note. Note: this should fail gracefully thanks to 
    # Django's default behavior
    note = EntityNote.objects.create(
        owner=user,
        target=entity,
        content=data['note']
        )
    note.save()

    return HttpResponse('success')
