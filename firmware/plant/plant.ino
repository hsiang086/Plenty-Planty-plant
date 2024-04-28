/* Copyright © hsiang086 2024 */

#include <WiFi.h>
#include <WebServer.h>
#include <HTTPClient.h>

#include "credentials.h"

class SendRequests {
    private:
        HTTPClient http;
        String serverName;
    public:
        SendRequests(String serverName) {
            this->serverName = serverName;
        }

        void sendHumidity(int soil_moisture) {
            http.begin(serverName + "/api/vi/humidity?hu=" + String(soil_moisture));
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
            http.begin(serverName + "/api/v1/led");
            int httpCode = http.GET();
            String ledStatus;
            if (httpCode > 0) {
                ledStatus = http.getString();
                Serial.print("HTTP status code: ");
                Serial.println(httpCode);
                Serial.print("LED status: ");
                Serial.println(ledStatus);
            } else {
                Serial.println("Error on HTTP request");
            }
            http.end();
            return ledStatus;
        }
};

SendRequests sendRequests(serverName);
// WebServer server(80); // Uncomment this line to enable the server

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
