import os
from twilio.rest import Client
import sys
sys.path.append("..")  # Agrega el directorio anterior al PATH
from TwilioConfig import PHONE_NUMBER, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, API_KEY_WAPI, COORDINATE
import time
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG)

query = COORDINATE
api_key = API_KEY_WAPI
weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1&aqi=yes&alerts=no"
response = requests.get(weather_url).json()["forecast"]
class Scraping():
    
    def __init__(self, data):
        self.data = data
        
        
    def date(self, ind):
        # '2023-06-20 00:00' este es el formato de la fecha
        return self.data['forecastday'][0]['hour'][ind]['time'].split(' ')[0]
    
    def hour(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['time'].split(' ')[1]
        
    def temp(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['temp_c']
        
    def condition(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['condition'][0]['text']
        
    def wind(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['wind_kph']
        
    def sensation(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['feelslike_c']
        
    def rain(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['will_it_rain']
        
    def prob_rain(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['chance_of_rain']
      
        
if __name__ == "__main__":
    # response = requests.get(weather_url).json()
    # #Comprobamos que esta la clave forecast
    # logging.info(response.keys())
    # weather_data = response["forecast"]
    # with open('WeatherData.json', 'w') as jf: 
    #     json.dump(weather_data, jf, ensure_ascii=False, indent=4)
        
    # logging.warning(weather_data['forecastday'][0]['hour'][23]['time'])
        
    #Obtenemos la fecha
    datos = Scraping(response)
    for i in range(24):
        fecha = datos.hour(i)
        logging.info(fecha)