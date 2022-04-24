# fn = function 

# -----------------------------------------------------------------------------
# Dependencies 
# -----------------------------------------------------------------------------

import requests
import json
import time
import folium
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


# -----------------------------------------------------------------------------
# fn2: 
# -----------------------------------------------------------------------------


def get_map(route):
    
    """ 
    Visualize a selected route leg 
    
    dependencies 
    ----------
    folium 
    
    Parameters
    ----------
    route: modified dictionary output of the get route fn 
    
    Returns
    -------
    folium map showing the route section 
    
    """
    
    m = folium.Map(location=[(route['start_point'][0] + route['end_point'][0])/2, 
                             (route['start_point'][1] + route['end_point'][1])/2], 
                   zoom_start=13)

    folium.PolyLine(
        route['route'],
        weight=8,
        color='blue',
        opacity=0.6
    ).add_to(m)

    folium.Marker(
        location=route['start_point'],
        icon=folium.Icon(icon='play', color='green')
    ).add_to(m)

    folium.Marker(
        location=route['end_point'],
        icon=folium.Icon(icon='stop', color='red')
    ).add_to(m)

    return m

