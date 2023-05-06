int IN1=D1;
int IN2=D2;
int EN1=D0;
int duration=200;
void setup() {
  // put your setup code here, to run once:
pinMode(IN1,OUTPUT);
pinMode(IN2,OUTPUT);
pinMode(EN1,OUTPUT);

}

void loop() {
  // put your main code here, to run repeatedly:
analogWrite(EN1,255);
digitalWrite(IN1,HIGH);
digitalWrite(IN2,LOW);
delay(duration);
}
