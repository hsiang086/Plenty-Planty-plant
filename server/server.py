##############################
# Copyright © hsiang086 2024 #
##############################

import random
import json
import socket
from fastapi import FastAPI, HTTPException, Query
import aiohttp

from database import ServerDatabase

app = FastAPI()

config = json.load(open('config.json'))
db = ServerDatabase()

async def send_discord_message(humidity: float, message="I am thirsty!"):
    webhook_url = config["WEBHOOK_URL"][random.randint(0, len(config["WEBHOOK_URL"])-1)]
    payload = {
        "username": "Plenty Planty Plant",
        "avatar_url": "https://watchandlearn.scholastic.com/content/dam/classroom-magazines/watchandlearn/videos/animals-and-plants/plants/what-are-plants-/What-Are-Plants.jpg",
        "content": f"{message}, the humidity is `{humidity}`!",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(webhook_url, json=payload) as response:
            return response.status

@app.get('/api/v1')
async def root():
    usage = {
        "/api/v1": "Get usage information",
        "/api/v1/humidity": "Send humidity value (?hu=VALUE<float>)",
        "/api/v1/led": "Get LED status",
        "/api/v1/setled": "Set LED (?status=on/off<string>)"
    }
    return usage

@app.get('/api/v1/humidity')
async def get_humidity(hu: float = Query(..., description="Humidity value")):
    await send_discord_message(humidity=hu)
    return hu

@app.get('/api/v1/led')
async def get_led():
    led_status = await db.get_led_status()
    if led_status is not None:
        return {"status": 1 if led_status else 0}
    else:
        return {"status": "off"}

@app.get('/api/v1/setled')
async def set_led(status: str = Query(..., description="LED status (on/off)")):
    if status.lower() == 'on':
        await db.set_led_status(True)
        return "LED status set to ON"
    elif status.lower() == 'off':
        await db.set_led_status(False)
        return "LED status set to OFF"
    else:
        raise HTTPException(status_code=400, detail="Invalid status value. Please use 'on' or 'off'.")

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

if __name__ == '__main__':
    ip = get_ip()
    print(f"Server running on \033[1mhttp://{ip}:1588\033[0m")

    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(db.init_db())
    
    import uvicorn
    try:
        uvicorn.run(app, host="0.0.0.0", port=1588)
    except KeyboardInterrupt:
        print("\033[91mServer stopped...\033[0m")

