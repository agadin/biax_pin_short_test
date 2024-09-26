#include <Servo.h>

Servo myServo;  // Create a servo object

const int servoPin = 9;  // Pin to which the servo is connected
const int angle1 = 30;   // First angle to rotate to
const int angle2 = 0;    // Second angle to rotate back to

void setup() {
  myServo.attach(servoPin);  // Attach the servo to the specified pin
  Serial.begin(9600);        // Start serial communication at 9600 baud
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();  // Read the incoming command
    if (command == 'R') {          // If the command is 'R', rotate the servo
      myServo.write(angle1);       // Rotate to 30 degrees
      delay(1000);                 // Wait for 1 second
      myServo.write(angle2);       // Rotate back to 0 degrees
      delay(1000);                 // Wait for 1 second
    }
  }
}