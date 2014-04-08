
from django.views.generic import View
from django.http import HttpResponse
from yank_entities.models import YEntity, YNote

import json

class EntityLocation(View):
    '''
    Input: POST data containing the device's location (in lat/lng) and a given 
        radius underneath a set maximum

    Output: A list of entities within the given radius 
    '''
    def post(self, request):
        # Get post data
        arg_lat    = request.POST['lat']
        arg_lng    = request.POST['lng']
        arg_radius = request.POST['radius']

        # TODO: Assert max radius

        # Filter relevant entities
        qset_entity = YEntity.objects.filter(
            lat__gte=arg_lat-arg_radius
        )
        .filter(
            lat__lte=arg_lat+arg_radius
        )

        # TODO: test and serialize
        return HttpResponse('[]')

