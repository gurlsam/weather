import sys
import time
# import atexit
# import logging
# import subprocess
import urllib2
import json, requests
from pprint import pprint
from bs4 import BeautifulSoup
from neopixel import *
import ipgetter
import RPi.GPIO as GPIO
import Adafruit_MPR121.MPR121 as MPR121
# import uinput


salzburg = "30760"
key_mapping = {
               0: "274087",     #Lisbon
               1: "307297",     #Barcelona
               2: "623",        #Paris
               3: "178087",     #Berlin
               4: "30760",      #Salzburg
                }

## Function for capacitive touch sensor
def cap_sensor():
    # create MPR121 instance
    cap = MPR121.MPR121()
    # initialise comms using i2c bus
    # default address is 0x5a
    if not cap.begin():
        print ("Error initializing MPR121. Check wiring!")
        sys.exit()
    print ("Capacitive Sensor. Press CTRL-C to end")
    last_touched = cap.touched()
    while True:
        current_touched = cap.touched()
        for pin, key in key_mapping.iteritems():
            pin_bit = 1 << pin
            if current_touched & pin_bit and not last_touched & pin_bit:
                print ('{0} touched!'.format(pin))
#                 logging.debug('Input {0} touched'.format(pin))
                print pin,key
                weather_api(key)
            if not current_touched & pin_bit and last_touched & pin_bit:
                print ('{0} released!'.format(pin))
        last_touched = current_touched
        time.sleep(0.1)
    

## Function to initiate button ##
def button(cities):
    GPIO.setmode(GPIO.BCM)
#     GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(23, GPIO.IN)
    print 'Press the button to cycle thru cities. Use CTRL-C to exit'
    prev_input = 1
    while True:
        input = GPIO.input(23)
        for i in cities:
            if (prev_input and not input):
                print ('Button pressed')
                print i
                time.sleep(0.05)
        prev_input = input

## Function to scrape hourly weather ##
def scrape_weather(weather_url):
    page = urllib2.urlopen(weather_url)
    weather_soup = BeautifulSoup(page, 'html.parser')
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
    weather_dict = dict(zip(hours, rain))
    return weather_dict

## Function to get Weather via API ##
def weather_api(location):
#     myip = ipgetter.myip()
#     locator_api = "http://dataservice.accuweather.com/locations/v1/cities/ipaddress"
    wapi_key = "a8Rw8CQWQCN2KabjmJRnbkG7UdldAlIX"
    wapi_hourly = "http://dataservice.accuweather.com/forecasts/v1/hourly/12hour/"
    
    ## Get data
#     myloc_url = locator_api + "?apikey=" + wapi_key + "&q=" + myip
#     myloc_json = requests.get(myloc_url).json()
#     myloc_name = myloc_json["EnglishName"]
#     myloc_key = myloc_json["Key"]
#     weather_hourly_url = wapi_hourly + myloc_key + "?apikey=" + wapi_key
    weather_hourly_url = wapi_hourly + location + "?apikey=" + wapi_key
    # weather_hourly_url = wapi_hourly + "30760" + "?apikey=" + wapi_key #Salzburg
    # weather_hourly_url = wapi_hourly + "30332" + "?apikey=" + wapi_key #Linz
    # weather_hourly_url = wapi_hourly + "326269" + "?apikey=" + wapi_key #Maidenhead
    # weather_hourly_url = wapi_hourly + "53286" + "?apikey=" + wapi_key #Vancouver
    # weather_hourly_url = wapi_hourly + "328328" + "?apikey=" + wapi_key #London
    # weather_hourly_url = wapi_hourly + "22889" + "?apikey=" + wapi_key #Sydney
    # weather_hourly_url = wapi_hourly + "178087" + "?apikey=" + wapi_key #Berlin
    weather_hourly_json = requests.get(weather_hourly_url).json()
    # print "Location: " + myloc_name + " " + myloc_key
    precipitation_list = []
    for i in weather_hourly_json:
        precipitation_list.append(i["PrecipitationProbability"])
#     print precipitation_list
    light_it_up(precipitation_list)
    return

def colorWipe(strip, color, wait_ms=50):
    ## Wipe color across display a pixel at a time
    ## Can use this to test functionality
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)
        
## Function to send weather data to Neopixel LEDs ##
def light_it_up(forecast):
    forecast = forecast[:8]
    LED_COUNT = 8 # Number of LED pixels.
    LED_PIN = 18 # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ = 800000 # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 5 # DMA channel to use for generating signal (try 5)
    LED_INVERT = False # True to invert the signal (when using NPN transistor level shift)
    
    #Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    strip.setBrightness(20)
    # strip.setPixelColorRGB(0, 255, 0, 0) #set to green
    count = 0
    for i in forecast:
        if i < 30:
            print "Probability is " + str(i) + "%, so a low chance of rain"
            strip.setPixelColorRGB(count, 255, 0, 0) #GRB
            strip.show()
        elif i < 60:
            print "Probability is " + str(i) + "%, it's looking a bit dodgy out there"
            strip.setPixelColorRGB(count, 191, 255, 0)
            strip.show()
        else:
            print "Probability is " + str(i) + "%, so grab your brollie!"
            strip.setPixelColorRGB(count, 0, 255, 0)
            strip.show()
        count += 1
        time.sleep(0.2)

def main():
#     weather_url = "http://www.accuweather.com/en/at/salzburg/30760/hourly-weather-forecast/30760"
#     weather_url = "http://www.accuweather.com/en/gb/london/ec4a-2/hourly-weather-forecast/328328"
#     weather_url = "http://www.accuweather.com/en/au/sydney/22889/hourly-weather-forecast/22889"
#     weather_url = "http://www.accuweather.com/en/de/berlin/10178/hourly-weather-forecast/178087"
#     data_scraped = scrape_weather(weather_url)
#     button(locations_dict)
#     rain_forecast = weather_api()
#     light_it_up(rain_forecast)
    cap_sensor()
#     colorWipe(strip, Color(0, 0, 255)) #Green Wipe

if __name__ == '__main__':
    main()
