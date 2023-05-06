const int stepPin = 5; 
const int dirPin = 2;
//const int dirPinrev=3; 
const int enPin = 8;

void setup() {
  pinMode(stepPin,OUTPUT); 
  pinMode(dirPin,OUTPUT);
//  pinMode(dirPinrev,OUTPUT);
  pinMode(enPin,OUTPUT);
  digitalWrite(enPin,LOW);

  Serial.begin(9600);
  
}

void rotatestepper(int numsteps){
  for(int x = 0; x < numsteps; x++) {
    digitalWrite(stepPin,HIGH); 
    delayMicroseconds(500); 
    digitalWrite(stepPin,LOW); 
    delayMicroseconds(500); 
  }
}

void loop() {

  int steps=1600;
  digitalWrite(dirPin,HIGH);// Enables the motor to move in a particular direction
   rotatestepper(1300);
   delay(100);
   for(int i=0;i<50;i++){
   Serial.println(random(900,1024));
   
    }
    float sum = 0;
  for(int i=0;i<20;i++){
      int randNumber = random(0, 60);
//      Serial.println(randNumber);
      digitalWrite(dirPin,HIGH);// Enables the motor to move in a particular direction
      rotatestepper(randNumber);
      sum+=randNumber;
      
      delay(100); // One second delay befire changing direction

      randNumber = random(0, 60);
//      Serial.println(randNumber);
      digitalWrite(dirPin,LOW);//Changes the direction of rotation
      rotatestepper(randNumber);
      sum-=randNumber;

      delay(100); 

      Serial.println(random(150, 200));
       
    }
   // Enables the motor to move in a particular direction
    rotatestepper(1300-sum);
  
}
