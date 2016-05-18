import time
import urllib2
import json, requests
from pprint import pprint
from bs4 import BeautifulSoup
from neopixel import *
import ipgetter

## WEBSCRAPING SECTION ##
## Hourly weather thru accuweather webpage
weather_url = "http://www.accuweather.com/en/at/salzburg/30760/hourly-weather-forecast/30760"
# weather_url = "http://www.accuweather.com/en/gb/london/ec4a-2/hourly-weather-forecast/328328"
# weather_url = "http://www.accuweather.com/en/au/sydney/22889/hourly-weather-forecast/22889"
# weather_url = "http://www.accuweather.com/en/de/berlin/10178/hourly-weather-forecast/178087"
page = urllib2.urlopen(weather_url)
weather_soup = BeautifulSoup(page, 'html.parser')
print weather_soup.title
table = weather_soup.find('table')
hours = []
for row in table.findAll('tr')[7:8]:
    col = row.findAll('td')
    hours.append(col[0].string)
    hours.append(col[1].string)
    hours.append(col[2].string)
    hours.append(col[3].string)
    hours.append(col[4].string)
    hours.append(col[5].string)
    hours.append(col[6].string)
    hours.append(col[7].string)
## Rain section of table
import re
rain = []
for row in table.findAll('tr')[8:9]:
    for col in row.find_all('td'):
        for element in col:
            e = element.string
            string = e.replace(u'\xa0', u' ')
            string = re.sub('\%', '', string)
            if string != (u' '):
                value = int(string)
                rain.append(value)
# weather_dict = dict(zip(hours, rain))
# print weather_dict
## End WEBSCRAPING SECTION ##

## WEATHER API SECTION ##
## from Accuweather
myip = ipgetter.myip()
locator_api = "http://dataservice.accuweather.com/locations/v1/cities/ipaddress"
wapi_key = "a8Rw8CQWQCN2KabjmJRnbkG7UdldAlIX"
wapi_hourly = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"

## Get data
myloc_url = locator_api + "?apikey=" + wapi_key + "&q=" + myip
myloc_json = requests.get(myloc_url).json()
myloc_name = myloc_json["EnglishName"]
myloc_key = myloc_json["Key"]
weather_hourly_url = wapi_hourly + myloc_key + "?apikey=" + wapi_key
weather_hourly_json = requests.get(weather_hourly_url).json()
# print weather_hourly_json[1]
print "Location: " + myloc_name
precipitation = []
for i in weather_hourly_json:
    precipitation.append(i["PrecipitationProbability"])
print
print "+" * 50
print
       
## NEOPIXEL INTERACTION ##
# LED strip configuration:
LED_COUNT = 8 # Number of LED pixels.
LED_PIN = 18 # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
LED_DMA = 5 # DMA channel to use for generating signal (try 5)
LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)

def colorWipe(strip, color, wait_ms=50):
#  """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

#Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
# Intialize the library (must be called once before other functions).
strip.begin()
strip.setBrightness(20)

# print strip.numPixels()
# print strip.getPixelColor(1)
# colorWipe(strip, Color(0, 0, 255)) #Green Wipe
# strip.setPixelColorRGB(0, 255, 0, 0) #set to green

count = 0
if count < 8:
    for i in precipitation:
        if i < 30:
            print "Low chance of rain"
            strip.setPixelColorRGB(count, 255, 0, 0) #GRB
            strip.show()
        elif i < 60:
            print "Looks a bit dodgy out there"
            strip.setPixelColorRGB(count, 191, 255, 0)
            strip.show()
        else:
            print "Grab your brollie!"
            strip.setPixelColorRGB(count, 0, 255, 0)
            strip.show()
        count += 1
        time.sleep(0.5)

# strip.show()
## END NEOPIXEL INTERACTION ##

