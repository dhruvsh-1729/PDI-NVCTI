#include<Servo.h>
#include<time.h>

//variables
Servo Mservo1;
Servo Mservo2;
Servo Mservo3;
int pos;
int swt = 8;
int thetaup=180,thetadown=180;
int a1=180,a2=thetaup,a3=180,sz=4,path;
int arr1[] = {0,6,7,0};
int arr2[] = {0,1,2,0};
int arr3[] = {3,4,5,0};

void setup() {
  // put your setup code here, to run once:
  Mservo1.attach(3);
  Mservo1.write(a1);
//  /delay(10);
  Mservo2.attach(5);
  Mservo2.write(a2);
//  delay(10);
  Mservo3.attach(6);
  Mservo3.write(a3);
//  de/lay(10);
  pinMode(swt, INPUT);
  Serial.begin(9600);
  Serial.print(a1);
  Serial.print(" ");
  Serial.print(a2);
  Serial.print(" ");
  Serial.println(a3);
}

void funcfront(Servo ms){
//  for(pos=0;pos<=180;pos++){
//      ms.write(pos);
//      delay(10);
//    }

  for(pos=180;pos>=0;pos--){
    ms.write(pos);
    delay(10);
  }
}

void funcback(Servo ms){
//  for(pos=180;pos>=0;pos--){
//    ms.write(pos);
//    delay(10);
//  }
  for(pos=0;pos<=180;pos++){
      ms.write(pos);
      delay(10);
    }
}


void funcfronts(Servo ms){
  for(pos=thetaup;pos>=50;pos--){
    ms.write(pos);
    delay(10);
  }
}

void funcbacks(Servo ms){

  for(pos=0;pos<=thetadown;pos++){
      ms.write(pos);
      delay(10);
    }
}

char operation(int n){
  Serial.println(n);
  int t3 = n%2;
  n = n/2;
  int t2 = n%2;
  n = n/2;
  int t1 = n%2;
  if(t1==1){
    funcfront(Mservo1); 
  }
  else{
    funcback(Mservo1); 
  }
  if(t2==1){
    funcfronts(Mservo2); 
  }
  else{
    funcbacks(Mservo2); 
  }
  if(t3==1){
    funcfront(Mservo3); 
  }
  else{
    funcback(Mservo3); 
  }
}

void operform(int i){
  while(1){
//    Serial.println(digitalRead(swt));
    if(digitalRead(swt) == 1){
      break;
    }
//    Serial.println("i an inf");
  }
  Serial.println("i am out");
  operation(i);
//  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println("i am done1");
  
//  srand(time(0));
   int t=1;
   Serial.print("Path Executing Number: ");
   Serial.println(t);
  
  if(t==1){
    for(int i=0;i<sz;i++)
    {
      operform(arr1[i]);
    }
  }
  else if(t==2){
    for(int i=0;i<sz;i++)
    {
      operform(arr2[i]);
    }
  }
  else {
    for(int i=0;i<sz;i++)
    {
      operform(arr3[i]);
    }
  }
}
