import pandas as pd
import requests
import json
import os

url = "https://meteostat.p.rapidapi.com/stations/daily"

querystring = {"station": "SBPR0", "start": "2021-01-02", "end": "2023-03-20"}

headers = {
    "X-RapidAPI-Key": os.environ['RAPID_API_KEY'],
    "X-RapidAPI-Host": "meteostat.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)
print(response)

df = pd.DataFrame(json.loads(response.text)['data'])

# Code	Meaning
# TAVG	Average Temperature
# TMIN	Minimum Temperature
# TMAX	Maximum Temperature
# DWPT	Dew Point
# PRCP	Total Precipitation
# WDIR	Wind (From) Direction
# WSPD	Average Wind Speed
# WPGT	Wind Peak Gust
# RHUM	Relative Humidity
# PRES	Sea-Level Air Pressure
# SNOW	Snow Depth
# TSUN	Total Sunshine Duration
# COCO	Weather Condition Code

rename_map = {
    'date': 'Date',
    'tavg': 'Average Temperature',  # Celsius
    'tmin': 'Minimum Temperature',  # Celsius
    'tmax': 'Maximum Temperature',  # Celsius
    'prcp': 'Total Precipitation',  # Millimeters
    'wdire': 'Wind (From) Direction',  # Degrees
    'wspd': 'Average Wind Speed',  # Kilometers per hour
    'pres': 'Sea-Level Air Pressure',  # hPa
    'rhum': 'Relative Humidity',  # Percent
    # 'snow': 'Snow Depth',  # Not used
    # 'wpgt': 'Wind Peak Gust',  # Not used
    # 'tsun': 'Total Sunshine Duration'  # Not used
}

df.drop(['snow', 'wpgt', 'tsun'], axis=1, inplace=True)
df.rename(columns=rename_map, inplace=True)

df.to_csv('../data/data.csv', index=False)

