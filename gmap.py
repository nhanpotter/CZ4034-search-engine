import os
import random

import googlemaps


def get_lat_lng(address: str):
    """Get latitude and longitude of the given address

    Args:
        address (str): Address of the restaurant

    Returns:
        dict: key is 'lat' and 'lng'
    """
    key = os.getenv("API_KEY")
    if not os.getenv("API_KEY_BACKUP"):
        if random.choice([True, False]):
            key = os.getenv("API_KEY_BACKUP")

    gmaps = googlemaps.Client(key=key)
    try:
        response = gmaps.geocode(address)
    except:
        # In case address too long
        response = gmaps.geocode(address[len(address) // 2:])

    print(response)
    return response[0]['geometry']['location']
