/*
    MPU6050 Triple Axis Gyroscope & Accelerometer. Pitch & Roll & Yaw Gyroscope Example.
    Read more: http://www.jarzebski.pl/arduino/czujniki-i-sensory/3-osiowy-zyroskop-i-akcelerometr-mpu6050.html
    GIT: https://github.com/jarzebski/Arduino-MPU6050
    Web: http://www.jarzebski.pl
    (c) 2014 by Korneliusz Jarzebski
*/

#include <Wire.h>
#include <MPU6050.h>
#define Pi 3.14159
MPU6050 mpu;

// Timers
unsigned long timer = 0;
float timeStep = 0.01;
float prev_roll=0;
float prev_pitch =0;
// Pitch, Roll and Yaw values
float pitch_g = 0;
float roll_g = 0;
//float yaw_g = 0;
float pitch_m;
float roll_m;
void setup() 
{
  Serial.begin(115200);

  // Initialize MPU6050
  while(!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  
  // Calibrate gyroscope. The calibration must be at rest.
  // If you don't want calibrate, comment this line.
  mpu.calibrateGyro();

  // Set threshold sensivty. Default 3.
  // If you don't want use threshold, comment this line or set 0.
  mpu.setThreshold(3);
}

void loop()
{
  timer = millis();

  // Read normalized values
  Vector norm = mpu.readNormalizeGyro();
  
  Vector A = mpu.readNormalizeAccel();
  float Ax= A.XAxis;
  float Ay= A.YAxis;
  float Az= A.ZAxis;

  float pitch = -atan2(Ay,Ax)*180/Pi;
  pitch = 0.1*prev_pitch + 0.9*pitch;
//  Serial.print(pitch);
//  Serial.print(" ");
  float roll = -atan2(Az,Ax)*180/Pi;
  roll = 0.1*prev_roll + 0.9*roll;
//  Serial.println(roll);
  
  // Calculate Pitch, Roll and Yaw
  pitch_g = pitch_g + norm.YAxis * timeStep;
  roll_g = roll_g + norm.XAxis * timeStep;
//  yaw_g = yaw_g + norm.ZAxis * timeStep;

pitch_m = 0.9*pitch_g + 0.1*pitch;
roll_m = 0.9*roll_g + 0.1*roll;

  Serial.print(pitch_m);
  Serial.print(" ");
  Serial.println(roll_m);

  // Wait to full timeStep period
  delay((timeStep*1000) - (millis() - timer));
}
