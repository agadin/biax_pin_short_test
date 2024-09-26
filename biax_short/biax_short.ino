// Arduino code to control a 2-relay module connected to pin 8

const int relayPin = 8;
String command = "";

void setup() {
  // Initialize the relay pin as an output
  pinMode(relayPin, OUTPUT);
  // Initialize serial communication at 9600 baud rate
  Serial.begin(9600);
}

void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming byte
    char incomingByte = Serial.read();
    // Append the byte to the command string
    command += incomingByte;

    // Check if the command is complete (ends with a newline character)
    if (incomingByte == '\n') {
      // Remove any trailing newline characters
      command.trim();

      // Check the command and control the relay accordingly
      if (command == "ON") {
        digitalWrite(relayPin, HIGH); // Turn relay on
        Serial.println("Relay is turned on");
      } else if (command == "OFF") {
        digitalWrite(relayPin, LOW); // Turn relay off
        Serial.println("Relay is turned off");
      }

      // Clear the command string for the next command
      command = "";
    }
  }
}