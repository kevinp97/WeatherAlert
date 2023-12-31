import sys
sys.path.append("..")  # Agrega el directorio anterior al PATH
from TwilioConfig import API_KEY_WAPI, COORDINATE
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
        return self.data['forecastday'][0]['hour'][ind]['condition']['text']
        
    def wind(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['wind_kph']
        
    def sensation(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['feelslike_c']
        
    def rain(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['will_it_rain']
        
    def prob_rain(self, ind):
        return self.data['forecastday'][0]['hour'][ind]['chance_of_rain']
      
def organizador_datos(datos, i):
    date = datos.date(i)
    hour = datos.hour(i)
    temp = datos.temp(i)
    condition = datos.condition(i)
    wind = datos.wind(i)
    sensation = datos.sensation(i)
    rain = datos.rain(i)
    prob_rain = datos.prob_rain(i)
        
    return [date, hour, temp, condition, wind, sensation, rain, prob_rain]

def creador_dataframe(datos):
    data = []
    for i in tqdm(range(0,24)):
        data.append(organizador_datos(datos,i))
        
    dataframe = pd.DataFrame(data, columns=["Fecha", "Hora", "Temperatura", "Condicion", "Viento","Sensacion", "Lluvia", "Probabilidad_Lluvia"])
    dataframe["Fecha"] = pd.to_datetime(dataframe["Fecha"])
    dataframe["Hora"] = pd.to_datetime(dataframe['Hora'], format='%H:%M').dt.time
    return dataframe
        
    
def temp_max_min_and_rain(dataframe):
    temp_max = dataframe['Temperatura'].max()
    hora_temp_max = dataframe[dataframe['Temperatura'] == dataframe['Temperatura'].max()]['Hora']
    lluvia = dataframe[(dataframe['Lluvia'] == 1) & (dataframe['Hora'] >= time(8,0)) & (dataframe['Hora'] <= time(21,0))]
    hora_lluvia = dataframe[(dataframe['Lluvia'] == 1) & (dataframe['Hora'] >= time(8,0)) & (dataframe['Hora'] <= time(21,0))]['Hora']
    prob_lluvia = dataframe[(dataframe['Hora'] >= time(8,0)) & (dataframe['Hora'] <= time(21,0))]['Probabilidad_Lluvia']
    prob_lluvia.index.name = 'Hora'
    prob_lluvia.name = "Probabilidad lluvia"
    
    return temp_max, hora_temp_max, lluvia, hora_lluvia, prob_lluvia

def format_prob_lluvia(prob_lluvia):
    mensaje = ''
    for hora, prob in prob_lluvia.items():
        mensaje += f"\t- A las {hora}:00 -> {prob}%\n"
    return mensaje
    
        
if __name__ == "__main__":
    datos = Scraping(response)
    dataframe = creador_dataframe(datos)
    logging.warning(dataframe.dtypes)
    
    
    
    
    
    
    
    
    
    
    
