"""
implementation of the haversine functions -- we're using this to determine the
distance between two points on the globe. 

This isn't as accurate as it can be due to the elliptical nature of the actual
globe, but in this context we don't care at all.
"""

from math import radians, cos, sin, asin, sqrt

def earth_radius():
    return 6378.1

def haversine_dist(lng1, lat1, lng2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lng1, lat1, lng2, lat2 = map(radians, [lng1, lat1, lng2, lat2])

    # haversine formula
    dlng = lng2 - lng1
    dlat = lat2 - lat1
    a    = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c    = 2 * asin(sqrt(a))
    km   = 6367 * c
    return km
    
def globe_distance_angle_threshold(distance):
    """
    calculate an angle threshold (in radians) for a given distance from a given 
    point. 
    """
    return (1-cos(distance/earth_radius()))/2
