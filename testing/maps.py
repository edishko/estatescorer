# Import libraries
import googlemaps
import math

# Define a class for working with Google Maps
class MAPS:

    def __init__(self, api_key, origin, destination):
        self.gmaps = googlemaps.Client(key=api_key)
        self.origin = origin
        self.destination = destination

    def path(self, mode):
        if mode == 'direct':
            lat1, lon1 = self.origin
            lat2, lon2 = self.destination

            radius = 6371  # Radius of the Earth in kilometers
            lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

            # Haversine formula
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
            c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
            distance = radius * c

            return distance

        path = self.gmaps.directions(self.origin, self.destination, mode=mode)
        return path[0]['legs'][0]['distance']['value'] / 1000, path[0]['legs'][0]['duration']['value'] / 3600

# Initialize the MAPS class
maps = MAPS(api_key='AIzaSyDN5cj3erHNhv8GiQVAbxYx0C3q3XHJmms', origin=(41.8252662618482, 44.76650705237628), destination=(41.679103935499974, 44.840062109473855))

# Print the results
print(f"Walking: Distance = {maps.path('walking')[0]:.2f} km, Duration = {maps.path('walking')[1]:.2f} hours")
print(f"Driving: Distance = {maps.path('driving')[0]:.2f} km, Duration = {maps.path('driving')[1]:.2f} hours")
print(f"Transit: Distance = {maps.path('transit')[0]:.2f} km, Duration = {maps.path('transit')[1]:.2f} hours")
print(f"Straight-Line Distance = {maps.path('direct'):.2f} km")
