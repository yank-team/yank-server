"""
yank_server.helpers
various helper functions to make development easier
"""
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

def screen_methods(request, methods=['GET']):
    """
    determines whether a given request conforms to a whitelist of allowed 
    HTTP methods
    """
    if request.method not in methods:
        return False
    return True

def screen_attrs(data, attrs=[]):
    """
    determines whether given data conforms to a set of given attributes
    extra attributes are ignored 

    TODO: screen these out as well
    """
    for item in attrs:
        if item not in data:
            return False
    return True
    
def std_response(msg="", success=True, data=None):
    """
    constructs a standard response dictionary to be translated into JSON and
    given back in an HTTP response
    """
    return json.dumps({
        'success': success,
        'msg'    : msg,
        'data'   : data
    })

class CSRFExemptMixin(object):
    """
    Exempt a class-based view from CSRF
    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)
