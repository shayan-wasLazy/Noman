#include <Arduino.h>
#include <Wire.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <math.h>

#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>


// =====================================
// Configuration from .env
// =====================================

#ifndef WIFI_SSID
#error "WIFI_SSID is not defined"
#endif

#ifndef WIFI_PASSWORD
#error "WIFI_PASSWORD is not defined"
#endif

#ifndef BACKEND_HOST
#error "BACKEND_HOST is not defined"
#endif

#ifndef BACKEND_PORT
#error "BACKEND_PORT is not defined"
#endif

#ifndef NODE_ID
#error "NODE_ID is not defined"
#endif


// =====================================
// ADXL345
// =====================================

Adafruit_ADXL345_Unified accel =
    Adafruit_ADXL345_Unified(12345);


// =====================================
// Backend URL
// =====================================

String serverURL =
    "http://" +
    String(BACKEND_HOST) +
    ":" +
    String(BACKEND_PORT) +
    "/api/sensor";


// =====================================
// Timing
// =====================================

unsigned long lastSend = 0;

const unsigned long SEND_INTERVAL = 500;


// =====================================
// WiFi
// =====================================

void connectWiFi()
{
    Serial.print("Connecting to WiFi");

    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
    }

    Serial.println();

    Serial.println("WiFi connected!");

    Serial.print("ESP32 IP: ");
    Serial.println(WiFi.localIP());
}


// =====================================
// Send data to backend
// =====================================

void sendSensorData(
    float ax,
    float ay,
    float az
)
{
    if (WiFi.status() != WL_CONNECTED)
    {
        Serial.println("WiFi disconnected.");

        connectWiFi();

        return;
    }


    HTTPClient http;

    http.begin(serverURL);

    http.addHeader(
        "Content-Type",
        "application/json"
    );


    float magnitude =
        sqrt(
            ax * ax +
            ay * ay +
            az * az
        );


    String json = "{";

    json += "\"node_id\":\"";
    json += NODE_ID;
    json += "\",";

    json += "\"ax\":";
    json += String(ax, 3);
    json += ",";

    json += "\"ay\":";
    json += String(ay, 3);
    json += ",";

    json += "\"az\":";
    json += String(az, 3);
    json += ",";

    json += "\"magnitude\":";
    json += String(magnitude, 3);

    json += "}";


    Serial.println();
    Serial.println("Sending:");
    Serial.println(json);


    int responseCode =
        http.POST(json);


    Serial.print("HTTP Response: ");
    Serial.println(responseCode);


    http.end();
}


// =====================================
// Setup
// =====================================

void setup()
{
    Serial.begin(115200);

    delay(1000);


    Serial.println();
    Serial.println("==============================");
    Serial.println("SIH26025 SENSOR NODE");
    Serial.println("==============================");


    Serial.print("Node ID: ");
    Serial.println(NODE_ID);


    // I2C

    Wire.begin(21, 22);


    // ADXL345

    if (!accel.begin())
    {
        Serial.println(
            "ERROR: ADXL345 not detected!"
        );

        while (true)
        {
            delay(1000);
        }
    }


    Serial.println(
        "ADXL345 detected!"
    );


    accel.setRange(
        ADXL345_RANGE_16_G
    );


    // WiFi

    connectWiFi();


    Serial.print("Backend: ");
    Serial.println(serverURL);
}


// =====================================
// Loop
// =====================================

void loop()
{
    if (
        millis() - lastSend >=
        SEND_INTERVAL
    )
    {
        lastSend = millis();


        sensors_event_t event;

        accel.getEvent(&event);


        float ax =
            event.acceleration.x;

        float ay =
            event.acceleration.y;

        float az =
            event.acceleration.z;


        Serial.println();
        Serial.println(
            "========== SENSOR =========="
        );

        Serial.print("X: ");
        Serial.print(ax);
        Serial.println(" m/s^2");

        Serial.print("Y: ");
        Serial.print(ay);
        Serial.println(" m/s^2");

        Serial.print("Z: ");
        Serial.print(az);
        Serial.println(" m/s^2");


        sendSensorData(
            ax,
            ay,
            az
        );
    }
}