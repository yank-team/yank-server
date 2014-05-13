
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from auth.models import YankUser
from base64 import b64encode

import os, json, bcrypt


@csrf_exempt
def list_user(request):
    """
    list users, or create a new user if one doesn't exist already
    """
    if request.method == 'GET':
        # List users -- this is a DEBUG method. We need to get rid of it after
        # we have a working product
        users = YankUser.objects.all()
        ret = [
            {
                'username': x.username,
                'password_digest': x.password_digest,
                'apik'    : x.api_key
            }
            for x in users
        ]
        return HttpResponse(json.dumps(ret))

    elif request.method != 'POST':
        return HttpResponse('method not allowed', status=405)

    data = json.loads(request.read())

    if 'username' not in data or 'password' not in data:
        return HttpResponse('bad request', status=400)

    # Check for user
    try:
        user = YankUser.objects.get(username__exact=data['username'])
    except ObjectDoesNotExist:

        # Create a new user
        enc_passwd = data['password'].encode('utf-8')

        user = YankUser.objects.create(
            username=data['username'],
            password_digest=bcrypt.hashpw(enc_passwd, bcrypt.gensalt()),
            api_key=None
            )
        user.save()
        return HttpResponse('success')

    # User exists -- abort
    return HttpResponse('user exists', status=403)


@csrf_exempt
def authenticate(request):
    """
    authenticate a user into the service
    """
    if request.method != 'POST':
        return HttpResponse(status=405)

    # read body of the request as json
    data = json.loads(request.read())
    ret  = {}

    # Ensure we've been passed the correct data
    if 'username' not in data or 'password' not in data:
        return HttpResponse(status=400)

    # authenticate
    try:
        user = YankUser.objects.get(username__exact=data['username'])

        # check password hash
        enc_passwd = data['password'].encode('utf-8')
        enc_digest = user.password_digest.encode('utf-8')

        if bcrypt.hashpw(enc_passwd, enc_digest) != enc_digest:
            # fail on invalid password
            return HttpResponse('bad password', status=403)

    except ObjectDoesNotExist:
        return HttpResponse('user not found', status=404)

    # Are we logged in already?
    if user.api_key is not None:
        # If so, kill the request
        return HttpResponse('user logged in already', status=403)
    
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
    except ObjectDoesNotExist:
        # Save the key
        user.api_key = apik
        user.save()
        ret['apik'] = apik

        return HttpResponse(json.dumps(ret))

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

    return HttpResponse('success')
