# ____ ____ ____ ____ # Libraries #
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options  # Import Options for headless mode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from shapely.geometry import Polygon
import time
import json
import re
import googlemaps
import math

# ____ ____ ____ ____ #

# ____ ____ ____ ____ # Classes #
class UGREALESTATE():
    class MAPS:

        def __init__(self, api_key):
            self.gmaps = googlemaps.Client(key=api_key)

        def path(self, mode, origin, destination):
            if mode == 'direct':
                lat1, lon1 = origin
                lat2, lon2 = destination

                radius = 6371  # Radius of the Earth in kilometers
                lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

                # Haversine formula
                dlat = lat2 - lat1
                dlon = lon2 - lon1
                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = radius * c

                return distance

            path = self.gmaps.directions(origin, destination, mode=mode)
            return path[0]['legs'][0]['distance']['value'] / 1000, path[0]['legs'][0]['duration']['value'] / 3600

    class NAPR:
        def __init__(self, cadastral_codes):
            self.cadastral_codes = cadastral_codes
        
        def cadastral_urls(self):
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options = options)
            driver.get("https://maps.gov.ge/") 
            search = driver.find_element(by="id", value="search_box")

            urls = []
            tempurl = "https://maps.gov.ge/map/portal#state/"
            for cadastral_code in self.cadastral_codes:
                try:  
                    search.clear()
                    search.send_keys(cadastral_code)
                    search.send_keys(Keys.RETURN)
                    WebDriverWait(driver, 20).until(lambda driver: tempurl not in driver.current_url)
                    tempurl = driver.current_url
                    
                    url = tempurl.replace('/map/portal#search/result', '') + '&lang=ka&res=shp'
                    urls.append(url)

                except Exception as e:
                    print("Error:", str(e))
                    driver.quit()

            driver.quit()
            return urls

        def cadastral_coordinates(self):
            urls = self.cadastral_urls()
            
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")
            driver = webdriver.Firefox(options = options)
            
            centroids = []
            for url in urls:
                driver.get(url)
                WebDriverWait(driver, 20).until(lambda driver: driver.find_element(By.TAG_NAME, 'body'))
                shape = json.loads(driver.find_element(By.TAG_NAME, 'body').text)['data'][0]['shape']
                
                coordinates = re.findall(r'(\d+\.\d+) (\d+\.\d+)', shape)
                
                coordinate_tuples = [(float(lat), float(lon)) for lon, lat in coordinates]
                polygon = Polygon(coordinate_tuples)
                centroid = polygon.centroid
                
                centroids.append((centroid.xy[0][0], centroid.xy[1][0]))
            
            driver.quit()
            return centroids

    def __init__(self, gmaps_api_key, cadastral_codes, destinations):
        origins = self.NAPR(cadastral_codes).cadastral_coordinates()
        maps = self.MAPS(gmaps_api_key)

        for origin in origins:
            print(f'origin: {origin}')
            for destination in destinations:
                for mode in ['walking', 'driving', 'transit']:
                    print(f"{mode}: distance = {maps.path(mode, origin, destination)[0]:.2f} km, duration = {maps.path(mode, origin, destination)[1]:.2f} hours, destination: {destination}")
                print(f'direct: distance = {maps.path("direct", origin, destination):.2f} km, destination: {destination}')
            print('\n')
# ____ ____ ____ ____ # 

REALESTATE(gmaps_api_key = 'AIzaSyDN5cj3erHNhv8GiQVAbxYx0C3q3XHJmms', cadastral_codes = ['01.12.11.043.008', '01.11.03.010.208', '01.17.08.063.041', '01.16.04.040.048'], destinations = [(41.679103935499974, 44.840062109473855)])