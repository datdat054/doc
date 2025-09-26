#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include "DHT.h"
#include "Adafruit_Sensor.h"

// Thông tin Wifi
const char* ssid = "Phong 1";
const char* password = "66662626";

// ThingSpeak channel
String apiKey = "WL9VLNEICRKD2A2H";
const char* server = "api.thingspeak.com";

// ThingSpeak Alerts
const char* alertServer = "https://api.thingspeak.com/alerts/send";
String alertApiKey = "TAKVs6a7hVaw5HPloXO";

// Cảm biến DHT11
#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Relay
#define RELAY D1

WiFiClient client;

void setup() {
  Serial.begin(115200);
  delay(10);

  Serial.println("Connecting to WiFi...");
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");

  pinMode(RELAY, OUTPUT);
  digitalWrite(RELAY, LOW); // Mặc định tắt relay
  dht.begin();
}

void loop() {
  float temperature = dht.readTemperature();
  float humidity = dht.readHumidity();

  if (isnan(temperature) || isnan(humidity)) {
    Serial.println("Failed to read from DHT sensor!");
    delay(2000);
    return;
  }

  // Gửi dữ liệu lên ThingSpeak
  if (client.connect(server, 80)) {
    String postStr = "api_key=" + apiKey +
                     "&field1=" + String(temperature) +
                     "&field2=" + String(humidity);

    client.println("POST /update HTTP/1.1");
    client.println("Host: api.thingspeak.com");
    client.println("Connection: close");
    client.println("X-THINGSPEAKAPIKEY: " + apiKey);
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(postStr.length());
    client.println();
    client.println(postStr);

    Serial.printf("Temperature: %.1f °C, Humidity: %.1f %% => Sent to ThingSpeak\n",
                  temperature, humidity);
  }

  // Điều khiển relay + gửi cảnh báo khi vượt ngưỡng
  if (temperature >= 27) {
    digitalWrite(RELAY, HIGH);  // Bật relay
    Serial.println("Relay ON (Temp >= 27°C)");
    sendAlert(temperature, humidity);
  } else {
    digitalWrite(RELAY, LOW);   // Tắt relay
    Serial.println("Relay OFF (Temp < 27°C)");
  }

  delay(20000);
}

void sendAlert(float temp, float humi) {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure secureClient;
    secureClient.setInsecure();

    HTTPClient http;
    http.begin(secureClient, alertServer);

    http.addHeader("Content-Type", "application/x-www-form-urlencoded");
    http.addHeader("ThingSpeak-Alerts-API-Key", alertApiKey);

    String subject = "! Cảnh báo nhiệt độ ESP8266";
    String body = "Nhiệt độ cao: " + String(temp) + "°C (Ngưỡng 27°C), Độ ẩm: " + String(humi) + "%";

    String postData = "subject=" + subject + "&body=" + body;

    int httpCode = http.POST(postData);

    if (httpCode > 0) {
      Serial.printf("[ALERT] HTTP Response code: %d\n", httpCode);
      String payload = http.getString();
      Serial.println(payload);
    } else {
      Serial.printf("[ALERT] POST failed: %s\n", http.errorToString(httpCode).c_str());
    }

    http.end();
  }
}
