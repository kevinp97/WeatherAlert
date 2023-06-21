from twilio.rest import Client
from TwilioConfig import PHONE_NUMBER_FROM, PHONE_NUMBER_TO, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, API_KEY_WAPI, COORDINATE
from ScrapingData.WeatherData import Scraping, organizador_datos, creador_dataframe, temp_max_min_and_rain, format_prob_lluvia
import time
import requests
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime, time
import logging
logging.basicConfig(level=logging.DEBUG)

query = COORDINATE
api_key = API_KEY_WAPI
weather_url = f"http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={query}&days=1&aqi=yes&alerts=no"
response = requests.get(weather_url).json()["forecast"]
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN
phone_number_from = PHONE_NUMBER_FROM
phone_number_to = PHONE_NUMBER_TO
client = Client(account_sid, auth_token)

if __name__ == "__main__":
    datos = Scraping(response)
    dataframe = creador_dataframe(datos)
    temp_max, hora_temp_max, lluvia, hora_lluvia, prob_lluvia = temp_max_min_and_rain(dataframe)
    probabilidad_lluvia = format_prob_lluvia(prob_lluvia)
    mensaje = f"*PREVISIÓN DEL DÍA*\n\n\n -La temperatura máxima del día será de {temp_max} a las {hora_temp_max}.\n -Las probabilidades de lluvia son:\n{probabilidad_lluvia}\n "
    message = client.messages.create(
            body = mensaje,
            from_ = phone_number_from,
            to =  phone_number_to
        )
    logging.info(message.sid)