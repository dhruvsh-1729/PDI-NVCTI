const int buttonPin = 8;  // the number of the pushbutton pin

// variables will change:
int buttonState = 0;  // variable for reading the pushbutton status

void setup() {
  // initialize the LED pin as an output:
  Serial.begin(9600);
  Serial.println("Starting now....");
  pinMode(buttonPin,INPUT);
}

void loop(){

  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState);
  delay(50);
}
