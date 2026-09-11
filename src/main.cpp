#include <Arduino.h>
#include <WiFi.h>
#include <HTTPClient.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_ADXL345_U.h>

#include "env_config.h"


// ============================================================
// ADXL345
// ============================================================

Adafruit_ADXL345_Unified accel =
    Adafruit_ADXL345_Unified(12345);


// ============================================================
// TIMING
// ============================================================

const unsigned long SENSOR_INTERVAL = 1000;

unsigned long lastSensorSend = 0;


// ============================================================
// SERVER URL
// ============================================================

String serverURL;


// ============================================================
// CONNECT TO WIFI
// ============================================================

void connectWiFi()
{
    Serial.println();
    Serial.println("Connecting to WiFi...");

    WiFi.mode(WIFI_STA);

    WiFi.begin(
        WIFI_SSID,
        WIFI_PASSWORD
    );

    int attempts = 0;

    while (
        WiFi.status() != WL_CONNECTED &&
        attempts < 30
    )
    {
        delay(500);

        Serial.print(".");

        attempts++;
    }

    Serial.println();

    if (WiFi.status() == WL_CONNECTED)
    {
        Serial.println("WiFi connected!");

        Serial.print("IP Address: ");
        Serial.println(WiFi.localIP());

        Serial.print("MAC Address: ");
        Serial.println(WiFi.macAddress());
    }
    else
    {
        Serial.println(
            "WiFi connection failed"
        );
    }
}


// ============================================================
// SEND SENSOR DATA
// ============================================================

void sendSensorData(
    float x,
    float y,
    float z
)
{
    if (
        WiFi.status() != WL_CONNECTED
    )
    {
        Serial.println(
            "WiFi disconnected"
        );

        connectWiFi();

        return;
    }


    HTTPClient http;

    http.begin(serverURL);

    http.addHeader(
        "Content-Type",
        "application/json"
    );


    // --------------------------------------------------------
    // JSON
    // --------------------------------------------------------

    String json = "{";

    json += "\"node_id\":\"";
    json += NODE_ID;
    json += "\",";

    json += "\"x\":";
    json += String(x, 4);
    json += ",";

    json += "\"y\":";
    json += String(y, 4);
    json += ",";

    json += "\"z\":";
    json += String(z, 4);

    json += "}";


    Serial.println();
    Serial.println(
        "Sending sensor data..."
    );

    Serial.println(json);


    // --------------------------------------------------------
    // POST
    // --------------------------------------------------------

    int responseCode =
        http.POST(json);


    Serial.print(
        "HTTP Response: "
    );

    Serial.println(responseCode);


    if (responseCode > 0)
    {
        String response =
            http.getString();

        Serial.println(
            "Server response:"
        );

        Serial.println(response);
    }
    else
    {
        Serial.print(
            "HTTP Error: "
        );

        Serial.println(
            http.errorToString(
                responseCode
            )
        );
    }


    http.end();
}


// ============================================================
// SETUP
// ============================================================

void setup()
{
    Serial.begin(115200);

    delay(1000);


    Serial.println();
    Serial.println(
        "================================"
    );

    Serial.println(
        "SIH26025 MINE MONITORING NODE"
    );

    Serial.println(
        "================================"
    );


    // --------------------------------------------------------
    // Node information
    // --------------------------------------------------------

    Serial.print(
        "Node ID: "
    );

    Serial.println(NODE_ID);


    // --------------------------------------------------------
    // WiFi
    // --------------------------------------------------------

    connectWiFi();


    // --------------------------------------------------------
    // Server URL
    // --------------------------------------------------------

    serverURL =
        "http://" +
        String(BACKEND_HOST) +
        ":" +
        String(BACKEND_PORT) +
        "/api/sensor";


    Serial.print(
        "Backend: "
    );

    Serial.println(
        serverURL
    );


    // --------------------------------------------------------
    // ADXL345
    // --------------------------------------------------------

    Serial.println(
        "Initializing ADXL345..."
    );


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


    accel.setRange(
        ADXL345_RANGE_2_G
    );


    Serial.println(
        "ADXL345 initialized"
    );


    Serial.println(
        "================================"
    );
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
    unsigned long now =
        millis();


    // --------------------------------------------------------
    // Send every 1 second
    // --------------------------------------------------------

    if (
        now - lastSensorSend
        >= SENSOR_INTERVAL
    )
    {
        lastSensorSend = now;


        // ----------------------------------------------------
        // Read accelerometer
        // ----------------------------------------------------

        sensors_event_t event;

        accel.getEvent(
            &event
        );


        // ADXL345 gives m/s²
        // Convert to g

        float x =
            event.acceleration.x /
            SENSORS_GRAVITY_STANDARD;

        float y =
            event.acceleration.y /
            SENSORS_GRAVITY_STANDARD;

        float z =
            event.acceleration.z /
            SENSORS_GRAVITY_STANDARD;


        // ----------------------------------------------------
        // Print
        // ----------------------------------------------------

        Serial.println();
        Serial.println(
            "Sensor reading:"
        );

        Serial.print("X: ");
        Serial.print(x, 4);
        Serial.println(" g");

        Serial.print("Y: ");
        Serial.print(y, 4);
        Serial.println(" g");

        Serial.print("Z: ");
        Serial.print(z, 4);
        Serial.println(" g");


        // ----------------------------------------------------
        // Send
        // ----------------------------------------------------

        sendSensorData(
            x,
            y,
            z
        );
    }
}