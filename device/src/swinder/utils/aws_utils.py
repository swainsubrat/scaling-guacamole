import logging
import json
import time

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from swinder.utils.constants import (CLIENT_ID, ENDPOINT, PORT,
                                     ROOT_CA_PATH, CERTIFICATE_PATH,
                                     PRIVATE_KEY_PATH)
# from constants import (CLIENT_ID, ENDPOINT, PORT,
#                                      ROOT_CA_PATH, CERTIFICATE_PATH,
#                                      PRIVATE_KEY_PATH)

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = AWSIoTMQTTClient(CLIENT_ID)
myAWSIoTMQTTClient.configureEndpoint(ENDPOINT, PORT)
myAWSIoTMQTTClient.configureCredentials(ROOT_CA_PATH, PRIVATE_KEY_PATH, CERTIFICATE_PATH)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(100)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(500)  # 5 sec

myAWSIoTMQTTClient.connect()

def publish(message, topic):
    """
    Publish messaged to pre-connected endpoint
    """
    request = {}
    request["id"]  = message["id"]
    request["action"] = message["action"]

    if message["action"] == "open":
        request["angle"] = message.get("angle", 90)
    else:
        request["angle"] = 0

    request["priority"] = 5
    messageJson = json.dumps(request)
    response = myAWSIoTMQTTClient.publish(topic, messageJson, 1)

    if response:
        print('Published topic %s: %s\n' % (topic, messageJson))
    
    return response

# Custom MQTT message callback
def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

def subscribe(topic, customCallback):
    response = myAWSIoTMQTTClient.subscribe(topic, 1, customCallback)

    return response


if __name__ == "__main__":
    while True:
        subscribe(topic="user_publish", customCallback=customCallback)
        time.sleep(10)