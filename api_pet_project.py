import requests
from datetime import datetime
import json


adress_1 = 'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API}'
adress_2 = 'https://www.cbr-xml-daily.ru/daily_json.js'
adress_3 = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo'


API_alphavantage = ''                   # api key на сайте www.alphavantage.co
API_openweather = ''    # api key  Вовы на сайте openweather
# API = ''              # api key мой апи на сайте openweather но он не работает...
city = 'Saransk'
stock = 'IBM'
interval = '60min'


def download_data(adress_1,adress_2,adress_3, API_1,API_3, stock,interval, city):
    ''' Функция будет обращаться на ресурсы и скачивать оттуда сырые данные'''

    api_response_weather = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_1}').text
    data_1 = json.loads(api_response_weather)

    api_response_currency = requests.get(adress_2).text
    data_2 = json.loads(api_response_currency)

    api_response_stocks = requests.get(
        f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval={interval}&apikey={API_3}').text
    data_3 = json.loads(api_response_stocks)

    return data_1, data_2, data_3


def data_processing(data_1, data_2, data_3, interval):
    '''Обработка данных из массивов. Парсинг необходимых данных. Создание ключевых переменных.'''
    processed_3 = []
    processed_2 = []
    processed_1 = [round(data_1['main']['temp']), data_1['wind']['speed']]
    forecast_day = datetime.utcfromtimestamp(data_1['dt']).strftime('%Y-%m-%d %H:%M:%S')   # дата
    processed_1.append(forecast_day[:11])

    processed_2.append(data_2['Date'][:10])                                                # дата на сайте cbr
    processed_2.append(data_2['Valute']['EUR']['Value'])                                   # курс евро
    processed_2.append(data_2['Valute']['EUR']['Name'])                                    # название валюты

    processed_3.append(data_3['Meta Data']['2. Symbol'])                                    # название акции
    actual_date = data_3['Meta Data']['3. Last Refreshed']                                  # время последнего обновления курса
    processed_3.append(actual_date)
    processed_3.append(data_3[f'Time Series ({interval})'][f'{actual_date}']['4. close'])   # курс акции на закрытии

    return processed_1, processed_2, processed_3


def data_visualization(processed_1, processed_2, processed_3, city):
    '''Отображение ключевых переменных с пояснениями'''
    print(f'Прогноз погоды на {processed_1[2]}')
    print(f'Среднесуточная температура в городе {city} - {processed_1[0]} градус/а/ов')
    print(f'Скорость ветра {processed_1[1]} метра в секунду')
    print()
    print(f'Курсы валют на {processed_2[0]}')
    print(f'Курс {processed_2[2]} {processed_2[1]}')
    print()
    print(f'Курс акции на последнюю временную точку {processed_3[1]}')
    print(f'{processed_3[0]} - название акции')
    print(f'{processed_3[2]} - среднедневной курс')

massive_1, massive_2, massive_3 = download_data(adress_1, adress_2, adress_3, API_openweather,API_alphavantage, stock,interval, city)
key_var_massive_1, key_var_massive_2, key_var_massive_3 = data_processing(massive_1,massive_2,massive_3, interval)
data_visualization(key_var_massive_1, key_var_massive_2, key_var_massive_3, city)

'''Вопрос насколько нам нужны массивы везде на выходах
Можно словари сделать - мне нравится идея
Можно список списков, но будет немного некрасиво
Оставим пока так, вроде должно быть правильно'''

