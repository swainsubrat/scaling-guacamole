import os
import pickle

from pprint import pprint
from openweathermap import get_schedule

from utils.constants import *
from utils.aws_utils import publish

from datetime import date, datetime

def save(obj, path):
    outfile = open(path, 'wb')
    pickle.dump(obj, outfile)
    outfile.close()


def load(path):
    infile = open(path, 'rb')
    obj = pickle.load(infile)
    infile.close()

    return obj


def make_messages(schedule):
    """
    Create message structure from schedule
    """
    messages = []
    for id in REGISTERED_IDS:
        _dict = {}
        _dict["id"] = id
        _dict["action"] = schedule["action"]
        _dict["description"] = schedule["description"]
        messages.append(_dict)
    
    return messages

dirs = os.listdir("./forecasts")
today = str(date.today()) + ".pkl"

schedule = None
if today in dirs:
    schedule = load(f"./forecasts/{today}")
    print("Found Existing")
else:
    schedule = get_schedule()


if schedule["isSuccess"]:

    # find the latest schedule and publish
    for i in range(len(schedule)):

        ts = schedule["schedule"][i]["timestamp"]
        ts = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

        if datetime.now() >= ts:
            if schedule["schedule"][i].get("has_published", False):
                print("Already published the latest forecast")
                continue
            else:
                # publish
                messages = make_messages(schedule=schedule["schedule"][i])

                for message in messages:
                    publish(message, topic="worker_publish", priority=4)
                print("Published!!!!!!!!!")

                # update
                schedule["schedule"][i]["has_published"] = True
                break
        else:
            break
    
    save(schedule, f"./forecasts/{today}")
