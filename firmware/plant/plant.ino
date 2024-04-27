/* Copyright © hsiang086 2024 */

#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

#include "credentials.h"

WebServer server(80);

void setup() {
    Serial.begin(serial_baud_rate);
    pinMode(soil_sensor, INPUT);
    pinMode(led, OUTPUT);
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
    setupRoutes();
    startServer();
}

void loop() {
    server.handleClient();
    int soil_moisture = analogRead(soil_sensor);
    if ((millis() - lastTime) > timerDelay) {
        if (soil_moisture > 4000) {
            Serial.print("Soil moisture: ");
            Serial.println(soil_moisture);
            Serial.println("Not in use, please check the sensor.");
        } else if (soil_moisture > 2000) {
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
    } else {
        Serial.println("Error on HTTP request");
    }
    http.end();
}

void handleRoot() {
    server.send(200, "text/plain", "Hello from ESP32!");
}

void handleLedAPI() {
    if (server.hasArg("color")) {
        String color = server.arg("color");
        if (color == "1") {
            digitalWrite(led, HIGH);
            server.send(200, "text/plain", "LED is on");  
        } else {
            digitalWrite(led, LOW);
            server.send(200, "text/plain", "LED is off");
        }
    }
}

void handleNotFound() {
    server.send(404, "text/plain", "Not found");
}

void setupRoutes() {
    server.on("/", HTTP_GET, handleRoot);
    server.on("/api/v1/led", HTTP_GET, handleLedAPI);
    server.onNotFound(handleNotFound);
}

void startServer() {
    server.begin();
    Serial.println("HTTP server started at " + WiFi.localIP().toString());
}
