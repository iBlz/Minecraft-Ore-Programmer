#include <FastLED.h>
#include <ArduinoJson.h>
#define NUM_LEDS 30
#define LED_PIN 6

CRGB leds[NUM_LEDS];

uint8_t hue = 0;
bool colorSet = false;

void setup() {
  Serial.begin(9600);
  FastLED.addLeds<WS2812B, LED_PIN, GRB>(leds, NUM_LEDS);
  FastLED.setBrightness(25);
}

void loop() {
  search_for_lines();
  if (!colorSet) {
    rgb();
  }
}

void rgb() {
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i] = CHSV(hue + i, 255, 255);
  }
  EVERY_N_MILLISECONDS(10){
    hue++;
  }
  FastLED.show();
}

void search_for_lines()
{
  if (Serial.available())
  {
    StaticJsonDocument<64> doc;
    DeserializationError error = deserializeJson(doc, Serial.readString());
    if (!error) {
      const char* brightness = doc["brightness"];
      const char* hex = doc["hex"];
      const char* rgb_toggle = doc["rgb_toggle"];
      Serial.print("Brightness : ");
      Serial.println(brightness);
      Serial.print("Hex : ");
      Serial.println(hex);
      Serial.print("Rgb toggle : ");
      Serial.println(rgb_toggle);
      apply_json(brightness, hex, rgb_toggle);
    }
  }
}

void apply_json(int brightness, String hex, int rgb_toggle) {
  int brightnessInt = atoi(brightness);
  int rgb_toggleInt = atoi(rgb_toggle);
  FastLED.setBrightness(brightnessInt);
  if (rgb_toggleInt == 1) {
    long hexValue = strtol(hex.c_str(), NULL, 16);
    Serial.print("Hex ---> CRGB : ");
    Serial.print(hexValue);
    CRGB color = CRGB(hexValue);
    fill_solid(leds, NUM_LEDS, color);
    FastLED.show();
    colorSet = true;
  }
  else {
    colorSet = false;
  }
}