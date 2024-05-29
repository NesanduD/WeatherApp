import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import sys
import time
import json
from tabulate import tabulate
import time
import sys

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.3'
}

# functions
def responses(url):  
    return requests.get(url, headers=header)

def status_check(resp):
    return resp.status_code != 200

def average(array_name):
    return round(sum(array_name) / len(array_name), 2)

def connecting_animation():
    animation = "|/-\\"
    for i in range(20):
        sys.stdout.write("\r" + "Connecting " + animation[i % len(animation)])
        sys.stdout.flush()
        time.sleep(0.1)

    sys.stdout.write("\rConnected!        \n")



# arrays
today_rain_day = []  # array for today daytime rain probablity
today_rain_night = []  # array for tonight rain prob.
tomorrow_rain_day = []  # array for tomorrow daytime rain probablity
tomorrow_rain_night = []  # array for tomorrow night rain prob.

# URLS
accuweather_url = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/837535?apikey=IeS7q8uvP3iefn51Qa4ReCfNihJgrGqU&details=true&metric=true'
weathercom_url = 'https://weather.com/weather/tenday/l/48df01ee9c0aadc73b846a4dc6c2074d9e87a951e2e69f33f70ce7e14dbc0ecf'
weatheratlas_url = 'https://www.weather-atlas.com/en/sri-lanka/katubedda-weather-tomorrow'
timeanddatecom_url = 'https://www.timeanddate.com/weather/@1241019/ext'

# Responses
accuweather_response = responses(accuweather_url)
weathercom_response = responses(weathercom_url)
weather_atlas_response = responses(weatheratlas_url)
timeaddatecom_response = responses(timeanddatecom_url)

connecting_animation()

# Timeanddatecom code
if status_check(timeaddatecom_response):
    print("Connection failed with timeanddate.com. Error code:", timeaddatecom_response.status_code)
else:
    print("Connection established with timeanddate.com.")
    timeanddatecom_html = requests.get(timeanddatecom_url).text
    timeanddatecom_soup = BeautifulSoup(timeanddatecom_html, 'html.parser')
    td_elements = timeanddatecom_soup.find_all('td', {'class': 'sep'})
    timeanddatecom_percentage_values = []

    for td in td_elements:
        text = td.get_text()
        if '%' in text:
            timeanddatecom_percentage_values.append(text)

    timeanddatecom_percentage_values = [int(p.strip("%")) for p in timeanddatecom_percentage_values]
    today_rain_day.append(timeanddatecom_percentage_values[0])
    today_rain_night.append(timeanddatecom_percentage_values[0])
    tomorrow_rain_day.append(timeanddatecom_percentage_values[1])
    tomorrow_rain_night.append(timeanddatecom_percentage_values[1])

# Weather-atlas code
if status_check(weather_atlas_response):
    print("Connection failed with weather-atlas.com. Error code:", weather_atlas_response.status_code)
else:
    print('Connection established with weather-atlas.com.')
    weather_atlas_html = requests.get(weatheratlas_url).text
    weather_atlas_soup = BeautifulSoup(weather_atlas_html, 'html.parser')
    ul_elements = weather_atlas_soup.find_all('ul', {'class': 'list-unstyled lh-sm mb-0'})
    weather_atlas_percentage_values = []
    
    for ul in ul_elements:
        li_elements = ul.find_all('li')
        for li in li_elements:
            if 'Precip. probability:' in li.get_text():
                precip_probability = li.find('span', {'class': 'fw-bold'}).get_text(strip=True)
                weather_atlas_percentage_values.append(precip_probability)

    weather_atlas_percentage_values_day = weather_atlas_percentage_values[4:11]
    weather_atlas_percentage_values_day = [int(p.strip("%")) for p in weather_atlas_percentage_values_day]
    weather_atlas_percentage_values_night = weather_atlas_percentage_values[11:]
    weather_atlas_percentage_values_night = [int(p.strip("%")) for p in weather_atlas_percentage_values_night]

    tomorrow_rain_day.append(sum(weather_atlas_percentage_values_day) / len(weather_atlas_percentage_values_day))
    tomorrow_rain_night.append(sum(weather_atlas_percentage_values_night) / len(weather_atlas_percentage_values_night))

# Weathercom code
if status_check(weathercom_response):
    print("Connection failed with weather.com. Error code:", weathercom_response.status_code)
else:
    print("Connection established with weather.com.")
    weathercom_html = requests.get(weathercom_url).text
    weathercom_soup = BeautifulSoup(weathercom_html, 'html.parser')
    percentage_value_elements = weathercom_soup.find_all('span', {'data-testid': 'PercentageValue'})

    weathercom_percentage_values = [int(element.text.strip("%")) for element in percentage_value_elements]

    today_rain_day.append(weathercom_percentage_values[0])
    today_rain_night.append(weathercom_percentage_values[4])

# Accuweather code
if status_check(accuweather_response):
    print("Connection failed with accuweather. Error code:", accuweather_response.status_code)
else:
    print("Connection established with accuweather.")
    data = accuweather_response.json()
    accuweather_daily_forecasts = data.get('DailyForecasts', [])
    accuweather_precipitation_probability_day = [adf.get('Day', {}).get('PrecipitationProbability', None) for adf in accuweather_daily_forecasts]
    accuweather_precipitation_probability_night = [b.get('Night', {}).get('PrecipitationProbability', None) for b in accuweather_daily_forecasts]

    today_rain_day.append(accuweather_precipitation_probability_day[0])
    today_rain_night.append(accuweather_precipitation_probability_night[0])
    tomorrow_rain_day.append(accuweather_precipitation_probability_day[1])
    tomorrow_rain_night.append(accuweather_precipitation_probability_night[1])

# Prepare data for tabulate
data = [
    ["Today Daytime", average(today_rain_day), len(today_rain_day)],
    ["Today Nighttime", average(today_rain_night), len(today_rain_night)],
    ["Tomorrow Daytime", average(tomorrow_rain_day), len(tomorrow_rain_day)],
    ["Tomorrow Nighttime", average(tomorrow_rain_night), len(tomorrow_rain_night)]
]

# Print the results in a tabulated format
print(tabulate(data, headers=["Period", "Rain Probability (%)", "Used sources Count"], tablefmt="pretty"))
