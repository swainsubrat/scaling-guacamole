"""
publish(Client) =====>>>===== AWS_IoT[AWS_IoT(subscribe); AWS_IoT(publish)] =====>>>===== subscribe(Device)
"""
from flask import Flask, render_template
from swinder.utils.aws_utils import subscribe

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
message_published = None

# Custom MQTT message callback
def customCallback(client, userdata, message):
    global message_published
    message_published = eval(message.payload.decode('utf-8'))
    print(type(message.payload))
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("-------------\n\n")

subscribe(topic="user_publish", customCallback=customCallback)

@app.route("/")
@app.route("/home")
def home():
    global message_published
    return render_template("index.html", message=message_published)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=True)
