from django.views.generic import View
from django.http import HttpResponse

class CSRFToken(View):
    '''
    Rotate the CSRF token -- that is, generate a new one
    '''
    def get(self, request):
        return HttpResponse('token here')

class Authenticate(View):
    '''
    Authenticate a user and/or log that user into the service
    '''
    
    # POST logs a user in
    def post(self, request):
        return HttpResponse('logged in')

    # DELETE logs us out
    def delete(self, request):
        return HttpResponse('user logged out')
