import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import sys
import time
header = Headers(
        browser="chrome",  # Generate only Chrome UA
        os="mac",  # Generate any Mac platform
        headers=False,  # generate misc headers
        )

# functions
def responses(url):  
    return requests.get(url, headers=header.generate())

def status_check(resp):
    if resp.status_code != 200:
        return True
    else:
        return False
    
# arrays
today_rain_day      = [] # array for today daytime rain probablity
today_rain_night    = [] # array for tonight rain prob.
tomorrow_rain_day   = [] # array for tomorrow daytime rain probablity
tomorrow_rain_night = [] # array for tomorrow night rain prob.


# URLS
accuweather_url    = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/309472?apikey=IeS7q8uvP3iefn51Qa4ReCfNihJgrGqU&details=true&metric=true'
weathercom_url     = 'https://weather.com/weather/tenday/l/fb23578d1e77fc9465448c2aa52f6e72e9b5f380bada48f4e626070fe3920cb2'
weatheratlas_url   = 'https://www.weather-atlas.com/en/sri-lanka/kuruwita-weather-tomorrow'
timeanddatecom_url = 'https://www.timeanddate.com/weather/@1237940/ext'
msn_url            = 'https://www.msn.com/en-us/weather/hourlyforecast/in-Kuruwita,Sabaragamuwa-Province?loc=eyJsIjoiS3VydXdpdGEiLCJyIjoiU2FiYXJhZ2FtdXdhIFByb3ZpbmNlIiwicjIiOiJSYXRuYXB1cmEgRGlzdHJpY3QiLCJjIjoiU3JpIExhbmthIiwiaSI6IkxLIiwidCI6MTAyLCJnIjoiZW4tc2ciLCJ4IjoiODAuMzY2ODk3NTgzMDA3ODEiLCJ5IjoiNi43NzYxMDAxNTg2OTE0MDYifQ%3D%3D&weadegreetype=C&cvid=651008f8734e43af9ab5ac9e1e3ba583'


# Responses
accuweather_response   = responses(accuweather_url)
weathercom_response    = responses(weathercom_url)
weather_atlas_response = responses(weatheratlas_url)
timeaddatecom_response = responses(timeanddatecom_url)
msn_response           = responses(msn_url)


#msn code
if msn_response.status_code != 200:
    print("Connection failed with msn.com. Error code: ",msn_response.status_code)
else:
    print("connection established with msn.com. ")
    msn_html = requests.get(msn_url).text
    # msn.com soupobject
    msn_soup = BeautifulSoup(msn_html,'html.parser')
    precip_elements = msn_soup.find_all('div', {'title': 'Chance of precipitation'})
    for precip_element in precip_elements:
        # Find all span elements inside the current precipitation div
        span_elements = precip_element.find_all('span')
        msn_today = span_elements[1].text.strip()
        print(span_elements)
        # still only today weather scraped. need to scrape msn tomorrow too
'''
# Timeanddatecom code
if timeaddatecom_response.status_code != 200:
    print("Connection failed with timeandweather.com. Error code: ",timeaddatecom_response.status_code)
else:
    print("connection established with timeanddate.com. ")
    timeanddatecom_html = requests.get(timeanddatecom_url).text
    #timeanddate.com soupobject
    timeanddatecom_soup = BeautifulSoup(timeanddatecom_html,'html.parser')
    td_elements = timeanddatecom_soup.find_all('td',{'class':'sep'})
    timeanddatecom_percentage_values = []

    for td in td_elements:
        # Extract text content
        text = td.get_text()

        # Check if the text is a percentage value
        if '%' in text:
            timeanddatecom_percentage_values.append(text)

    timeanddatecom_percentage_values=[int(p.strip("%")) for p in timeanddatecom_percentage_values ]
    today_rain_day.append(timeanddatecom_percentage_values[0])
    today_rain_night.append(timeanddatecom_percentage_values[0])

    tomorrow_rain_day.append(timeanddatecom_percentage_values[1])
    tomorrow_rain_day.append(timeanddatecom_percentage_values[1])



# Weather-atlas code
if weather_atlas_response.status_code !=200:
    print("Connection failed with weather-atlas.com. Error code: ",weather_atlas_response.status_code)
else:
    print('connection established with weather-atlas.com. ')
    weather_atlas_html = requests.get(weatheratlas_url).text

    #weather-atlas soupobject
    weather_atlas_soup = BeautifulSoup(weather_atlas_html,'html.parser')

    ul_elements = weather_atlas_soup.find_all('ul',{'class':'list-unstyled lh-sm mb-0'})
    weather_atlas_percentage_values = []
    for ul in ul_elements:
        # Find all li elements within the ul
        li_elements = ul.find_all('li')
        # Iterate through each li element
        for li in li_elements:
            # Check if the li element contains 'Precip. probability:'
            if 'Precip. probability:' in li.get_text():
                # Extract the value from the li element
                precip_probability = li.find('span', {'class': 'fw-bold'}).get_text(strip=True)
                weather_atlas_percentage_values.append(precip_probability)
                # Break out of the loop since we found the desired value
    # some processigng
    weather_atlas_percentage_values_day   = weather_atlas_percentage_values[4:11]
    weather_atlas_percentage_values_day   = [int(p.strip("%")) for p in weather_atlas_percentage_values_day]
    weather_atlas_percentage_values_night = weather_atlas_percentage_values[11:]
    weather_atlas_percentage_values_night = [int(p.strip("%")) for p in weather_atlas_percentage_values_night]
    # addng to main array (tomorrow)
    tomorrow_rain_day.append(weather_atlas_percentage_values_day/len(weather_atlas_percentage_values_day))
    tomorrow_rain_night.append(weather_atlas_percentage_values_night/len(weather_atlas_percentage_values_night)) 


# Weathercom code
if weathercom_response.status_code != 200:
    print("Connection failed with weather.com. Error code: ",weathercom_response.status_code)
else:
    print("connection established with weather.com.")
    weathercom_html = requests.get(weathercom_url).text

    # weathercom soupobject
    weathercom_soup  = BeautifulSoup(weathercom_html,'html.parser')

    # Find all elements with data-testid="PercentageValue"
    percentage_value_elements = weathercom_soup.find_all('span', {'data-testid': 'PercentageValue'})

    weathercom_percentage_values = []
    # Extract and store weather information on a list
    for element in percentage_value_elements:
        percentage_value = element.text
        weathercom_percentage_values.append(percentage_value)
    
        today_rain_day.append(weathercom_percentage_values[0]) # adding weathercom day time rain prob. 
        today_rain_night.append(weathercom_percentage_values[4]) # adding tonight rain


# Accuweather code
if status_check(accuweather_response):
    print("Connection failed with accuweather. Error code: ",accuweather_response.status_code)
else:
    print("connection established with accuweather.")

    # Parsing the JSON data
    data = accuweather_response.json()
    
    # get preciptitation data from all daily forecasts of accuweather
    accuweather_daily_forecasts = data.get('DailyForecasts', [])   
    accuweather_precipitation_probability_day = [adf.get('Day', {}).get('PrecipitationProbability', None) for adf in accuweather_daily_forecasts]
    accuweather_precipitation_probability_night = [b.get('Night', {}).get('PrecipitationProbability', None) for b in accuweather_daily_forecasts]
   
    # Preciptitation information
    today_rain_day.append(accuweather_precipitation_probability_day[0])
    today_rain_night.append(accuweather_precipitation_probability_night[0])


 ''' 

''' weathercom output
0 =  today rain
1 =  today rain
2 =  today humid
3 =  tonight rain 
4 =  tonight humid 
5 =  tomorrow day rain
6 =  tomorrow day rain
7 =  tomorrow day humid
8 =  tomorrow night rain
9 = tomorrow night humid

'''

'''weather_atlas output
Precip. probability: 86%
Precip. probability: 76%
Precip. probability: 100% today
Precip. probability: 96% tomorrow
Precip. probability: 100%
Precip. probability: 100%
Precip. probability: 96%
Precip. probability: 86%
Precip. probability: 76%
Precip. probability: 67%
Precip. probability: 60%
Precip. probability: 60%'''



