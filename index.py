#! /usr/bin/env python3

import argparse
import requests
from bs4 import BeautifulSoup


baseUrl = "https://weather.com/weather/today/l/{}:4:US"



def getWeatherInfo(zipcode):
    if type(zipcode)==str and len(zipcode)==5 and zipcode.isdigit():
        requestUrl = baseUrl.format(zipcode)
        weather = requests.get(requestUrl)
        if weather.status_code==200:
            pageData = BeautifulSoup(weather.text, 'html.parser')
            temperature = pageData.find(class_="today_nowcard-temp").span.get_text().replace("°","")
            # data = pageData.find(id="APP").find_all('div')[0]
            print(temperature)
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