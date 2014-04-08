
from django.views.generic import View
from django.http import HttpResponse
from yank_entities.models import YEntity, YNote

import json

class EntityLocation(View):

    def post(self, request):
        return HttpResponse(request.body)

