/*
    MPU6050 Triple Axis Gyroscope & Accelerometer. Pitch & Roll Accelerometer Example.
    Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-zyroskop-i-akcelerometr-mpu6050.html
    GIT: https://github.com/jarzebski/Arduino-MPU6050
    Web: http://www.jarzebski.pl
    (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
#include <MPU6050.h>
#define Pi 3.14159
MPU6050 mpu;
float prev_roll=0;
float prev_pitch =0;
void setup() 
{
  Serial.begin(115200);

  Serial.println("Initialize MPU6050");

  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
}

void loop()
{
  // Read normalized values 
  Vector A = mpu.readNormalizeAccel();
  float Ax= A.XAxis;
  float Ay= A.YAxis;
  float Az= A.ZAxis;

  float pitch = -atan2(Ay,Ax)*180/Pi;
  pitch = 0.5*prev_pitch + 0.5*pitch;
  Serial.print(pitch);
  Serial.print(" ");
  float roll = -atan2(Az,Ax)*180/Pi;
  roll = 0.5*prev_roll + 0.5*roll;
  Serial.println(roll);

//Serial.print(Ax);
//Serial.print(" ");
//Serial.print(Ay);
//Serial.print(" ");
//Serial.print(Az);
//Serial.println(" ");

  // Calculate Pitch & Roll
//  int pitch = -(atan2(normAccel.XAxis, sqrt(normAccel.YAxis*normAccel.YAxis + normAccel.ZAxis*normAccel.ZAxis))*180.0)/M_PI;
//  int roll = (atan2(normAccel.YAxis, normAccel.ZAxis)*180.0)/M_PI;

  
  delay(100);
}
