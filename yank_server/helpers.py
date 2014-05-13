"""
yank_server.helpers
various helper functions to make development easier
"""
import math

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
    return {
        'success': success,
        'msg'    : msg,
        'data'   : data
    }

"""
implementation of the haversine functions -- we're using this to determine the
distance between two points on the globe. 

This isn't as accurate as it can be due to the elliptical nature of the actual
globe, but in this context we don't care at all.
"""
def haversin(theta):
    return (1-math.cos(theta))/2

def haversine(lats, lngs):
    a = haversin(lats[1]-lats[0])
    b = math.cos(lats[0])*math.cos(lats[1])
    c = haversin(lngs[1]-lngs[0])
    return a + b*c

def distance_between_globe_coords(point_a, point_b):
    earth_radius = 6378.1
    lats = (point_a[0], point_b[0])
    lngs = (point_b[1], point_b[1])
    return 2*earth_radius*math.asin(math.sqrt(haversine(lats, lngs)))
