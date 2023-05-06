int IN1= D0;
int IN2= D1;
int IN3= D2;
int IN4= D3;
int ENA= D6;
int ENB= D5;
int duration = 500;
void setup() {
  // put your setup code here, to run once:
pinMode(IN1,OUTPUT);
pinMode(IN2,OUTPUT);
pinMode(IN3,OUTPUT);
pinMode(IN4,OUTPUT);
pinMode(ENA,OUTPUT);
pinMode(ENB,OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
forward();
delay(duration);
}

void forward(){
// analogWrite(ENA,255);
// analogWrite(ENB,255);
 digitalWrite(IN1,HIGH);
 digitalWrite(IN2,LOW);
 digitalWrite(IN3,HIGH);
 digitalWrite(IN4,LOW);
 delay(duration);
// analogWrite(ENA,0);
// analogWrite(ENB,0);
 digitalWrite(IN1,LOW);
 digitalWrite(IN2,LOW);
 digitalWrite(IN3,LOW);
 digitalWrite(IN4,LOW); 
}
