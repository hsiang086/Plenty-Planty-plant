/* Copyright © hsiang086 2024 */

#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <LiquidCrystal_I2C.h> 

#include "credentials.h"

class SendRequests {
    private:
        HTTPClient http;
        String serverUrl;
    public:
        SendRequests(String serverUrl) {
            this->serverUrl = serverUrl;
        }

        void sendHumidity(int soil_moisture) {
            http.begin(serverUrl + "/api/vi/humidity?hu=" + String(soil_moisture));
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

        String getLedStatus() {
            http.begin(serverUrl + "/api/v1/led");
            int httpCode = http.GET();

            if (httpCode == HTTP_CODE_OK) {
                String payload = http.getString();
                DynamicJsonDocument doc(1024);
                deserializeJson(doc, payload);
                int ledStatus = doc["status"];
                Serial.print("HTTP status code: ");
                Serial.println(httpCode);
                Serial.print("LED status: ");
                Serial.println(ledStatus);
                http.end();
                return String(ledStatus);
            } else {
                Serial.println("Error on HTTP request");
                http.end();
                return "";
            }
        }
};

SendRequests sendRequests(serverUrl);
// WebServer server(80); // Uncomment this line to enable the server

LiquidCrystal_I2C lcd(0x27,16,2);

void lcdinit(){
    lcd.init();
    lcd.backlight();
    lcd.setCursor(0,0);
    lcd.print("Hello, world!");
    lcd.setCursor(0,1);
    lcd.print("world, Hello!");
}

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
    lcdinit();
    // setupRoutes(); // Uncomment this line to enable the server
    // startServer(); // Uncomment this line to enable the server
}

void loop() {
    // server.handleClient(); // Uncomment this line to enable the server
    int soil_moisture = analogRead(soil_sensor);
    if ((millis() - lastTime) > timerDelay) {
        if (soil_moisture > 4000) {
            Serial.print("Soil moisture: ");
            Serial.println(soil_moisture);
            Serial.println("Not in use, please check the sensor.");
        } else if (soil_moisture > 2000) {
            sendRequests.sendHumidity(soil_moisture);
        } else {
            Serial.print("Soil moisture: ");
            Serial.println(soil_moisture);
            Serial.println("Soil moisture is enough, no need to send request.");
        }
        ledStatus = sendRequests.getLedStatus();
        // Serial.println(ledStatus);
        if (ledStatus == String("1")) {
            digitalWrite(led, HIGH);
        } else if (ledStatus == String("0")){
            digitalWrite(led, LOW);
        } else {
            Serial.println("LED status is not available.");
        }
        lastTime = millis();
    }
}

// void handleRoot() {
//     server.send(200, "text/plain", "Hello from ESP32!");
// }

// void handleLedAPI() {
//     if (server.hasArg("color")) {
//         String color = server.arg("color");
//         if (color == "1") {
//             digitalWrite(led, HIGH);
//             server.send(200, "text/plain", "LED is on");  
//         } else {
//             digitalWrite(led, LOW);
//             server.send(200, "text/plain", "LED is off");
//         }
//     }
// }

// void handleNotFound() {
//     server.send(404, "text/plain", "Not found");
// }

// void setupRoutes() {
//     server.on("/", HTTP_GET, handleRoot);
//     server.on("/api/v1/led", HTTP_GET, handleLedAPI);
//     server.onNotFound(handleNotFound);
// }

// void startServer() {
//     server.begin();
//     Serial.println("HTTP server started at " + WiFi.localIP().toString());
// }
