const int ledPin = 2; // Pin LED bawaan pada sebagian besar ESP32

void setup() {
  Serial.begin(115200); // Kecepatan komunikasi harus sama dengan Python
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);
}

void loop() {
  // Cek apakah ada data masuk dari Python
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      digitalWrite(ledPin, HIGH); // Nyalakan LED
    } 
    else if (command == '0') {
      digitalWrite(ledPin, LOW);  // Matikan LED
    }
  }
}
