int pwmChannel = 0; 
int frequence = 1000; 
int resolution = 8; // 8-bit resolution, 256 possible values

int EN1=26;
int EN2=25;
int IN1=13;
int IN2=12;
int IN3=14;
int IN4=27;
int EN3=22;
int EN4=23;
int IN5=15;
int IN6=2;
int IN7=4;
int IN8=5;

int speed1=255,speed2=255;
int duration=1000;

void setup() {
  // put your setup code here, to run once:

pinMode(EN1,OUTPUT);
pinMode(EN2,OUTPUT);
pinMode(IN1,OUTPUT);
pinMode(IN2,OUTPUT);
pinMode(IN3,OUTPUT);
pinMode(IN4,OUTPUT);
pinMode(EN3,OUTPUT);
pinMode(EN4,OUTPUT);
pinMode(IN5,OUTPUT);
pinMode(IN6,OUTPUT);
pinMode(IN7,OUTPUT);
pinMode(IN8,OUTPUT);

ledcSetup(pwmChannel, frequence, resolution);

ledcAttachPin(EN1, pwmChannel);
ledcAttachPin(EN2, pwmChannel);
ledcAttachPin(EN3, pwmChannel);
ledcAttachPin(EN4, pwmChannel);
}

void loop() {
  // put your main code here, to run repeatedly:
  
//wheels move forward testing
forward();

//wheels move backward testing
backward();

//wheels moving leftwards
//left();

//wheels moving rightwards
//right();/


}

void forward(){
  ledcWrite(pwmChannel,speed1);
digitalWrite(IN1,LOW);
digitalWrite(IN2,HIGH);
digitalWrite(IN3,LOW);
digitalWrite(IN4,HIGH);
delay(duration);
digitalWrite(IN1,LOW);
digitalWrite(IN2,LOW);
digitalWrite(IN3,LOW);
digitalWrite(IN4,LOW);

delay(3000);

//back wheels move forward
digitalWrite(IN5,LOW);
digitalWrite(IN6,HIGH);
digitalWrite(IN7,LOW);
digitalWrite(IN8,HIGH);
delay(duration);
digitalWrite(IN5,LOW);
digitalWrite(IN6,LOW);
digitalWrite(IN7,LOW);
digitalWrite(IN8,LOW);

delay(3000);

//both motors move forward

digitalWrite(IN1,LOW);
digitalWrite(IN2,HIGH);
digitalWrite(IN3,LOW);
digitalWrite(IN4,HIGH);

digitalWrite(IN5,LOW);
digitalWrite(IN6,HIGH);
digitalWrite(IN7,LOW);
digitalWrite(IN8,HIGH);

delay(duration);

digitalWrite(IN1,LOW);
digitalWrite(IN2,LOW);
digitalWrite(IN3,LOW);
digitalWrite(IN4,LOW);

digitalWrite(IN5,LOW);
digitalWrite(IN6,LOW);
digitalWrite(IN7,LOW);
digitalWrite(IN8,LOW);

delay(3000);
}


void backward(){
  ledcWrite(pwmChannel,speed1);
digitalWrite(IN1,HIGH);
digitalWrite(IN2,LOW);
digitalWrite(IN3,HIGH);
digitalWrite(IN4,LOW);
delay(duration);
digitalWrite(IN1,LOW);
digitalWrite(IN2,LOW);
digitalWrite(IN3,LOW);
digitalWrite(IN4,LOW);

delay(3000);

//back wheels move forward
digitalWrite(IN5,HIGH);
digitalWrite(IN6,LOW);
digitalWrite(IN7,HIGH);
digitalWrite(IN8,LOW);
delay(duration);
digitalWrite(IN5,LOW);
digitalWrite(IN6,LOW);
digitalWrite(IN7,LOW);
digitalWrite(IN8,LOW);

delay(3000);

//both motors move forward

digitalWrite(IN1,HIGH);
digitalWrite(IN2,LOW);
digitalWrite(IN3,HIGH);
digitalWrite(IN4,LOW);

digitalWrite(IN5,HIGH);
digitalWrite(IN6,LOW);
digitalWrite(IN7,HIGH);
digitalWrite(IN8,LOW);

delay(duration);

digitalWrite(IN1,LOW);
digitalWrite(IN2,LOW);
digitalWrite(IN3,LOW);
digitalWrite(IN4,LOW);

digitalWrite(IN5,LOW);
digitalWrite(IN6,LOW);
digitalWrite(IN7,LOW);
digitalWrite(IN8,LOW);

delay(3000);
}
