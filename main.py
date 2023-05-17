import requests
from datetime import datetime as dt
from twilio.rest import Client
import os

weather_apikey = os.environ['ODO35_APIKEY']
account_sid = os.environ['ODO35_ACCSID']
auth_token = os.environ['ODO35_AUTHTOKEN']
twilio_number = environ['TWILIO_NUMBER']
my_number = environ['MY_NUMBER']
client = Client(account_sid, auth_token)
parameters = {
    "q": "-33.88,151.15",
    "key": weather_apikey,
    "days": 2,
    "aqi": "no",
    "tides": "no",
}

response = requests.get("http://api.weatherapi.com/v1/forecast.json", params=parameters)
response.raise_for_status()
request_data = response.json()
next_48 = request_data['forecast']['forecastday'][0]['hour'] + request_data['forecast']['forecastday'][1]['hour']

next_48_condition = []
count = 0
for _ in next_48:
    next_48_condition.append(next_48[count]['condition']['code'])
    count += 1
condition_slice = next_48_condition[dt.now().hour: dt.now().hour + 12]

rain = ""
for _ in condition_slice:
    if _ >= 1150:
        rain = True
if rain:
    client.messages.create(
        body="It's going to rain in the next 12 hours.",
        from_=twilio_number,
        to=my_number
    )
    print("It's going to rain in the next 12 hours")
