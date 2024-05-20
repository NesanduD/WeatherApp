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

# URLS
accuweather_url    = 'http://dataservice.accuweather.com/forecasts/v1/daily/5day/309472?apikey=IeS7q8uvP3iefn51Qa4ReCfNihJgrGqU&details=true&metric=true'
weathercom_url     = 'https://weather.com/weather/tenday/l/746ec06059a777b4fe27c23654cd84da9bf2c4f2ebc7ee53f098aaf52d94eb87'
weatheratlas_url   = 'https://www.weather-atlas.com/en/sri-lanka/kuruwita-long-term-weather-forecast'
timeanddatecom_url = 'https://www.timeanddate.com/weather/@1237940/ext'

# Responses
accuweather_response = requests.get(accuweather_url, headers=header.generate())
weathercom_response = requests.get(weathercom_url,headers=header.generate())
weather_atlas_response = requests.get(weatheratlas_url,headers=header.generate())
timeaddatecom_response = requests.get(timeanddatecom_url,headers=header.generate())

# Timeanddatecom code
if timeaddatecom_response.status_code != 200:
    print("Connection failed with timeandweather.com. Error code: ",timeaddatecom_response.status_code)
else:
    print("connection established with timeanddate.com. ")
    timeanddatecom_html = requests.get(timeanddatecom_url).text
    #timeanddate.com soupobject
    timeanddatecom_soup = BeautifulSoup(timeanddatecom_html,'html.parser')
    

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
                break

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
        
# Accuweather code
if accuweather_response.status_code != 200:
    print("Connection failed with accuweather. Error code: ",accuweather_response.status_code)
else:
    print("connection established with accuweather.")

    # Parsing the JSON data
    data = accuweather_response.json()
    
    # get preciptitation data from all daily forecasts of accuweather
    accuweather_daily_forecasts = data.get('DailyForecasts', [])   
    accuweather_precipitation_probability = [adf.get('Day', {}).get('PrecipitationProbability', None) for adf in accuweather_daily_forecasts]
    
    # Preciptitation information
    today_precipitation_accuweather = accuweather_precipitation_probability[0]
    tomorrow_precipitation_accuweather = accuweather_precipitation_probability[1]
    
''' weathercom output
Percentage Value: 96% today rain
Percentage Value: 96% today rain
Percentage Value: 86% humid today
Percentage Value: 59% rain tonight
Percentage Value: 98% tomorrow day rain
Percentage Value: 97% humid
Percentage Value: 97% rain tomorrow day
Percentage Value: 84% humid
Percentage Value: 87% rain tomorrow night
Percentage Value: 92%
Percentage Value: 83% humid
Percentage Value: 68% night rain 11
Percentage Value: 98% humid
Percentage Value: 99%
Percentage Value: 99%
Percentage Value: 83%
Percentage Value: 78%
Percentage Value: 99%
    Percentage Value: 95%
Percentage Value: 95%
    Percentage Value: 85%
Percentage Value: 60%
Percentage Value: 99%
Percentage Value: 85%
Percentage Value: 85%
Percentage Value: 85%
Percentage Value: 72%
Percentage Value: 99%
    Percentage Value: 76%
Percentage Value: 76%
Percentage Value: 86%
Percentage Value: 73%
Percentage Value: 99%
    Percentage Value: 66%
Percentage Value: 66%
Percentage Value: 86%
Percentage Value: 24%
Percentage Value: 98%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 85%
Percentage Value: 60%
Percentage Value: 99%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 89%
Percentage Value: 60%
Percentage Value: 99%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 89%
Percentage Value: 60%
Percentage Value: 99%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 88%
Percentage Value: 60%
Percentage Value: 99%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 88%
Percentage Value: 60%
Percentage Value: 98%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 87%
Percentage Value: 60%
Percentage Value: 98%
Percentage Value: 60%
Percentage Value: 60%
Percentage Value: 88%
Percentage Value: 60%
Percentage Value: 99%
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