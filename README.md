# Plenty Planty plant

## Description
This is a plant watering app that helps you keep track of your plants and when they need to be watered. You can add plants to your garden and set a watering schedule for each plant. The app will remind you when it's time to water your plants.

## Installation
To install and run the server, follow these steps:
1. Clone the repository
2. cd into the project directory
3. Run `pip install -r requirements.txt` to install the dependencies
4. Modify the `config.json` file to include your database credentials. The file should look like this:
```json
{
    "WEBHOOK_URL": [
        "url1",
        "url2",
        "..."
    ], 
    "DISCORD_TOKEN": "your_discord_bot_token",
    "PREFIX": "your_discord_bot_prefix",
}
```
5. Run `python server.py` to start the server
6. Run `python bot.py` to start the bot

after that, you can compile and upload the firmware to the ESP32. The firmware is located in the `firmware/plant` directory.
ensure that you have add the `credentials.h` file to the `firmware/plant` directory. The file should look like this example:
```cpp
const int serial_baud_rate = 9600;
const int soil_sensor =        36; // GPIO36

const char* ssid =     "********";
const char* password = "********";

const String serverName = "http://192.168.1.109:1588/api/v1/humidity";

unsigned long lastTime =        0;
unsigned long timerDelay =   5000;
```
You can use the Arduino IDE to compile and upload the firmware to your esp32.

## Contributing
If you would like to contribute to the project, feel free to fork the repository and submit a pull request. You can also open an issue if you have any suggestions or feedback.You can also contact me at: [email](mailto:fabiowu20070806@gmail.com)
