# fn = function 

# -----------------------------------------------------------------------------
# Dependencies 
# -----------------------------------------------------------------------------

import requests
import json
import time
import polyline

# -----------------------------------------------------------------------------
# fn1: 
# -----------------------------------------------------------------------------

def get_route(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat):
    
    """ 
    Measure the route distance betweeen two waypoints. 
    
    dependencies 
    ----------
    polyline 
    
    Parameters
    ----------
    pickup_lon, pickup_lat: cordinates of the starting waypoint 
    dropoff_lon, dropoff_lat: cordiantes of the ending waypoint 
    
    Returns
    -------
    dictionary for the modified OSRM output for the http call 

    """
    
    loc = "{},{};{},{}".format(pickup_lon, pickup_lat, dropoff_lon, dropoff_lat)
    #OSRM call, refer docs for additional arguments 
    url = "http://127.0.0.1:5000/route/v1/driving/"
    r = requests.get(url + loc) 
    if r.status_code!= 200:
        return {}
    
    res = r.json()   
    # decode all the points between waypoints using Googles polyline fn 
    routes = polyline.decode(res['routes'][0]['geometry'])
    start_point = [res['waypoints'][0]['location'][1], res['waypoints'][0]['location'][0]]
    end_point = [res['waypoints'][1]['location'][1], res['waypoints'][1]['location'][0]]
    distance = res['routes'][0]['distance']
    
    out = {'route':routes,
           'start_point':start_point,
           'end_point':end_point,
           'distance':distance
          }

    return out


