from flask import Flask, request
import requests
import json
import socket

app = Flask(__name__)

config = json.load(open('config.json'))

@app.route('/api/v1/humidity', methods=['GET'])
def get_humidity():
    humidity = request.args.get('hu')
    if humidity:
        sendDiscordMessage(humidity=humidity)
        return str(humidity), 200
    else:
        return "No humidity value provided", 400
def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    Ip = s.getsockname()[0]
    return Ip

def sendDiscordMessage(humidity, message="I am thirsty!"):
    webhook_url = config["WEBHOOK_URL"][1]
    payload = {
        "username": "Plenty Planty Plant",
        "avatar_url": "https://watchandlearn.scholastic.com/content/dam/classroom-magazines/watchandlearn/videos/animals-and-plants/plants/what-are-plants-/What-Are-Plants.jpg",
        "content": f"{message}, the humidity is `{humidity}`!",
    }
    res = requests.post(webhook_url, json=payload)
    return res.status_code

if __name__ == '__main__':
    Ip = getIpAddress()
    app.run(debug=True, host=Ip, port=1588)