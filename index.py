#! /usr/bin/env python3

import argparse
import requests
import pandas as pd
from bs4 import BeautifulSoup

baseScrapeUrl = "https://weather.com/weather/today/l/{zipcode}:4:US"
darkSkyApiUrl = "https://api.darksky.net/forecast/{key}/{lat},{lng}"

#Optimally needs a cache to limit api calls. Maybe thats something that my calling func should be doing?

try:
    with open("darkSkyKey.txt") as darkSkyKeyFile:
        darkSkyKey = darkSkyKeyFile.read()
    zipcodeConversion = pd.read_csv("USZipCodeToLatLong.csv",dtype=str)
except IOError as e: 
    raise Exception("Must supply an api key under darkSkyKey.txt and a csv file called USZipCodeToLatLong.csv") from e
except:
    raise Exception("Something terrible happened")

def getWeatherInfo(zipcode, shouldScrape=False):
    validZip = type(zipcode)==str and len(zipcode)==5 and zipcode.isdigit()
    if validZip:
        if shouldScrape:
            requestUrl = baseScrapeUrl.format(zipcode=zipcode)
            weather = requests.get(requestUrl)
            if weather.status_code==200:
                pageData = BeautifulSoup(weather.text, 'html.parser')
                temperature = pageData.find(class_="today_nowcard-temp").span.get_text().replace("°","")
                # data = pageData.find(id="APP").find_all('div')[0]
                print(temperature)
        else:
            try:
                latAndLong = zipcodeConversion.loc[zipcodeConversion['ZIP']==zipcode].iloc[0]
            except:
                print("Zip mapping missing for"+zipcode)
                return({"error":"Zip mapping missing for"+zipcode})
            print(latAndLong)
            requestUrl = darkSkyApiUrl.format(key=darkSkyKey,lat=latAndLong["LAT"],lng=latAndLong["LNG"])
            print(requestUrl)
            weatherData = requests.get(requestUrl)
            print(weatherData.json())
            print("Get data from api")
            #Still needs to return weather data
    else:
        print("Zip needs to be a valid 5 digit code")
        return({"error":"Zip needs to be a valid 5 digit code"})


def printWeatherSummary(weatherInfo):
    print("Weather info!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Submit zipcode for parsing")
    parser.add_argument("zipcode",type=str,help="Enter zipcode to find weather for")
    arguments = parser.parse_args()
    printWeatherSummary(getWeatherInfo(arguments.zipcode))