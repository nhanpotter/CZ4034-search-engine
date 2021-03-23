from tinydb import TinyDB, Query

from constants import RESTAURANT_DB_PATH
from gmap import get_lat_lng


class RestaurantUtils:
    def __init__(self):
        self.db = TinyDB(RESTAURANT_DB_PATH)

    def list(self):
        """Get the list of all restaurants.
        """
        return self.db.all()

    def _get_last_id(self):
        """Get last restaurant id.
        """
        last_id = -1
        for restaurant in self.db.all():
            if restaurant.id > last_id:
                last_id = restaurant.id

        return last_id

    def restaurant_exists(self, name, location):
        """Check if restaurant already exists in the db.

        Returns:
            bool: True if restaurant already exists. Otherwise, False
        """
        Restaurant = Query()
        result = self.db.search(
            (Restaurant.name == name) & (Restaurant.location == location))
        return len(result) != 0

    def insert(self, name, location):
        res_id = self._get_last_id() + 1
        loc = get_lat_lng(location)
        restaurant = {
            'id': res_id,
            'name': name,
            'location': location,
            'lat': loc['lat'],
            'lng': loc['lng']
        }
        self.db.insert(restaurant)

        return restaurant
