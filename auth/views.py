
from django.http import HttpResponse

from django.views.generic import View

from django.core.exceptions import ObjectDoesNotExist
from auth.models import YankUser
from base64 import b64encode
from yank_server.helpers import std_response, CSRFExemptMixin

import os, json, bcrypt

class AuthUserView(CSRFExemptMixin, View):

    def get(self, request):
        """
        List all users on the database -- NOTE: this is a debug 
        method, and should be walled-off in a production server
        """
        return HttpResponse(std_response(data=[
            {'username': x.username, 'apik': x.api_key}
            for x in YankUser.objects.all()
        ]))

        def post(self, request):
            """ create a new user if his/her username doesn't exist already """

            data = json.loads(request.read())

            try:
                user = YankUser.objects.get(username__exact=data['username'])
                return HttpResponse(
                    std_response(status=False, msg='user exists'), status=403)
            except ObjectDoesNotExist:
                # TODO: Log the user query somewhere
                pass

            enc_passwd = data['password'].encode('utf-8')
            user = YankUser.objects.create(
                username=data['username'],
                password_digest=bcrypt.hashpw(enc_passwd, bcrypt.gensalt()),
                api_key=None
            )
            user.save()
            return HttpResponse(std_response(success=True, msg='success'))

class AuthLoginView(CSRFExemptMixin, View):
    # TODO: see if we can use GET to verify an APIK

    def post(self, request):
        """ authenticate a user """
        data = json.loads(request.read())

        try:
            user = YankUser.objects.get(username__exact=data['username'])
        except ObjectDoesNotExist:
            # User not found -- quit
            res = std_response(success=False, msg='user not found')
            return HttpResponse(res, status=404)

        # check password hash
        enc_passwd = data['password'].encode('utf-8')
        enc_digest = user.password_digest.encode('utf-8')

        if bcrypt.hashpw(enc_passwd, enc_digest) != enc_digest:
            # fail on invalid password
            res = std_response(success=False, msg='bad password') 
            return HttpResponse(res, status=403)

        # generate apik -- check/refresh it until it doesn't exist
        try:
            # This should virtually always terminate in the first loop. We just want
            # to be able to handle the crazy corner-case of more than one apik 
            # conflict elegantly
            while True:
                # generate random bytes
                rbytes = os.urandom(64)

                # encode this as a string
                apik     = b64encode(rbytes).encode('utf-8')
                apikuser = YankUser.objects.get(api_key__exact=apik)

                # keep pyflakes happy, and also ensure we don't hold onto the 
                # hypothetically retrieved user for more than one step
                apikuser = None
        except ObjectDoesNotExist:
            # Save the key
            user.api_key = apik
            user.save()
            ret['apik'] = apik

            # Serialize return data as a standard response
            res = std_response(success=True, data=ret)
            return HttpResponse(res)

    def delete(self, request):
        pass

@csrf_exempt
def logout(request):
    if request.method != 'DELETE':
        return HttpResponse(status=405)

    data = json.loads(request.read())

    # Ensure the APIK has been given
    # TODO: implement this as a decorator
    if 'apik' not in data:
        return HttpResponse(status=400)
    apik = data['apik']

    # find user associated with the APIK
    try:
        user = YankUser.objects.get(api_key__exact=apik)
    except ObjectDoesNotExist:
        return HttpResponse(status=403)

    # remove the user's APIK thereby logging that user out
    user.api_key = None
    user.save()

    ret = std_response(success=True, msg='success')
    return HttpResponse(ret)

@csrf_exempt
def verify_apik(request):
    """
    verifies a given API key from the client -- allows the client to check a 
    stored APIK against its online counterpart for consistency.
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    data = json.loads(request.read())

    try:
        user = YankUser.get(id__exact=data['uid'])
    except ObjectDoesNotExist as e:
        res = std_response(msg='valid apik', success=True, data=None)
        return HttpResponse(res)

    # verify that the APIK is not taken -- if it is, just boot the user and
    # keep on truckin'
    if user.api_key == None:
        res = std_response(msg='no apik', success=False, data=None)
        return HttpResponse(res, status=404)

    elif user.api_key == data['apik']:
        res = std_response(msg='valid apik', success=True, data=None)
        return HttpResponse(res)

    # boot user
    user.api_key = None
    user.save()

    # keep on truckin'
    res = std_response(msg='invalid apik', success=False, data=None)
    return HttpResponse(res, status=403)
