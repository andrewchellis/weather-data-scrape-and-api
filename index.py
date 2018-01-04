#! /usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup


baseScrapeUrl = "https://weather.com/weather/today/l/{}:4:US"
darkSkyKey = ""
try:
    with open("darkSkyKey.txt") as darkSkyKeyFile:
        darkSkyKey = darkSkyKeyFile.read()
except IOError as e: 
    raise Exception("Must supply an api key under darkSkyKey.txt") from e
except:
    raise Exception("Something terrible happened")

def getWeatherInfo(zipcode, shouldScrape=False):
    validZip = type(zipcode)==str and len(zipcode)==5 and zipcode.isdigit()
    if validZip:
        if shouldScrape:
            requestUrl = baseScrapeUrl.format(zipcode)
            weather = requests.get(requestUrl)
            if weather.status_code==200:
                pageData = BeautifulSoup(weather.text, 'html.parser')
                temperature = pageData.find(class_="today_nowcard-temp").span.get_text().replace("°","")
                # data = pageData.find(id="APP").find_all('div')[0]
                print(temperature)
        else:
            print("Get data from api")
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