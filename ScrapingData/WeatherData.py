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


if __name__ == "__main__":
    response = requests.get(weather_url).json()
    #Comprobamos que esta la clave forecast
    logging.info(response.keys())
    weather_data = response["forecast"]
    with open('WeatherData.json', 'w') as jf: 
        json.dump(weather_data, jf, ensure_ascii=False, indent=4)