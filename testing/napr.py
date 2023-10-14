# ____ ____ ____ ____ # Libaries #
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
# ____ ____ ____ ____ #

# ____ ____ ____ ____ # Classes #
class NAPR():
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
            
            print(shape)
            print(coordinate_tuples)
            print(centroid)
            centroids.append((centroid.xy[0][0], centroid.xy[1][0]))
        
        driver.quit()
        return centroids
        
        # return shapes

napr = NAPR(['01.12.11.043.008', '01.11.03.010.208', '01.17.08.063.041', '01.16.04.040.048'])
# print(napr.cadastral_coordinates())
napr.cadastral_coordinates()          