import googlemaps
import os

gmaps = googlemaps.Client(key=os.getenv("API_KEY"))


def get_lat_lng(address: str):
    """Get latitude and longitude of the given address

    Args:
        address (str): Address of the restaurant

    Returns:
        dict: key is 'lat' and 'lng'
    """
    response = gmaps.geocode(address)
    return response[0]['geometry']['location']
