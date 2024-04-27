#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "phil's home";
const char* password = "Fabiowu20070806";

String serverName = "http://192.168.1.109:1588/api/v1/humidity";

const int soil_sensor = 36;

unsigned long lastTime = 0;
unsigned long timerDelay = 5000; // 10 seconds

void setup() {
    Serial.begin(9600);
    pinMode(soil_sensor,INPUT);
    WiFi.begin(ssid, password);
    Serial.println(String("I am connecting to ") + ssid + String("!"));
    Serial.print(String("connecting"));
    while (WiFi.status() != WL_CONNECTED) {
        delay(250);
        Serial.print(".");
    }
    Serial.print("\nConnected to WiFi, IP address: ");
    Serial.println(WiFi.localIP());
    Serial.println("WiFi status: ");
    WiFi.printDiag(Serial);
}

void loop() {
    int soil_moisture = analogRead(soil_sensor);
    if ((millis() - lastTime) > timerDelay) {
        if (soil_moisture > 2000) {
            sendRequest(soil_moisture);
        } else {
            Serial.print("Soil moisture: ");
            Serial.println(soil_moisture);
            Serial.println("Soil moisture is enough, no need to send request.");
        }
        lastTime = millis();
    }
}

void sendRequest(int soil_moisture) {
    HTTPClient http;
    http.begin(serverName + "?hu=" + String(soil_moisture));
    int httpCode = http.GET();
    if (httpCode > 0) {
        String payload = http.getString();
        Serial.print("HTTP status code: ");
        Serial.println(httpCode);
        Serial.print("Humidity: ");
        Serial.println(payload);
    }
    else {
        Serial.println("Error on HTTP request");
    }
    http.end();
}
