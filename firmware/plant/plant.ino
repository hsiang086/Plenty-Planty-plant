#include <WiFi.h>
#include <HTTPClient.h>

#include "credentials.h"

void setup() {
    Serial.begin(serial_baud_rate);
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
        if (soil_moisture > 2000 && soil_moisture <= 4000) {
            sendRequest(soil_moisture);
        } else if (soil_moisture > 4000) {
            Serial.print("Soil moisture: ");
            Serial.println(soil_moisture);
            Serial.println("Not in use, please check the sensor.");
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
