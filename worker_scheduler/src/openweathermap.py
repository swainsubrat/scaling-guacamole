import requests

from pprint import pprint
from datetime import datetime

from utils.constants import *


def get_schedule():
    complete_url = \
        f"https://api.openweathermap.org/data/2.5/onecall?lat={LAT}&lon={LON}&exclude=current,daily,alert,minutely&appid={API_KEY}"
    response = requests.get(complete_url)
    x = response.json()

    response = {"isSuccess": False}
    if x.get("cod"):
        response["message"] = x["message"]

        return response

    else:
        hourly_data = x.get("hourly")[:24]
        schedule = []

        for data in hourly_data:
            weather_desc = data["weather"][0]["description"]
            weather_main = data["weather"][0]["main"]

            ts = int(data["dt"])
            ts = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        
            action = None
            if weather_main == "Rain":
                action = "close"
            else:
                action = "open"

            schedule.append({
                "timestamp": ts,
                "action"   : action,
                "description": weather_desc
            })
        response["isSuccess"] = True
        response["schedule"]  = schedule

        return response

if __name__ == "__main__":
    schedule = get_schedule()
    pprint(schedule)