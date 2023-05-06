const int IN1 = 0;
const int IN2 = 1;
const int EN1 = 2;
int duration = 1000;
int mot_speed=180;
void setup() {
  // put your setup code here, to run once:
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(EN1,OUTPUT);
  Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
//  analogWrite(EN1,mot_speed);
  
  forward();
  delay(10);
}

void forward(){
  analogWrite(EN1,mot_speed);
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  delay(duration);
}
