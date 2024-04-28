from flask import Flask, request
import requests
import json
import socket
import random
from database import LEDDatabase

app = Flask(__name__)

config = json.load(open('config.json'))
db = LEDDatabase()

@app.route('/api/v1/humidity', methods=['GET'])
def get_humidity():
    humidity = request.args.get('hu')
    if humidity:
        send_discord_message(humidity=humidity)
        return str(humidity), 200
    else:
        return "No humidity value provided", 400
    
@app.route('/api/v1/led', methods=['GET'])
def get_led():
    led_status = db.get_led_status()
    if led_status is not None:
        return str(1 if led_status else 0), 200
    else:
        return "LED status not found", 404

@app.route('/api/v1/setled', methods=['GET'])
def set_led():
    status = request.args.get('status')
    if status:
        status = status.lower()  # Convert to lowercase for case-insensitive comparison
        if status == 'on':
            db.set_led_status(True)
            return "LED status set to ON", 200
        elif status == 'off':
            db.set_led_status(False)
            return "LED status set to OFF", 200
        else:
            return "Invalid status value. Please use 'on' or 'off'.", 400
    else:
        return "No status value provided", 400
    
def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    return ip

def send_discord_message(humidity, message="I am thirsty!"):
    webhook_url = config["WEBHOOK_URL"][random.randint(0, len(config["WEBHOOK_URL"])-1)]
    payload = {
        "username": "Plenty Planty Plant",
        "avatar_url": "https://watchandlearn.scholastic.com/content/dam/classroom-magazines/watchandlearn/videos/animals-and-plants/plants/what-are-plants-/What-Are-Plants.jpg",
        "content": f"{message}, the humidity is `{humidity}`!",
    }
    res = requests.post(webhook_url, json=payload)
    return res.status_code

if __name__ == '__main__':
    ip = get_ip_address()
    app.run(debug=True, host="0.0.0.0", port=1588)
