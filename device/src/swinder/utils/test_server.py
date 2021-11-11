
# from flask import Flask, render_template
# from flask_mqtt import Mqtt

# import ssl
# import urllib.request as request

# from swinder.utils.constants import *

# app = Flask(__name__)

# app.config["MQTT_BROKER_URL"]   = ENDPOINT
# app.config["MQTT_BROKER_PORT"]  = PORT
# app.config["MQTT_CLIENT_ID"]    = CLIENT_ID
# app.config["MQTT_KEEPALIVE"]    = 60
# app.config["MQTT_TLS_ENABLED"]  = True
# app.config["MQTT_TLS_CA_CERTS"] = ROOT_CA_PATH
# app.config["MQTT_TLS_CERTIFICATE"] = CERTIFICATE_PATH
# app.config["MQTT_TLS_KEYFILE"]  = PRIVATE_KEY_PATH
# app.config["MQTT_TLS_CIPHERS"]  = None
# app.config["MQTT_TLS_CERT_REQS"]= ssl.CERT_REQUIRED
# app.config["MQTT_TLS_VERSION"]  = ssl.PROTOCOL_TLSv1_2

# # ssl._DEFAULT_CIPHERS = ('DES-CBC3-SHA')
# mqtt = Mqtt(app)

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     print("Connected and waiting for message")
#     mqtt.subscribe("user_publish")


# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, msg):
#     data = eval(msg.payload.decode('utf-8'))
#     print(data)


# @app.route("/")
# def index():
#     return "Home"

# TLS13-AES-256-GCM-SHA384:TLS13-CHACHA20-POLY1305-SHA256:TLS13-AES-128-GCM-SHA256:ECDH+AESGCM:ECDH+CHACHA20:DH+AESGCM:DH+CHACHA20:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:RSA+AESGCM:RSA+AES:RSA+HIGH:!aNULL:!eNULL:!MD5:!3DES