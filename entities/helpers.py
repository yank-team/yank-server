import math

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
    """
    take two points as input. Output is the distance between them
    """
    earth_radius = 6378.1
    lats = (math.radians(point_a[0]), math.radians(point_b[0]))
    lngs = (math.radians(point_b[1]), math.radians(point_b[1]))
    return 2*earth_radius*math.asin(math.sqrt(haversine(lats, lngs)))

def globe_distance_angle_threshold(point, distance):
    """
    calculate an angle threshold (in radians) for a given distance from a given 
    point. 
    """
    earth_radius = 6378.1
    return haversin(distance/earth_radius)
