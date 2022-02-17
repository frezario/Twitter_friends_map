'''
    A module which builds a world map with marks of location of friends of a certain percon.
'''
import random
import json
from functools import lru_cache
import folium
from geopy.geocoders import Nominatim, ArcGIS


arcgis = ArcGIS(timeout=10)
nominatim = Nominatim(timeout=10, user_agent="notme")
geocoders = [arcgis, nominatim]


@lru_cache(maxsize=None)
def get_location_by_address(address: str):
    """
    Returns a tuple of latitude and longitude of an address, given as a string.
    Args:
        address: a string that represents an adress.
    >>> get_location_by_address('Washington')
    (38.890370000000075, -77.03195999999997, 'Washington, District of Columbia')
    """
    i = 0
    try:
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude, location.address
        i += 1
        location = geocoders[i].geocode(address)
        if location is not None:
            return location.latitude, location.longitude, location.address
    except AttributeError:
        return None


def get_data(path_to_file:str) -> list:
    '''
    Returns a list of tuples in format '(nickname, location)'
    Args:
        path_to_file (str, optional): a path to json file with info
        about user's friends. Defaults to 'info.json'.
    '''
    with open(path_to_file, mode='r', encoding='utf-8') as file:
        data = json.load(file)
    result = [(user['screen_name'], user['location']) for user in data['users']]
    return result


def build_map(path_to_file:str = 'templates/info.json', path_to_map:str = 'templates/map.html'):
    """
    Builds a map using a folium lib and saves it.
    Returns None.
    Args:
        path (str): a path to sav a map.
        lat (float): the latitude chosen.
        lon (float): the longitude chosen.
    """
    data = get_data(path_to_file)
    world_map = folium.Map(location=[0, 0], zoom_start=5)
    html = """
Nickname:<br>
{}<br>
Place:<br>
{}
"""
    colors = [ 'red', 'blue', 'gray', 'darkred', 'lightred', 'orange', 'beige',
            'green', 'darkgreen', 'lightgreen', 'darkblue', 'lightblue', 'purple',
            'darkpurple', 'pink', 'cadetblue', 'lightgray', 'black']
    feature_group = folium.FeatureGroup('Friends')
    for item in data:
        try:
            lat, lon, location = get_location_by_address(item[1])
        except (TypeError, AttributeError):
            continue
        iframe = folium.IFrame(html=html.format(
            item[0], location), width=300, height=100)
        feature_group.add_child(folium.Marker(location = [lat, lon],
                                popup=folium.Popup(iframe),
                                icon=folium.Icon(color=random.choice(colors))))
        world_map.add_child(feature_group)
    world_map.save(path_to_map)
