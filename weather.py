import urllib2
from bs4 import BeautifulSoup
# url = "http://www.wunderground.com/history/airport/KBUF/2011/1/1/DailyHistory.html?theprefset=SHOWMETAR&theprefvalue=1&format=1"
# url = "https://www.wunderground.com/at/salzburg/zmw:00000.1.11350/precipitation"
# url = "http://weather.weatherbug.com/weather-forecast/hourly/salzburg-salzburg-au"

# Hourly weather available thru accuweather
url = "http://www.accuweather.com/en/at/salzburg/30760/hourly-weather-forecast/30760"
# url = "http://www.accuweather.com/en/gb/london/ec4a-2/hourly-weather-forecast/328328"
page = urllib2.urlopen(url)
soup = BeautifulSoup(page, 'html.parser')
                           
print soup.title

table = soup.find('table')

#Hours
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

#Rain section of table
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

print hours
print rain

for i in rain:
    if i < 50:
        print "Low chance of rain"
    else:
        print "Grab your brollie!"
# weather_dict = dict(zip(hours, rain))
# print weather_dict