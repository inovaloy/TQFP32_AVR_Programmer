#define BUILD_IN_LED 13

void setup()
{
    pinMode(BUILD_IN_LED, OUTPUT);
    Serial.begin(115200);
}

void loop()
{
    digitalWrite(BUILD_IN_LED, HIGH);
    Serial.println("HIGH");
    delay(1000);
    digitalWrite(BUILD_IN_LED, LOW);
    Serial.println("LOW");
    delay(1000);
}
